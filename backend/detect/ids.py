"""
HTTP Intrusion Detection System (IDS) logic should be implemented here.

http_data = {
    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'category': 'Unclassified',
    'source_ip': packet[IP].src,
    'source_port': packet[TCP].sport,
    'destination_ip': packet[IP].dst,
    'destination_port': packet[TCP].dport,
    'request_method': extract_request_method(headers),
    'request_uri': extract_request_uri(headers),
    'http_version': extract_http_version(headers),
    'header_fields': json.dumps(extract_header_fields(headers), ensure_ascii=False),
    'request_body': json.dumps(filter_non_printable(body), ensure_ascii=False)
}
"""

import json
from datetime import datetime

CONFIG_FILE_PATH = 'i_class.json'

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 加载白名单、黑名单和规则
whitelist = set(load_json('ip_whitelist.json'))
blacklist = set(load_json('ip_blacklist.json'))
rules = load_json('rules.json')
i_class = load_json(CONFIG_FILE_PATH)

def match_rules(http_data, rules):
    # 匹配规则
    for rule in rules:
        if all(http_data.get(key) == value for key, value in rule.items()):
            return True
    return False

def log_malicious_traffic(http_data, category):
    http_data['category'] = category
    with open('log.txt', 'a') as log_file:
        log_file.write(json.dumps(http_data) + '\n')

class IDS:
    def __init__(self, whitelist, blacklist, rules, i_class):
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.rules = rules
        self.i_class = i_class

    def is_whitelisted(self, ip):
        # 检查 IP 是否在白名单中
        return ip in self.whitelist

    def is_blacklisted(self, ip):
        # 检查 IP 是否在黑名单中
        return ip in self.blacklist

    def detect(self, http_data):
        source_ip = http_data['source_ip']
        
        # 白名单过滤IP
        if self.is_whitelisted(source_ip):
            return self.i_class["Normal Packets"]
        
        # 黑名单过滤IP
        if self.is_blacklisted(source_ip):
            log_malicious_traffic(http_data, self.i_class["Insecure IPs"])
            return self.i_class["Insecure IPs"]

        # 基于规则的异常检测 TODO
        if match_rules(http_data, self.rules):
            log_malicious_traffic(http_data, self.i_class["CVEs"])
            return self.i_class["CVEs"]

        # 基于 AI-MODEL 的异常检测 TODO
        # url = http_data['request_uri']

        return self.i_class["Unclassified"]


# 初始化 IDS 实例
ids_system = IDS(whitelist, blacklist, rules, i_class)


if __name__ == '__main__':
    # 示例 http_data
    http_data = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'category': 'Unclassified',
        'source_ip': '192.168.1.1',
        'source_port': 12345,
        'destination_ip': '192.168.1.2',
        'destination_port': 80,
        'request_method': 'GET',
        'request_uri': '/index.html',
        'http_version': 'HTTP/1.1',
        'header_fields': json.dumps({'User-Agent': 'Mozilla/5.0'}, ensure_ascii=False),
        'request_body': json.dumps({}, ensure_ascii=False)
    }
    
    # 调用 IDS 检测函数
    result = ids_system.detect(http_data)
    print(result)