import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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
                 group_id INTEGER,
                 FOREIGN KEY(group_id) REFERENCES groups(id));''')

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
    password = generate_password_hash("123")
    try:
        c.execute('INSERT INTO users (username, password, group_id) VALUES (?, ?, ?)', ("admin", password, 'ИСИП23п'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    
def add_group(name, curse):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('INSERT INTO groups (name, curse) VALUES (?, ?)', (name, curse))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    
def delete_group(name):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('DELETE FROM groups WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def change_group(name, curse):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('UPDATE groups SET curse = ? WHERE name = ?', (curse, name))
    conn.commit()
    conn.close()

def change_user(username, password, group):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('UPDATE users SET password = ?, group = ? WHERE username = ?', (password, group, username))
    conn.commit()
    conn.close()