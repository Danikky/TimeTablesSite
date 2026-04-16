import sqlite3

db_name = "users.db"

def create_db():
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT UNIQUE,
                 password TEXT,
                 email TEXT,
                 phone TEXT,
                 group TEXT);''')
    c.execute('''CREATE TABLE IF NOT EXISTS groups
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT UNIQUE,
                curse INTEGER);''')
    conn.commit()
    conn.close()

def reg_user(username, password, group):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, group) VALUES (?, ?, ?)', (username, password, group))
    conn.commit()
    conn.close()
    
def login(username):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_text_user():
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, group) VALUES (?, ?, ?)', ("admin", "123", "ИСИП23п"))
    conn.commit()
    conn.close()
    
def add_group(name, curse):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('INSERT INTO groups (name, curse) VALUES (?, ?)', (name, curse))
    conn.commit()
    conn.close()