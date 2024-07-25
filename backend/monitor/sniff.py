from scapy.all import sniff, IP, TCP, Raw
import requests
import json
import re
import base64
from datetime import datetime
from multiprocessing import Event

# 将项目根目录添加到 sys.path
import sys, os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.detect.ids import *


# 配置全局变量
HOST_URL = 'http://localhost:8001/'
# 配置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
file_handler = logging.FileHandler('monitor/insert.log')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def insert_http_data(http_data):
    # 从api中获得正在使用的表名
    use_api_base_url = HOST_URL + 'api/db'
    data = requests.get(use_api_base_url + '/cur_db').json()
    if data and data.get('table_name'):
        table_name = data['table_name']
    else:
        table_name = 'None'
        return None
    # print(f"Current using table: {table_name}")
    # print(http_data)
    try:
        response = requests.post(use_api_base_url + f'/{table_name}/insert', json=http_data)
        return response
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        return None

def process_packet(packet):
    # print(f"Packet captured: {packet.summary()}") # debug info
    if packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors='ignore')
        http_data = extract_http_data(packet, payload)
        if http_data:
            # print(f"HTTP data to be inserted: {http_data}") # debug info
            
            # ----------------------------------------------------------------------------
            # 在这里调用IDS的逻辑，对http_data进行检测
            i_class = ids_system.detect(http_data) # return IDS class
            http_data['category'] = i_class
            # ----------------------------------------------------------------------------
            
            # 把检测完毕的数据插入数据库
            insert_http_data(http_data) # 不存储和记录response
            # response = insert_http_data(http_data)
            # if response:
            #     # print('[+] Insert success.', response.json()) # debug info
            #     logger.info('Insert success. Response: %s', response.json())

def extract_http_data(packet, payload):
    if "HTTP" in payload:
        headers, _, body = payload.partition('\r\n\r\n')
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
            'request_body': filter_non_printable(body),  # 直接传递处理后的 body # 'request_body': json.dumps(filter_non_printable(body), ensure_ascii=False)
            'raw_packet': base64.b64encode(packet.original).decode('utf-8'),  # Base64 编码后的原始数据包, 用于后续的 export pcap 文件
        }
        if http_data['request_method'] != 'Response': # 响应报文不收集，也可以收集
            return http_data
    return None

def extract_request_method(headers):
    match = re.match(r"^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH|TRACE|CONNECT)", headers)
    # return match.group(0) if match else 'UNKNOWN'
    return match.group(0) if match else 'Response' # 如果上面的请求方法都不是，就是响应报文

def extract_request_uri(headers):
    parts = headers.split()
    return parts[1] if len(parts) > 1 else '/'

def extract_http_version(headers):
    parts = headers.split()
    return parts[2] if len(parts) > 2 else 'HTTP/1.1'

def extract_header_fields(headers):
    header_lines = headers.split('\r\n')[1:]
    header_fields = {}
    for line in header_lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            header_fields[key] = value
    return header_fields

def filter_non_printable(text):
    return ''.join([c if c.isprintable() else '.' for c in text])

def start_sniffing(interface: str, stop_event: Event): # type: ignore
    print(f"Starting sniffing on interface: {interface}")
    # sniff(iface=interface, filter="tcp port 80", prn=process_packet, store=0)
    # sniff(iface=interface, filter="tcp", prn=process_packet, store=0)
    def stop_filter(_):
        return stop_event.is_set()
    
    sniff(iface=interface, filter="tcp", prn=process_packet, stop_filter=stop_filter, store=0)

if __name__ == '__main__':
    start_sniffing('eth0')