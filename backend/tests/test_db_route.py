# backend/tests/test_db_routes.py
import json

def test_hello(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data == b"Hello world!!! I'm zhsh aka qwe."

def test_init_db(test_client):
    response = test_client.post('/api/db/init')
    print(response.status_code)  # 打印状态码
    print(response.data)         # 打印响应数据
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert data['status'] == '200'
    assert data['msg'] == 'Database initialized'

def test_create_table(test_client):
    response = test_client.post('/api/db/create', json={'table_name': 'test_table'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == 'Table test_table created'

def test_insert_record(test_client):
    response = test_client.post('/api/db/insert', json={'table_name': 'test_table', 'data': 'test_data'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == 'Record inserted'

def test_query_records(test_client):
    response = test_client.post('/api/db/query', json={'table_name': 'test_table'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert len(data['data']) == 1
    assert data['data'][0]['data'] == 'test_data'

def test_drop_table(test_client):
    table_name = 'test_table2'
    test_client.post('/api/db/create', json={'table_name': table_name})
    response = test_client.post('/api/db/drop', json={'table_name': table_name})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == f'Table {table_name} dropped'
    # Check table_name is dropped or not by querying the table
    response = test_client.post('/api/db/query', json={'table_name': table_name})
    data = json.loads(response.data)
    assert response.status_code == 500

def test_drop_all_tables(test_client):
    table_name = 'test_table3'
    test_client.post('/api/db/create', json={'table_name': table_name})
    response = test_client.post('/api/db/drop_all')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == '200'
    assert data['msg'] == 'All tables dropped'
    # Check table_name is dropped or not by querying the table
    response = test_client.post('/api/db/query', json={'table_name': table_name})
    data = json.loads(response.data)
    assert response.status_code == 500