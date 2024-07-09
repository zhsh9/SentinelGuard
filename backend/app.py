from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

# --------------------------------------------------------------------------------------
# Configuration
# Flask Application Init.
app = Flask(__name__)
app.config.from_object(Config)
# Used to initialize the SQLAlchemy object and bind it to the Flask application instance.
db = SQLAlchemy(app)

# Release mode.
# CORS(app, resources={r'/*': {
#     'origins': 'http://127.0.0.1:8000',
#     'allow_headers': ["Access-Control-Allow-Origin"],
# }})
# Dev mode.
CORS(app, resources={r'/*': {'origins': '*'}})
# --------------------------------------------------------------------------------------

# Home page: hello world
@app.route('/', methods=['GET'])
def index():
    return "Hello world!!! I'm zhsh aka qwe."


# --------------------------------------------------------------------------------------
# API: Check username and password
#      Check login status
from login_route import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# API: Database
from db_route import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Flask Application Executing:
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8001,
        debug=True,
    )
