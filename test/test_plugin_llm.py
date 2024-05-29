from flask import current_app
from utils.plugin.llm import LLM  # Assuming the above code is saved as llm.py


if __name__ == '__main__':
    # Configure the OpenAI API's base URL and API version

    # Simulated log record
    log_record = {
        'remote_host': '192.168.1.1',
        'log_name': '-',
        'remote_user': 'john_doe',
        'time': '29/May/2024:12:00:00 +0000',
        'request': 'GET /index.html HTTP/1.1',
        'status': 200,
        'bytes': 1234,
        'referer': 'http://example.com',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    # Create an instance of the LLM class
    llm_instance = LLM(context="", prompt="", config_path='../config.yaml')

    # Call the detect method to perform detection
    result = llm_instance.detect(log_record)

    # Output the detection result
    print(f"[!] Detection result: {result}")

    # Add logic for further processing based on the detection result
    if result:
        print("[*] Potential intrusion detected!")
    else:
        print("[*] No intrusion detected.")
