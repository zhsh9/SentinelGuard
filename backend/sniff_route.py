"""
API for scapy - sniff, capture network packets
- /api/sniffer/start: Start a new process to run the start_sniffing function.
- /api/sniffer/stop: Modify the value of the shared variable and wait for the sniffing process to terminate.
- /api/sniffer/status: Return the current sniffing status.
"""

from flask import Flask, request, jsonify
from multiprocessing import Process, Value
import time
from app import app
import detect

# 使用Value来共享状态变量
is_sniffing = app.config['IS_SNIFFING'] = Value('b', False)
sniffing_process = app.config['SNIFFING_PROCESS'] = None

def start_sniffing(interface, is_sniffing):
    with is_sniffing.get_lock():
        is_sniffing.value = True
    while is_sniffing.value:
        # 在这里添加你的嗅探逻辑
        print(f"[!] Start sniffing: interface - {interface}...")
        time.sleep(100)  # 模拟嗅探工作

def stop_sniffing(is_sniffing):
    with is_sniffing.get_lock():
        is_sniffing.value = False

@app.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    global is_sniffing, sniffing_process
    if sniffing_process and sniffing_process.is_alive():
        return jsonify({'status': 'error', 'message': 'Sniffer is already running'}), 400
    interface = request.json.get('interface', 'eth0')
    sniffing_process = Process(target=start_sniffing, args=(interface, is_sniffing))
    sniffing_process.start()
    return jsonify({'status': 'success', 'message': f'Sniffer started on interface {interface}'}), 200

@app.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    global is_sniffing, sniffing_process
    if not is_sniffing.value:
        return jsonify({'status': 'error', 'message': 'Sniffer is not running'}), 400
    stop_sniffing(is_sniffing)
    sniffing_process.join()
    return jsonify({'status': 'success', 'message': 'Sniffer stopped'}), 200

@app.route('/api/sniffer/status', methods=['GET'])
def sniffer_status():
    # 展示是否在嗅探
    # TODO 展示嗅探的数据包的所有summary
    return jsonify({'sniffing': is_sniffing.value}), 200
