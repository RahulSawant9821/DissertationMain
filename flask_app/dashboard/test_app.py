from app import app
import sqlite3
import unittest
import unittest.mock as mock

def test_get_db_connection():
        conn = sqlite3.connect('C:\\FinalYearProject\\code\\code\\data\\clustered_data\\dashboard_database.db')
        assert conn is not None

#https://www.geeksforgeeks.org/unit-testing-python-unittest/
#https://stackoverflow.com/questions/6854658/explain-the-setup-and-teardown-python-methods-used-in-test-cases
#https://restfulapi.net/http-status-codes/#2xx

class RFMProdApiTesting(unittest.TestCase):
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_RFMProd_data_retrivial_success(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            #Error Faced : https://programmaticallyspeaking.com/mocking-__iter__-with-a-magic-mock-in-python.html 
            #Solution : Magic mock object https://www.w3schools.com/python/python_iterators.asp
            mock_cursor.__iter__.return_value = [{'cluster':2},{'cluster':3}]
            response = self.app.get('/RFMProd')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[{'cluster':2},{'cluster':3}])



    def test_RFMProd_data_retrivial_empty(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            mock_cursor.__iter__.return_value = []
            response = self.app.get('/RFMProd')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[])




class RFMCustApiTesting(unittest.TestCase):
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_RFMCust_data_retrivial_success(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            #Error Faced : https://programmaticallyspeaking.com/mocking-__iter__-with-a-magic-mock-in-python.html 
            #Solution : Magic mock object https://www.w3schools.com/python/python_iterators.asp
            mock_cursor.__iter__.return_value = [{'cluster':2},{'cluster':3}]
            response = self.app.get('/RFMCust')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[{'cluster':2},{'cluster':3}])



    def test_RFMCust_data_retrivial_empty(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            mock_cursor.__iter__.return_value = []
            response = self.app.get('/RFMCust')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[])



class getUsers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_users_data_retrivial_success(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            mock_cursor.__iter__.return_value = [{'cluster':2},{'cluster':3}]
            response = self.app.get('/getUsers')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[{'cluster':2},{'cluster':3}])




    def test_users_data_retrivial_empty(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            mock_cursor.__iter__.return_value = []
            response = self.app.get('/getUsers')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[])



class clusterApiTesting(unittest.TestCase):
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_cluster_data_retrivial_success(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            #Error Faced : https://programmaticallyspeaking.com/mocking-__iter__-with-a-magic-mock-in-python.html 
            #Solution : Magic mock object https://www.w3schools.com/python/python_iterators.asp
            mock_cursor.__iter__.return_value = [{'cluster':2},{'cluster':3}]
            response = self.app.get('/clusters')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[{'cluster':2},{'cluster':3}])




    def test_cluster_data_retrivial_empty(self):
        with mock.patch('app.get_db_connection') as mock_db:
            mock_conn = mock.MagicMock()
            mock_db.return_value = mock_conn

            mock_cursor = mock.MagicMock()
            mock_conn.execute.return_value = mock_cursor

            mock_cursor.__iter__.return_value = []
            response = self.app.get('/clusters')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json,[])





class setUsers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_noData(self):
        response = self.app.post('/setUsers',json={" "})
        self.assertEqual(response.status_code,400)
        self.assertEqual("Request body not found",response.json['error'])

    def test_user_not_authorized(self):
        response=self.app.post('/setUsers',json=
                               {
                                    "user_id":2,
                                    "role":"user",
                                    "action":"changeRole",
                                    "setRole": "editor"

                                    })
        self.assertEqual(response.status_code,401)
        self.assertEqual('Unauthorized to perform this operation',response.json['error'])


    def test_change_user_role(self):
        response=self.app.post('/setUsers',json=
                               {
                                    "user_id":1,
                                    "role":"admin",
                                    "action":"changeRole",
                                    "setRole": "editor"

                                    })
        self.assertEqual(response.status_code,201)
        self.assertEqual('Role updated successfully',response.json['message'])


    def test_remove_user_role(self):
        response=self.app.post('/setUsers',json=
                               {
                                    "user_id":2,
                                    "role":"admin",
                                    "action":"removeUser"
                                    })
        self.assertEqual(response.status_code,201)
        self.assertEqual('user removed successfully',response.json['message'])

    def test_incorrect_action(self):
        response=self.app.post('/setUsers',json=
                               {
                                    "user_id":2,
                                    "role":"admin",
                                    "action":"delete",
                                    "setRole": "editor"

                                    })
        self.assertEqual(response.status_code,401)
        self.assertEqual('Invalid Action',response.json['error'])





class LoginTesting(unittest.TestCase):
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_user_login_success(self):
         response = self.app.post('/login',json={
              'username':'test_user',
              'password':'test_pass'
         })
         self.assertEqual(response.status_code,200)
         self.assertEqual('Login Successful',response.json['message'])

    def test_user_not_registered(self):
        response=self.app.post('/login',json={
              'username':'raw_user',
              'password':'raw_pass'
         })
        self.assertEqual(response.status_code,401)
        self.assertEqual('User does not exist',response.json['error'])


    def test_incorrect_credentials(self):
        response=self.app.post('/login',json={
              'username':'dup_user',
              'password':'test_pass'
         })
        self.assertEqual(response.status_code,401)
        self.assertEqual('Invalid password',response.json['error'])


    def test_user_credential_missing(self):
        response = self.app.post('/login',json={})
        self.assertEqual(response.status_code,400)
        self.assertEqual("No Input provided",response.json['error'])






class RegistrationTesting(unittest.TestCase):
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_user_registration_success(self):
         response = self.app.post('/register',json={
              'username':'test_user',
              'password':'test_pass'
         })
         self.assertEqual(response.status_code,201)
         self.assertEqual('User registered',response.json['message'])

    def test_user_already_Exist(self):
        self.app.post('/register',json={
              'username':'dup_user',
              'password':'dup_pass'
         })
        response=self.app.post('/register',json={
              'username':'dup_user',
              'password':'dup_pass'
         })
        self.assertEqual(response.status_code,400)
        self.assertEqual('Username already exists',response.json['error'])


    def test_user_details_missing(self):
        response = self.app.post('/register',json={})
        self.assertEqual(response.status_code,400)
        self.assertEqual("Invalid input",response.json['error'])


class LogoutTesting(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_noData(self):
        response = self.app.post('/logout',json={})
        self.assertEqual(response.status_code,400)
        self.assertEqual("Request body not found",response.json['error'])

    def test_user_id_not_found(self):
        response=self.app.post('/logout',json=
                               { "user_id":" "
                                    })
        self.assertEqual(response.status_code,401)
        self.assertEqual('user id not found',response.json['error'])


    def test_user_id_logout(self):
        response=self.app.post('/logout',json=
                               {
                                    "user_id":1
                                    })
        self.assertEqual(response.status_code,201)
        self.assertEqual('User logged out',response.json['message'])






if __name__=='__main__':
    unittest.main()

         
        



    




