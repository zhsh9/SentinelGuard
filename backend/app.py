from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# --------------------------------------------------------------------------------------
# Configuration
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Regitser blueprints
    # from .views import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    return app

# Flask Application Init.
app = create_app()
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
# API: Scapy - sniff, capture network packets
from sniff_route import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Flask Application Executing:
if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8001,
        debug=True,
    )
