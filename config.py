import os
import yaml

# Get the root directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Build the absolute path of the configuration file
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.yaml')


def load_flask_config(app):
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'config.yaml')
    app.config['config_path'] = config_path
    # Load configuration from YAML file
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    for k, v in config.items():
        app.config[k] = v


def load_config(filename=CONFIG_FILE_PATH):
    # Load configuration from YAML file
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


def extract_server_config(filename=CONFIG_FILE_PATH):
    """
    Extracts server configuration information from the config file.

    :return: A dictionary containing the server configuration details.
             e.g. {'server': 'apache', 'server_config': {'active': False, 'path': '/path/to/server.config'},
                'logs': {'file': {'active': True, 'json': False, 'yaml': False, 'path': '/var/log/apache2/access.log'}}}
    """
    config = load_config(filename)
    return {
        'server': config.get('server'),
        'server_config': config.get('server_config', {}),
        'logs': config.get('logs', {})
    }


def extract_filters_config(filename=CONFIG_FILE_PATH):
    """
    Extracts filter configuration information from the config file.
    :param filename: The config file.
    :return: A dictionary containing the filter configuration details.
    """
    config = load_config(filename)
    rules = config.get('rules', {})
    filters = rules.get('ai_methods', []) + rules.get('intrusions', [])
    return filters


def extract_cache_config(filename=CONFIG_FILE_PATH):
    """
    Extracts cache configuration information from the config file.
    :param filename: The config file.
    :return: A dictionary containing the cache configuration details.
    """
    config = load_config(filename)
    cache_config = config.get('cache', {})
    return cache_config


class API:
    def __init__(self):
        self.active = False
        self.service = ""
        self.model = ""
        self.api_key = ""
        self.organization = ""
        self.project = ""
        self.base_url = ""
        self.api_version = ""

    def extract_api_config(self, filename=CONFIG_FILE_PATH):
        """
        Extracts API configuration information from the config file.
        :param filename: The name of the config file.
        :return: None
        """
        config = load_config(filename)
        openai_config = config.get('openai', {})
        self.active = openai_config.get('active') if openai_config.get('active') else False
        self.service = openai_config.get('service') if openai_config.get('service') else ""

        openai_config = config.get('openai', {}).get('config', {})
        self.model = openai_config.get('model') if openai_config.get('model') else ""
        self.api_key = openai_config.get('api_key') if openai_config.get('api_key') else ""
        self.organization = openai_config.get('organization') if openai_config.get('organization') else ""
        self.project = openai_config.get('project') if openai_config.get('project') else ""
        self.base_url = openai_config.get('base_url') if openai_config.get('base_url') else ""
        self.api_version = openai_config.get('api_version') if openai_config.get('api_version') else ""
