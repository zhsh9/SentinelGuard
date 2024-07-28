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
from monitor.sniff import generate_sniffing, start_sniffing, stop_sniffing, analyse_pcap
import monitor.interface as interface
from copy import deepcopy
import gc


@app.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    sniffer = app.config['SNIFFER']
    
    # Sniffer is already running
    if sniffer is not None and sniffer.running:
        return jsonify({'status': 'error', 'message': 'Sniffer is already running'}), 400
    
    # Retrieve the interface and port list from the request
    interface_list = deepcopy(request.json.get('interface_list', []))
    port_list = deepcopy(request.json.get('port_list', []))
    
    # Generate and start the sniffer
    sniffer = app.config['SNIFFER'] = generate_sniffing(interface_list, port_list)
    is_done = start_sniffing(sniffer)

    # Update the shared variables
    if is_done:
        return jsonify({'status': 'success', 'message': f'Sniffer started on interface: {interface_list}, port: {port_list}'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to start sniffer'}), 400

@app.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    sniffer = app.config['SNIFFER']
    
    # Sniffer is not running
    if sniffer is None or not sniffer.running:
        return jsonify({'status': 'error', 'message': 'Sniffer is not running'}), 400

    # Stop the sniffer
    is_done = stop_sniffing(sniffer)
    if is_done:
        # Delete the reference to the sniffer and run the garbage collector to delete the instance of the sniffer
        del sniffer
        gc.collect()
        
        # Update the shared variables
        sniffer = app.config['SNIFFER'] = None
        return jsonify({'status': 'success', 'message': 'Sniffer stopped'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to stop sniffer'}), 400

@app.route('/api/sniffer/status', methods=['GET'])
def sniffer_status():
    sniffer = app.config['SNIFFER']

    # 展示是否在嗅探
    if sniffer is not None and sniffer.running:
        return jsonify({'sniffing': True}), 200
    else:
        return jsonify({'sniffing': False}), 200

@app.route('/api/sniffer/interfaces', methods=['GET'])
def get_interfaces():
    interfaces: list = interface.get_alive_interface()
    return jsonify(interfaces), 200

@app.route('/api/upload-pcap', methods=['POST'])
def upload_pcap():
    if 'pcapFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pcapFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 保存文件并进行分析
        filename = f"{app.config['PCAP_SAVE_DIR']}/{file.filename}"
        file.save(filename)
        analyse_pcap(filename)
        
        return jsonify({'success': 'File uploaded and analysed successfully!'}), 200
