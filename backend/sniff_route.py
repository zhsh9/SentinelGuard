"""
API for scapy - sniff, capture network packets
- /api/sniffer/start: Start a new process to run the start_sniffing function.
- /api/sniffer/stop: Modify the value of the shared variable and wait for the sniffing process to terminate.
- /api/sniffer/status: Return the current sniffing status.
"""

from flask import Flask, request, jsonify
from multiprocessing import Process, Event
import time
from app import app
import monitor.sniff as sniff
import monitor.interface as interface
from copy import deepcopy

# 使用Event来共享状态变量
is_sniffing = app.config['IS_SNIFFING'] = Event()
sniffing_process = app.config['SNIFFING_PROCESS'] = None

def start_sniffing(stop_event, interface_list=[], port_list=[]):
    stop_event.clear()
    sniff.start_sniffing(stop_event, interface_list, port_list)
    # 测试 Event 是否正常工作
    # while not stop_event.is_set():
    #     time.sleep(1)
    #     print(f"[!] Sniffing on interface {interface}...")

def stop_sniffing(stop_event):
    stop_event.set()

@app.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    global is_sniffing, sniffing_process
    if sniffing_process and sniffing_process.is_alive():
        return jsonify({'status': 'error', 'message': 'Sniffer is already running'}), 400
    interface_list = deepcopy(request.json.get('interface_list', []))
    port_list = deepcopy(request.json.get('port_list', []))
    print(f'interface_list: {interface_list}, port_list: {port_list}')
    sniffing_process = Process(target=start_sniffing, args=(is_sniffing, interface_list, port_list))
    sniffing_process.start()
    return jsonify({'status': 'success', 'message': f'Sniffer started on interface {interface}'}), 200

@app.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    global is_sniffing, sniffing_process
    if not sniffing_process or not sniffing_process.is_alive():
        return jsonify({'status': 'error', 'message': 'Sniffer is not running'}), 400
    stop_sniffing(is_sniffing)
    sniffing_process.join()
    return jsonify({'status': 'success', 'message': 'Sniffer stopped'}), 200

@app.route('/api/sniffer/status', methods=['GET'])
def sniffer_status():
    # 展示是否在嗅探
    # TODO 展示嗅探的数据包的所有summary
    if sniffing_process and sniffing_process.is_alive():
        return jsonify({'sniffing': True}), 200
    else:
        return jsonify({'sniffing': False}), 200

@app.route('/api/sniffer/interfaces', methods=['GET'])
def get_interfaces():
    interfaces: list = interface.get_alive_interface()
    return jsonify(interfaces), 200
