import secrets

# config.py
DATABASE_PATH = 'C:\\FinalYearProject\\code\\code\\data\\clustered_data\\dashboard_database.db'
#https://docs.python.org/3/library/secrets.html
SECRET_KEY = secrets.token_urlsafe(32)