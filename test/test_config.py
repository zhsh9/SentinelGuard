from config import *


if __name__ == '__main__':
    config_path = '../config.yaml'

    # config = extract_server_config(config_path)
    # print(config)

    # api = API()
    # api.extract_api_config(config_path)
    # print(api.active, api.service, api.model, api.api_key, api.organization, api.project, api.base_url, api.api_version)

    filters = extract_filters_config(config_path)
    print(filters)
