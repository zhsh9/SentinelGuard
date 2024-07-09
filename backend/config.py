# Username and Password for Login
import hashlib
import os

# Dashboard Manager Account Info
USERNAME = 'sentinelguard'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
if SECRET_KEY != 'you-will-never-guess':
    _PASSWORD = SECRET_KEY
else:
    _PASSWORD = 'sentinelguard'
PASSWORD = hashlib.sha256(_PASSWORD.encode('utf-8')).hexdigest()

# Mantain tokens for login process.
TOKEN = []  # You can generate this dynamically if needed, and use is to check connection
