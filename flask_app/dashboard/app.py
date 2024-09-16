from flask import Flask,jsonify,request
import sqlite3
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import timedelta
#https://flask-jwt.readthedocs.io/en/latest/ : deprecated
#https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html





# Initializing app instances and loading configuration from config files
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) 
app.config['SECRET_KEY']
CORS(app)
jwt = JWTManager(app)









# This function is used to establish a connection with the sqlite database
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    if conn is not None:
        conn.row_factory = sqlite3.Row
        return conn
    
    raise sqlite3.OperationalError('Failed to connect to database')






@app.route('/register',methods=['POST'])
def user_registration():

    data = request.get_json()
    if not data:
        return jsonify({'error': "Invalid input"}), 400
    
    username = data.get('username')
    password = data.get('password')
    role = data.get('role','User')

    if not username or not password :
        return jsonify({'error':"Missing username and password"}), 400
    try :
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("Select username from users where username=?",(username,))
        existing_user = cursor.fetchone()

        if existing_user :
            return jsonify({'error':'Username already exists'}),400
        
        #https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html
        hashed_Password = generate_password_hash(password)

        cursor.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",(username,hashed_Password,role))

        conn.commit()
        conn.close()

        return jsonify({'message':"User registered"}), 201
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}),500        






@app.route('/login',methods=['POST'])
def user_login():

    data = request.get_json()
    if not data:
        return jsonify({'error':'No Input provided'}),400
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error':'No username or password provided'}),400
    
    try :
        conn = get_db_connection()
        cursor  = conn.cursor()
        cursor.execute("Select * from users WHERE username=?",(username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'error':'User does not exist'}),401
        
        if not check_password_hash(user['password'],password):
            return jsonify({'error':'Invalid password'}),401
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_active = 1 WHERE id =?",(user['id'],))
        conn.commit()
        conn.close()
        access_token = create_access_token(identity=user['username'])
        refresh_token = create_access_token(identity=user['username'])
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': user['username'],   
            'role': user['role'],  
            'userId': user['id']    
        }), 200
    
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}),500





@app.route('/logout',methods=['POST'])
@jwt_required()
def user_logout():
    user = get_jwt_identity()
    try:
        if user:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = 0 WHERE username =?",(user,))
            conn.commit()
            conn.close()

            return jsonify({'message':'User logged out'}),201
        else:
            return jsonify({'error':'No data recieved'}),401
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}),500
     




@app.route('/getUsers',methods=['GET'])
@jwt_required()
def getUsers():
    try:
        conn = get_db_connection()
        users = []
        for row in conn.execute("Select * from users"):
            users.append(dict(row))
        conn.close()
        return jsonify(users)
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}),500





@app.route('/setUsers',methods=['POST'])
@jwt_required()
def setUsers():
    data = request.get_json()
    if not data:
        return jsonify({'error':"Request body not found"}),400
    
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")
    
    current_user_id = get_jwt_identity()

    # Fetch the current user's role from the database using the ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username =?", (current_user_id,))
    user_role = cursor.fetchone()['role']
    conn.close()

    if user_role == 'Admin':
        action =  data.get('action')
        user_id = data.get('user_id')
        conn = get_db_connection()
        cusror = conn.cursor()
        try :
            if action == 'changeRole':
                role_ = data.get("setRole") #role to be changed for particular user
                cusror.execute("UPDATE users SET role = ? WHERE id =?",(role_,user_id))
                conn.commit()
                return jsonify({'message':'Role updated successfully'}),201
            elif action =='removeUser':
                cusror.execute("DELETE  from users where id=?",(user_id,)) 
                conn.commit()
                return jsonify({'message':'user removed successfully'}),201
            else:
                return jsonify({'error':'Invalid Action'}),400
        except sqlite3.Error as e:
            return jsonify({'error':str(e)},500)
        finally:
            conn.close()
    return jsonify({'error':'Unauthorized to perform this operation'}),401







#https://stackoverflow.com/questions/69311855/how-to-fix-typeerror-object-of-type-row-is-not-json-serializable-obviously-cr
# API for clusters
@app.route('/clusters',methods=['GET'])
@jwt_required()
def getClusters():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")
    user = get_jwt_identity()
    if user:
        try:
            conn = get_db_connection()
            Kmeans_ = []
            for row in conn.execute("SELECT * FROM Main_Kmeans_clusters"):
                Kmeans_.append(dict(row))
               
            conn.close()
            return jsonify(Kmeans_)
        except sqlite3.Error as e:
            return jsonify({'error':str(e)},500)





# API for RFM customers
@app.route('/RFMCust',methods=['GET'], endpoint='RFMCustomer')
@jwt_required()
def getRFMCust():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")
    user = get_jwt_identity()
    if user:
        try:
            conn = get_db_connection()
            RFMCust = []
            for row in conn.execute("SELECT * FROM RFM_Customer_segments"):
                RFMCust.append(dict(row))
                #print(RFMCust)
            conn.close()
            return jsonify(RFMCust)
        except sqlite3.Error as e:
            return jsonify({'error':str(e)},500)



# API for RFM product
@app.route('/RFMProd',methods=['GET'], endpoint='RFMProduct')
@jwt_required()
def getRFMProd():
    auth_header = request.headers.get('Authorization')
    print(f"Authorization Header: {auth_header}")
    user = get_jwt_identity()
    if user:
        try:
            conn = get_db_connection()
            RFMProd = []
            for row in conn.execute("SELECT * FROM RFM_Product_segments"):
                RFMProd.append(dict(row))
            conn.close()
            return jsonify(RFMProd)
        except sqlite3.Error as e:
            return jsonify({'error':str(e)},500)
    
    
@app.route('/protected_resource', methods=['GET'])
@jwt_required()
def protected_resource():
    user_id = get_jwt_identity()
    # Use user_id for authorization or other logic
    return jsonify({'message': f'Hello, {user_id}!'})

if __name__ == '__main__':
    app.run( debug=True)


