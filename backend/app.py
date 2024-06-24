from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import secrets
import hashlib

app = Flask(__name__)

app.config.from_object('config')

CORS(app, resource={r'/*': {
    'origins': 'http://127.0.0.1:8000',
    'allow_headers': ["Access-Control-Allow-Origin"],
}})


# Home page: hello world
@app.route('/', methods=['GET'])
def index():
    return "Hello world!!! I'm zhsh aka qwe."


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
        return jsonify({'status': '200', 'msg': 'Logged in'}), 200
    else:
        return jsonify({'status': '401', 'msg': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8001,
        debug=True,
    )
