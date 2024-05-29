import re


def parse_apache_log_line(log_line, config):
    log_pattern = (
        r'(?P<remote_host>\S+) '   # %h
        r'(?P<log_name>\S*) '      # %l
        r'(?P<remote_user>\S*) '   # %u
        r'\[(?P<time>.*?)\] '      # %t
        r'"(?P<request>.*?)" '     # "%r"
        r'(?P<status>\d{3}) '      # %>s
        r'(?P<bytes>\S+) '         # %b
        r'"(?P<referer>.*?)" '     # "%{Referer}i"
        r'"(?P<user_agent>.*?)"'   # "%{User-Agent}i"
    )

    match = re.match(log_pattern, log_line)
    if not match:
        raise ValueError("Log line does not match pattern")

    log_dict = match.groupdict()

    # Based on the field type to convert into value.
    for field in config['apache']['fields']:
        name = field['name']
        field_type = field['type']
        if field_type == 'integer':
            log_dict[name] = int(log_dict[name]) if log_dict[name].isdigit() else 0
        elif field_type == 'string':
            log_dict[name] = str(log_dict[name])

    return log_dict


def parse_nginx_log_line(log_line, config):
    log_pattern = (
        r'(?P<remote_addr>\S+) '       # $remote_addr
        r'- (?P<remote_user>\S*) '     # $remote_user
        r'\[(?P<time_local>.*?)\] '    # [$time_local]
        r'"(?P<request>.*?)" '         # "$request"
        r'(?P<status>\d{3}) '          # $status
        r'(?P<body_bytes_sent>\S+) '   # $body_bytes_sent
        r'"(?P<http_referer>.*?)" '    # "$http_referer"
        r'"(?P<http_user_agent>.*?)"'  # "$http_user_agent"
    )

    match = re.match(log_pattern, log_line)
    if not match:
        raise ValueError("Log line does not match pattern")

    log_dict = match.groupdict()

    # Based on the field type to convert into value.
    for field in config['nginx']['fields']:
        name = field['name']
        field_type = field['type']
        if field_type == 'integer':
            log_dict[name] = int(log_dict[name]) if log_dict[name].isdigit() else 0
        elif field_type == 'string':
            log_dict[name] = str(log_dict[name])

    return log_dict


def parse_iis_log_line(log_line, config):
    # IIS log fields will be separated by spaces
    fields = log_line.split()

    if fields[0] == '#Fields:':
        raise ValueError("Log line is a header field line, not a data line")

    if len(fields) != len(config['iis']['fields']):
        raise ValueError("Log line does not match pattern")

    log_dict = {}

    for i, field in enumerate(config['iis']['fields']):
        name = field['name']
        field_type = field['type']
        value = fields[i]
        if field_type == 'integer':
            log_dict[name] = int(value) if value.isdigit() else 0
        elif field_type == 'string':
            log_dict[name] = str(value)

    return log_dict


def parse_log_line(log_line, config):
    server_type = config['server']
    if server_type == 'apache':
        return parse_apache_log_line(log_line, config)
    elif server_type == 'nginx':
        return parse_nginx_log_line(log_line, config)
    elif server_type == 'iis':
        return parse_iis_log_line(log_line, config)
    else:
        raise ValueError(f"Unsupported server type: {server_type}")
