# Username and Password for Login
import hashlib
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
USERNAME = 'qwe'
_PASSWORD = 'qwe'
PASSWORD = hashlib.sha256(_PASSWORD.encode('utf-8')).hexdigest()
TOKEN = []  # You can generate this dynamically if needed, and use is to check connection
