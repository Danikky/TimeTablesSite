from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
import asyncio
import os
import psutil
import subprocess
import threading
import time
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt
import json
import sqlite3
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_name = db.db_name


@socketio.on('connect', namespace='/server')
def handle_connect():
    print("Клиент подключился к WebSocket")
    
class User(UserMixin):
    def __init__(self, user_id, username, group):
        self.id = user_id
        self.username = username
        self.group = group
        
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(f"{db_name}")
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        group = request.form['group']
        try:
            db.reg_user(username, password, group)
            flash('Регистрация прошла успешно!')
            user_obj = User(db.login(username)[0], username, group)
            login_user(user_obj)
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Пользователь с таким именем уже существует')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.login(username)
        if user and check_password_hash(user[2], password):
            user_obj = User(user[0], user[1], user[3])
            login_user(user_obj)
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('index'))

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/profile/<int:user_id>")
@login_required
def profile_page(user_id):
    return render_template("profile.html")

@app.route("/timetable")
@login_required
def timetable():
    return render_template("timetable.html")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5245, debug=True)
