from scapy.all import sniff, IP, TCP, Raw, AsyncSniffer, wrpcap, Ether
import requests
import json
import re
import base64
from datetime import datetime
import time

# 将项目根目录添加到 sys.path
import sys, os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.detect.ids import *


# 配置全局变量
HOST_URL = 'http://localhost:8001/'
PCAP_SAVE_DIR_NAME = 'pcap'
# 如果文件夹不存在则创建
PCAP_SAVE_DIR = os.path.join(os.path.dirname(__file__), PCAP_SAVE_DIR_NAME)
os.makedirs(PCAP_SAVE_DIR, exist_ok=True)
# 配置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
current_dir = os.path.dirname(__file__)
log_file_path = os.path.join(current_dir, 'insert.log')
file_handler = logging.FileHandler(log_file_path)
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

def filter_generator(port_list=[]):
    if type(port_list) != list or len(port_list) == 0: # 不合法的输入，或者没有指定端口
        return "tcp"
    port_list = sorted([int(p) for p in port_list if str(p).isdigit()]) # 过滤掉非数字的端口
    ret_filter = []
    for port in port_list:
        ret_filter.append(f"tcp port {port}")
    return " or ".join(ret_filter)

def generate_sniffing(interface_list=[], port_list=[]) -> AsyncSniffer:
    # Generate the filter string based on the port list
    filter_str = filter_generator(port_list)
    
    if len(interface_list) == 0:
        interface = None
    else:
        interface = interface_list

    # print(f"Starting sniffing on interfaces: {interface}; fileter: {filter_str}")
    return AsyncSniffer(iface=interface, filter=filter_str, prn=process_packet, store=True)
    # sniff(iface=interface, filter=filter_str, prn=process_packet, stop_filter=stop_sniff, store=0) # old version

def start_sniffing(sniffer: AsyncSniffer) -> bool:
    try:
        sniffer.start()
        return True
    except Exception as e:
        logger.error('Error: %s', e)
        return False

def stop_sniffing(sniffer: AsyncSniffer) -> bool:
    try:
        # 停止嗅探
        sniffer.stop()
        # 获取捕获到的所有数据包
        packets = sniffer.results

        # 检查捕获到的数据包数量
        logger.info(f"Number of packets captured: {len(packets)}")

        # 过滤掉 NoneType 数据包
        filtered_packets = [pkt for pkt in packets if pkt is not None]

        # 检查过滤后的数据包数量
        logger.info(f"Number of valid packets: {len(filtered_packets)}")

        # 检查是否有数据包
        if filtered_packets:
            # 获取第一个数据包的链路层类型
            first_packet = filtered_packets[0]
            if isinstance(first_packet, Ether):
                linktype = 1  # Ethernet
            else:
                linktype = None  # 其他类型，可以根据需要设置

            # 将捕获到的数据包写入 pcap 文件
            pcap_file = f'{PCAP_SAVE_DIR}/{int(time.time())}.pcap'
            logger.info(f"Captured packets saved to {pcap_file}")

            # 指定链路层类型
            wrpcap(pcap_file, filtered_packets, linktype=linktype)
        else:
            logger.error("No valid packets to write.")
        
        return True
    except Exception as e:
        logger.error('Error: %s', e)
        return False

def analyse_pcap(filename: str, port_list=[]) -> None:
    filter_str = filter_generator(port_list)
    print(f"Analyzing sniffed data from file: {filename}")
    
    # 创建 AsyncSniffer 实例
    sniffer = AsyncSniffer(offline=filename, filter=filter_str, prn=process_packet, store=0)
    
    # 开始嗅探（读取 pcap 文件）
    sniffer.start()
    logger.info("Analyzing pcap file...")
    # 等待完成
    sniffer.join()
    logger.info("Analysis completed.")

if __name__ == '__main__':
    # 创建 AsyncSniffer 实例
    sniffer = generate_sniffing()
    sniffer.start()
    time.sleep(10)
    
    # 停止嗅探
    sniffer.stop()

    # 获取捕获到的所有数据包
    packets = sniffer.results

    # 将捕获到的数据包写入 pcap 文件
    pcap_file = f'{int(time.time())}.pcap'
    wrpcap(pcap_file, packets)

    print(f"Captured packets saved to {pcap_file}")
