import unittest
from utils.log_parse import parse_apache_log_line, parse_log_line
from config import load_config


class TestApacheLogParsing(unittest.TestCase):
    def test_parse_apache_log_line(self):
        # Example: Apache log record
        apache_log_line = ('127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 '
                           '"https://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I)"')

        expected_output = {
            'remote_host': '127.0.0.1',
            'log_name': '-',
            'remote_user': 'frank',
            'time': '10/Oct/2000:13:55:36 -0700',
            'request': 'GET /apache_pb.gif HTTP/1.0',
            'status': 200,
            'bytes': 2326,
            'referer': 'https://www.example.com/start.html',
            'user_agent': 'Mozilla/4.08 [en] (Win98; I)'
        }

        # Load config
        config = load_config('../config.yaml')

        # Unit test
        result = parse_apache_log_line(apache_log_line, config)
        self.assertEqual(result, expected_output)

    def test_parse_log_line(self):
        # Example: Apache log record
        apache_log_line = '127.0.0.1 - - [29/May/2024:04:59:19 +0800] "GET / HTTP/1.1" 200 10956 "-" "curl/8.5.0"'

        expected_output = {
            'remote_host': '127.0.0.1',
            'log_name': '-',
            'remote_user': '-',
            'time': '29/May/2024:04:59:19 +0800',
            'request': 'GET / HTTP/1.1',
            'status': 200,
            'bytes': 10956,
            'referer': '-',
            'user_agent': 'curl/8.5.0'
        }

        # Load config
        config = load_config('../config.yaml')

        # Unit test
        result = parse_log_line(apache_log_line, config)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
