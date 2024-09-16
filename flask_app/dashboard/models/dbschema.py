import sqlite3

conn = sqlite3.connect('C:\\FinalYearProject\\code\\code\\data\\clustered_data\\dashboard_database.db')
cursor = conn.cursor()
cursor.execute('''
DROP TABLE IF EXISTS users;
''')


cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    "is_active" BOOLEAN DEFAULT FALSE
)
''')

conn.commit()
conn.close()


