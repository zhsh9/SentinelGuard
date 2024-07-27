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
from monitor.sniff import generate_sniffing, start_sniffing, stop_sniffing
import monitor.interface as interface
from copy import deepcopy
import gc


@app.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    is_sniffing = app.config['IS_SNIFFING']
    sniffer = app.config['SNIFFER']
    
    # Sniffer is already running
    if is_sniffing and sniffer is not None:
        return jsonify({'status': 'error', 'message': 'Sniffer is already running'}), 400
    
    # Retrieve the interface and port list from the request
    interface_list = deepcopy(request.json.get('interface_list', []))
    port_list = deepcopy(request.json.get('port_list', []))
    
    # Generate and start the sniffer
    is_sniffing = app.config['IS_SNIFFING'] = True
    sniffer = app.config['SNIFFER'] = generate_sniffing(interface_list, port_list)
    is_done = start_sniffing(sniffer)

    # Update the shared variables
    if is_done:
        return jsonify({'status': 'success', 'message': f'Sniffer started on interface: {interface_list}, port: {port_list}'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to start sniffer'}), 400

@app.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    is_sniffing = app.config['IS_SNIFFING']
    sniffer = app.config['SNIFFER']
    
    # Sniffer is not running
    if not is_sniffing or sniffer is None:
        return jsonify({'status': 'error', 'message': 'Sniffer is not running'}), 400

    # Stop the sniffer
    is_done = stop_sniffing(sniffer)
    if is_done:
        # Delete the reference to the sniffer and run the garbage collector to delete the instance of the sniffer
        del sniffer
        gc.collect()
        
        # Update the shared variables
        is_sniffing = app.config['IS_SNIFFING'] = False
        sniffer = app.config['SNIFFER'] = None
        return jsonify({'status': 'success', 'message': 'Sniffer stopped'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to stop sniffer'}), 400

@app.route('/api/sniffer/status', methods=['GET'])
def sniffer_status():
    is_sniffing = app.config['IS_SNIFFING']
    sniffer = app.config['SNIFFER']

    # 展示是否在嗅探
    if is_sniffing and sniffer is not None:
        return jsonify({'sniffing': True}), 200
    else:
        return jsonify({'sniffing': False}), 200

@app.route('/api/sniffer/interfaces', methods=['GET'])
def get_interfaces():
    interfaces: list = interface.get_alive_interface()
    return jsonify(interfaces), 200
