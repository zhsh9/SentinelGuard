# backend/tests/test_db_routes.py
import json
from datetime import datetime

# 获取当前时间
now = datetime.now()
# 格式化为指定的字符串格式
timestamp = now.strftime("%Y%m%d%H%M%S")
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data == b"Hello world!!! I'm zhsh aka qwe."

def test_init_db(test_client):
    response = test_client.post('/api/db/drop_all')
    response = test_client.post('/api/db/init')
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert data['status'] == '200'
    assert data['msg'] == 'Database initialized'

def test_create_table(test_client):
    response = test_client.post('/api/db/create_table', json={'time': formatted_time})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert f'Table {timestamp} created successfully' in data['message']

def test_insert_record(test_client):
    test_client.post('/api/db/create_table', json={'timestamp': timestamp})
    record_data = {
        'table_name': timestamp,
        'category': 'test_category',
        'source_ip': '192.168.1.1',
        'source_port': 12345,
        'destination_ip': '192.168.1.2',
        'destination_port': 80,
        'request_method': 'GET',
        'request_uri': '/test',
        'http_version': 'HTTP/1.1',
        'header_fields': json.dumps({'Test': 'header'}),
        'request_body': json.dumps({'Test': 'body'})
    }
    response = test_client.post('/api/db/insert', json=record_data)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == 'Record inserted'

def test_query_records(test_client):
    test_client.post('/api/db/create_table', json={'timestamp': timestamp})
    record_data = {
        'table_name': timestamp,
        'category': 'test_category',
        'source_ip': '192.168.1.1',
        'source_port': 12345,
        'destination_ip': '192.168.1.2',
        'destination_port': 80,
        'request_method': 'GET',
        'request_uri': '/test',
        'http_version': 'HTTP/1.1',
        'header_fields': json.dumps({'Test': 'header'}),
        'request_body': json.dumps({'Test': 'body'})
    }
    test_client.post('/api/db/insert', json=record_data)
    response = test_client.post('/api/db/query', json={'table_name': 'http_request_log_20240709'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert len(data['data']) > 0  # Assuming there are records in the database

def test_drop_table(test_client):
    cur_timestamp = str(int(time.time()))
    test_client.post('/api/db/create_table', json={'timestamp': cur_timestamp})
    response = test_client.post('/api/db/drop', json={'table_name': cur_timestamp})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert f'Table {cur_timestamp} dropped' in data['msg']
    # Check table is dropped or not by querying the table
    response = test_client.post('/api/db/query', json={'table_name': cur_timestamp})
    assert response.status_code == 500

def test_drop_all_tables(test_client):
    cur_timestamp = str(int(time.time()))
    test_client.post('/api/db/create_table', json={'timestamp': cur_timestamp})
    response = test_client.post('/api/db/drop_all')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == 'All tables dropped'
    # Check tables are dropped or not by querying
    response = test_client.post('/api/db/query', json={'table_name': cur_timestamp})
    assert response.status_code == 500