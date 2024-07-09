# Username and Password for Login
import hashlib
import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ------------------------------- Log -------------------------------
    # log save path
    LOG_FILE = os.path.join(basedir, 'app.log')
    # Logger
    # Set up logging
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)

    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(file_formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)
    
    # ------------------------------- Login -------------------------------
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

    # ------------------------------- Database -------------------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Test Config Class
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False