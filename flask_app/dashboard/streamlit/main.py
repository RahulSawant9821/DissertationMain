import streamlit as st
import pandas as pd
import requests

base_API = "http://127.0.0.1:5000"

access_token = st.session_state.get('token', None)







# fetching data from sqlite DB
@st.cache_data(ttl=3600)
def fetchClusterData():
    global access_token
    if  access_token : 
        api = f"http://127.0.0.1:5000/clusters"
        headers = {'Authorization': f"Bearer {st.session_state.token}"}
        response = requests.get(api,headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
            
        else :
            st.error("Failed to fetch data")
        
@st.cache_data(ttl=3600)       
def fetchRFMCustData():
    global access_token
    if  access_token : 
        api = f"{base_API}/RFMCust"
        headers = {'Authorization': f"Bearer {st.session_state.token}"}
        response = requests.get(api,headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.warning("Failed to fetch data")
        return st.session_state.RFMCust
    
@st.cache_data(ttl=3600)    
def fetchRFMProdData():
    global access_token
    if  access_token : 
        api = f"{base_API}/RFMProd"
        headers = {'Authorization': f"Bearer {st.session_state.token}"}
        response = requests.get(api,headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.warning("Failed to fetch data")

        return st.session_state.RFMProd


def register_user():
    
    with st.form("registration_form"):
        st.header("Register Form")
        username = st.text_input("Username : ", key="username")
        password = st.text_input("Password : ",type="password",key="password")
        confirm_password =  st.text_input(" Confirm Password : ",type="password",key="confirmPassword")
        submitted = st.form_submit_button("Register",use_container_width=True)
        
        if submitted:
            if password == confirm_password :
                    api = f"http://127.0.0.1:5000/register"
                    data = {"username":username,"password":password}
                    response = requests.post(api,json=data)

                    if response.status_code == 201:
                        data = response.json()
                        st.success(data['message'])
                    else:
                        err = data['error']
                        st.warning(err)
        
 
headers = {}
#https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
def user_login():
    with st.form("login_form"):
        st.header("Login Form")
        username = st.text_input("Username : ")
        password = st.text_input("Password : ",type="password")
        submitted = st.form_submit_button("Submit",use_container_width=True)
        
        if submitted:
            api = f"http://127.0.0.1:5000/login"
            data = {"username":username,"password":password}
            response = requests.post(api,json=data)
            
            if response.status_code == 200:
                data = response.json()  
                # headers are required when making flask api calls, they are used to authenticate the user in backend
                global access_token
                headers = {'Authorization': f"Bearer {data['access_token']}"}
                st.session_state['username'] = data['username']
                st.session_state['role'] = data['role']
                st.session_state.user_id = data['userId']
                st.session_state.authenticated = True
                token = data['access_token']
                st.session_state.token = token
                st.session_state.headers = headers
                
            else:
                err = response.json()['error']
                st.warning(err)
    

def logout_user():
    if 'token' in st.session_state :
        api = f"{base_API}/logout"
        headers = {'Authorization': f"Bearer {st.session_state.token}"}
        response = requests.post(api,headers=headers)

        if response.status_code == 201:
            st.session_state.authenticated = False
            st.session_state.token= ""
            st.session_state.username = None
            st.session_state.role = None
            st.success("Logged out successfully")
        else:
            st.error("Logout failed")
    else:
        st.warning("User not logged in")
    st.session_state.clear()
    st.rerun()


def main():
    #st.logo(image="C:\\FinalYearProject\\code\\code\\flask_app\\dashboard\\static\\logo.png")
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if st.session_state.authenticated == True :
        


        clusterData = fetchClusterData()
        RFMCust = fetchRFMCustData()
        RFMProd = fetchRFMProdData()

        if clusterData is not None or RFMCust is not None or RFMProd is not None:
            st.session_state.clusterdata = clusterData
            st.session_state.RFMProd = RFMProd
            st.session_state.RFMCust = RFMCust
        else : 
            st.error("no data fetched")
        

        

        # page navigations
        p1 = st.Page("pages/custAnalysis.py",title=" Customer Analysis ", icon=":material/people:")
        p2 = st.Page("pages/prodAnalysis.py",title=" Product Analysis ", icon=":material/inventory:")
        p3 = st.Page("pages/dataAnalysis.py",title=" Data Cleaning ", icon=":material/source:")
        p4 = st.Page("pages/recommendation.py",title=" Recommendation ", icon=":material/assistant:")
        p5 = st.Page("setting/access.py",title=" Control Access ", icon=":material/account_circle:")

       
        
        logout_button = st.sidebar.button("Logout",key="logout_button")

        if logout_button:
            logout_user()

        pg = st.navigation({
            "Dashboard":[p1,p2,p3,p4],
            "Setting": [p5]
        })

        pg.run()

    else:
     
        login , register = st.tabs(["Login","Register"])

        with login:
            user_login()
        with register:
            register_user()
        

if __name__ =="__main__":
    main()