from config import extract_server_config


def process_config(file_path, config_path='../config.yaml'):
    """
    Processes the server configuration based on the server type specified in the config file.

    :param file_path: Path to the server configuration file to be processed.
    :param config_path: Path to the ids configuration file.
    """
    config = extract_server_config(config_path)

    if config['server'] == 'apache':
        processed_content = process_apache_config(file_path)
        print(processed_content)
    else:
        print(f"No processing function available for server type: {config['server']}")


def process_apache_config(file_path):
    """
    Processes an Apache configuration file by removing all comments and empty lines.

    :param file_path: Path to the Apache configuration file.
    :return: A string containing the processed configuration without comments and empty lines.
    """
    processed_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            # Ignore empty lines and comments
            if stripped_line and not stripped_line.startswith('#'):
                processed_lines.append(stripped_line)

    return "\n".join(processed_lines)
