import streamlit as st
import pandas as pd
import requests



#allowing only Admins to view this page
if st.session_state.role == 'User':
    st.warning("Not authorized")
else:
    st.session_state.Users = " "

    def getUsers_():
            global access_token
            if  st.session_state.token: 
                api = f"http://127.0.0.1:5000/getUsers"
                headers = {'Authorization': f"Bearer {st.session_state.token}"}
                response = requests.get(api,headers=headers)
                data = response.json()
                if not isinstance(data, list):
                    raise ValueError(f"Expected a list, but got {type(data)}")
            
                userTable = pd.DataFrame(data)
                if 'id' in userTable.columns:
                     userTable.set_index('id', inplace=True)

                st.session_state.Users = userTable
                userTable = pd.DataFrame(data)
                return userTable
        

    getUsers = getUsers_()
  
    getUsers = getUsers.drop(columns=['password'])
    st.dataframe(getUsers,use_container_width=True)
    Refresh_ = st.button("Refresh")
    if Refresh_:
       st.session_state.Users=getUsers_()

    def changeRole():
        with st.form("changeRole"):
            st.write("Welcome Admin, you can change roles here.")
            st.selectbox("Select User Id : ", getUsers['id'],key="userID")
            st.selectbox("Select User Roles : ",['User',"Editor",'Admin'],key="setRole")

            if st.form_submit_button("Change"):
                api = f"http://127.0.0.1:5000/setUsers"
                data = {'action':"changeRole","user_id":st.session_state.userID,"setRole":st.session_state.setRole,"role":st.session_state.role}
                headers = {'Authorization': f"Bearer {st.session_state.token}"}
                response = requests.post(api,json=data,headers=headers)

                if response.status_code == 201:
                    data = response.json()
                    st.success("Role changed Successfully")
            
                else:
                    err = response.json()['error']
                    st.warning(err)




    def removeUser():

        with st.form("removeUser"):
            st.write("Welcome Admin, you can remove users here.")     
            st.selectbox("Select User Id : ", getUsers['id'],key="userID_")
  

            if st.form_submit_button("Remove"):
                api = f"http://127.0.0.1:5000/setUsers"
                data = {'action':"removeUser","user_id":st.session_state.userID_,"role":st.session_state.role}
                headers = {'Authorization': f"Bearer {st.session_state.token}"}
                response = requests.post(api,json=data,headers=headers)

                if response.status_code == 201:
                    data = response.json()
                    st.success("User removed Successfully")
            
                else:
                    err = response.json()['error']
                    st.warning(err)     




    tab1 , tab2 = st.tabs(["Change Role","Remove User"])

    with tab1:
        changeRole()

    with tab2:
        removeUser()

 
      


