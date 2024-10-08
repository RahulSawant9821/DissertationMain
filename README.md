# ReadMe file for running interactive dashboard using machine learning
# NOTE : The csv file needed to run the Cust_Seg notebook is in the same folder as that of Cust_Seg jupyter file, named as raw.csv
# NOTE : Please Run the Cust_Seg jupyter notebook first, otherwise no database will be created. Next move to execution of the Recommendations notebook.
# NOTE : Execute the dbschema.py file in the models folder to create the user table.

Steps to be followed : 

1. Make sure that python is installed on your system, if not install python version 3.12 and above.
2. Open the main project directory which is CODE or code in visual studio code editor.
3. To install all the dependencies with a single command in terminal directed to the main project directory, " pip install -r requirements.txt".
4. Primarily, run the customer segmentation jupyter notebook by selecting the appropriate kernel. This execution may take some time. This step create our database for whole project. So make sure the database has been created in the specified location. The location for database would be : "C:\\FinalYearProject\\code\\code\\data\\clustered_data\\dashboard_database.db".
5. Important Note, the csv file fed to Cust_seg Jupyter notebook is at same location as that of jupyter notebook, named as raw.csv .
5. Next step is to execute the jupyter notebook called as Recommendation. 
6. Furthermore, an important step is to create user table. From the main directory Code, using command redirect to models folder within dashboard. The command to do so, " cd flask_app\dashboard\models". 
7. Once you reach the above mentioned location in the folder structure, run this command " python dbschema.py". Once this is executed succesfully head to the next step. This create a user table in the existing database.
8. Now, open two new terminals. One for running flask api and the other for frontend application.
9. For running backend API, first head to the folder using terminal, the command " cd flask_app\dashboard".
10. Once you are in the above mentioned directory, run the command, "python app.py" . This will start our backend API.
11. Now on the other terminal, redirect to streamlit folder  using the terminal, the command to do so is " cd flask_app\dashboard\streamlit".
12. Once you are at this location, run the command " streamlit run main.py"

The above steps will help to start the user interface of the tool. The user will be redirected to register and login page.
1. The user needs to register first and then head to login. After register, the user again needs to login by switching to the login tab.
2. Upon entering the credentials in the login page, DOUBLE Click on SUBMIT button or repeatedly click on submit button until the page redirects. 

Some features are unavailable for default user, hence to access features of the admin role. 
1. After registeration is done, install DB browser for sqlite and browse to our database location "C:\\FinalYearProject\\code\\code\\data\\clustered_data\\dashboard_database.db".
2. From the database, access the user table.
3. Locate the registered username, and change its role using the DB browser editor tool on the right hand side. You could change to any role, like User, Editor and Admin.
4. After doing so apply changes to the table.
5. From the toolbar in the header, write changes to the database and close the DB browser tool.
6. After succesfully performing these steps, head to the login page and enter your credentials and press submit button twice repeatedly. 

Now you could access all the admin features as well. If the tool is crashing, it might be due to streamlit session crash. No worries, you can again login and all the functionalities will be working completely fine this time.