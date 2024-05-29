from utils.log_load import monitor_log_file
from utils.log_parse import parse_log_line


if __name__ == '__main__':
    file_name = '/tmp/var/log/apache2/access.log'
    log_gen = monitor_log_file(file_name, parse_log_line)
    while True:
        log_dict = next(log_gen)
        print(log_dict)
