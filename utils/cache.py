from flask import current_app
from config import extract_cache_config
import json
import logging
import os


def cache_write(log_record: dict) -> None:
    cache_config = extract_cache_config()
    if cache_config['activate']:
        cache_path = cache_config['path']
    else:
        logging.error(f"[!] Cache function is disabled.")
        return

    # Ensure the directory exists
    cache_dir = os.path.dirname(cache_path)
    if not os.path.exists(cache_dir):
        try:
            os.makedirs(cache_dir)
        except OSError as e:
            logging.error(f"[!] Failed to create directory {cache_dir}: {e}")
            return

    # Convert the log record to a JSON string
    #   e.g. {'remote_host': '127.0.0.1', 'log_name': '-', 'remote_user': '-', 'time': '29/May/2024:04:59:19 +0800',
    #   'request': 'GET / HTTP/1.1', 'status': 200, 'bytes': 10956, 'referer': '-', 'user_agent': 'curl/8.5.0',
    #   'tag': {'LLM': True, 'SQL_INJECTION': False}}
    log_record_json = json.dumps(log_record)

    # Write the JSON string to the cache file
    try:
        with open(cache_path, 'a') as file:
            file.write(log_record_json + '\n')
    except IOError as e:
        logging.error(f"[!] Failed to write to cache file {cache_path}: {e}")


def cache_read() -> list[dict]:
    """
    Read cache based on file path in config.yaml
    :return: A list of dict converted from json strings.
    """
    # if current_app.config['cache']['activate']:
    #     cache_path = current_app.config['cache']['path']
    # else:
    #     logging.error(f"[!] Cache function is disabled.")
    #     cache_path = ""
    cache_config = extract_cache_config()
    if cache_config['activate']:
        cache_path = cache_config['path']
    else:
        logging.error(f"[!] Cache function is disabled.")
        cache_path = ""

    cache_dicts = []
    try:
        with open(cache_path, 'r') as file:
            cache = file.readlines()
        # Convert json string into dict
        for c in cache:
            cache_dicts.append(json.loads(c))
    except Exception as e:
        logging.error(f"Error reading cache file: {e}")
        # raise e
    return cache_dicts


# if __name__ == '__main__':
#     import pprint
#     cache = cache_read()
#     pprint.pprint(cache)
#     print(type(cache[0]))
