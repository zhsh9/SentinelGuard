from app import app
from flask import jsonify, request
import secrets
import hashlib

logger = app.config['LOGGER']

# API: Check username and password
@app.route('/api/login', methods=['POST'])
def login():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return jsonify({'error': 'Missing username or password'}), 400
    # Check username and password
    username = request.json['username']
    _password = request.json['password']
    password = hashlib.sha256(_password.encode('utf-8')).hexdigest()

    if username == app.config['USERNAME'] and password == app.config['PASSWORD']:
        token = secrets.token_hex(16)  # Generate a new token
        app.config['TOKEN'].append(token)
        
        # Log the successful login and token generation
        logger.info(f"User '{username}' logged in successfully. Token: {token}")
        
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 400


# API: Check login status
@app.route('/api/verify', methods=['POST'])
def check_login():
    if not request.json or not 'token' in request.json:
        return jsonify({'error': 'Missing token'}), 400

    token = request.json['token']

    if token in app.config['TOKEN']:
        # Log the successful token verification
        logger.info(f"Token verified successfully: {token}")
        
        return jsonify({'status': '200', 'msg': 'Logged in'}), 200
    else:
        # Log the failed token verification
        logger.warning(f"Invalid token: {token}")
        
        return jsonify({'status': '401', 'msg': 'Invalid token'}), 401
