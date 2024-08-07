# Username and Password for Login
import hashlib
import os
import logging
from scapy.all import AsyncSniffer

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ------------------------------- Log -------------------------------
    # Development mode
    DEV = True
    
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
    SQL_DB_NAMES = ['sentinel']
    CUR_DB_INDEX = 0
    CUR_DB_NAME = SQL_DB_NAMES[CUR_DB_INDEX]
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, f'{CUR_DB_NAME}.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_CLASS_NAME_PREFIX = r'DynamicHttpRequestLog_'
    SQL_TABLE_NAME_PREFIX = r'dynamic_http_request_log_'
    SQL_TIME_FORMAT = r'%Y-%m-%d %H:%M:%S'
    
    TABLES = {}
    TABLE_MAPPER = {}
    USING_TABLE = ''
    
    # ------------------------------- Data Collection -------------------------------
    SNIFFER:AsyncSniffer = None
    PCAP_SAVE_DIR_NAME = 'monitor/pcap'
    # 如果文件夹不存在则创建
    PCAP_SAVE_DIR = os.path.join(os.path.dirname(__file__), PCAP_SAVE_DIR_NAME)
    os.makedirs(PCAP_SAVE_DIR, exist_ok=True)


# Test Config Class
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
