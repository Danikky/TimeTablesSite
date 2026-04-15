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