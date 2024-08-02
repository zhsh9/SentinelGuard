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
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Release mode.
# CORS(app, resources={r'/*': {
#     'origins': 'http://127.0.0.1:8000',
#     'allow_headers': ["Access-Control-Allow-Origin"],
# }})
# Dev mode.
CORS(app, resources={r'/*': {
    'origins': [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'http://127.0.0.1:8001',
        'http://localhost:8001',
    ]
}})
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Home page: hello world
@app.route('/', methods=['GET'])
def list_apis():
    # List all the available APIs
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ','.join(sorted(rule.methods))
            routes.append({
                'endpoint': rule.endpoint,
                'methods': methods,
                'url': str(rule)
            })

    return jsonify({
        'APIs': routes
    })
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# API: Check username and password
#      Check login status
from route.user_manage import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# API: Database
from route.database import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# API: Scapy - sniff, capture network packets
from route.sniff import *
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Flask Application Executing:
if __name__ == '__main__':
    run_params = {
        'host': None,
        'port': 8001,
        'debug': True,
        'processes': True,
        'threaded': True,
    }
    if app.config['DEV']:
        run_params['host'] = '0.0.0.0'
    else:
        run_params['host'] = '127.0.0.1'
        run_params['debug'] = False

    app.run(**run_params)
