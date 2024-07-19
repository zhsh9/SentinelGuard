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

import os
import json
from datetime import datetime
import re
import ipaddress

CONFIG_FILE_PATH = 'i_class.json'

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建绝对路径
whitelist_path = os.path.join(current_dir, 'ip_whitelist.json')
blacklist_path = os.path.join(current_dir, 'ip_blacklist.json')
rules_path = os.path.join(current_dir, 'rules.json')
i_class_path = os.path.join(current_dir, CONFIG_FILE_PATH)

# 加载 JSON 文件
whitelist = set(load_json(whitelist_path))
blacklist = set(load_json(blacklist_path))
rules = load_json(rules_path)
i_class = load_json(i_class_path)

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
        
        # 是否使用对应的模块
        self.whitelist_on = True
        self.blacklist_on = True
        self.rules_on = True
        self.ai_on = True

    def is_whitelisted(self, ip):
        # 检查 IP 是否在白名单中，支持正则表达式，支持子网格式
        return self._match_ip(ip, self.whitelist)

    def is_blacklisted(self, ip):
        # 检查 IP 是否在黑名单中，支持正则表达式，支持子网格式
        return self._match_ip(ip, self.blacklist)

    def _match_ip(self, ip, ip_list):
        for pattern in ip_list:
            if self._ip_matches_pattern(ip, pattern):
                return True
        return False

    def _ip_matches_pattern(self, ip, pattern):
        # 支持子网掩码格式
        if '/' in pattern:
            try:
                network = ipaddress.ip_network(pattern, strict=False)
                if ipaddress.ip_address(ip) in network:
                    return True
            except ValueError:
                return False
        # 支持正则表达式
        else:
            regex_pattern = pattern.replace('*', '.*')
            if re.match(f'^{regex_pattern}$', ip):
                return True
        return False

    def detect(self, http_data):
        source_ip = http_data['source_ip']
        ret_flag = i_class["Unclassified"]
        
        # 白名单过滤IP
        if self.whitelist_on and self.is_whitelisted(source_ip):
            ret_flag = self.i_class["Normal Packets"]

        # 黑名单过滤IP
        if self.blacklist_on and self.is_blacklisted(source_ip):
            log_malicious_traffic(http_data, self.i_class["Insecure IPs"])
            ret_flag = self.i_class["Insecure IPs"]
            return ret_flag

        # 基于规则的异常检测 TODO
        if self.rules_on and match_rules(http_data, self.rules):
            log_malicious_traffic(http_data, self.i_class["CVEs"])
            ret_flag = self.i_class["CVEs"]
            return ret_flag

        # 基于 AI-MODEL 的异常检测 TODO
        # url = http_data['request_uri']

        return ret_flag


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
