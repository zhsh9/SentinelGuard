from app import app, db
from flask import jsonify, request

# API: Initialize the database
@app.route('/api/db/init', methods=['POST'])
def init_db():
    db.create_all()
    return jsonify({'status': '200', 'msg': 'Database initialized'}), 200

# API: Create a new table
@app.route('/api/db/create', methods=['POST'])
def create_table():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        data TEXT NOT NULL
    )
    '''
    db.engine.execute(query)
    return jsonify({'status': '200', 'msg': f'Table {table_name} created'}), 200

# API: Insert a record into a table
@app.route('/api/db/insert', methods=['POST'])
def insert_record():
    table_name = request.json.get('table_name')
    data = request.json.get('data')
    if not table_name or not data:
        return jsonify({'error': 'Missing table name or data'}), 400

    query = f'''
    INSERT INTO {table_name} (data) VALUES (:data)
    '''
    db.engine.execute(query, {'data': data})
    return jsonify({'status': '200', 'msg': 'Record inserted'}), 200

# API: Query records from a table
@app.route('/api/db/query', methods=['POST'])
def query_records():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    query = f'SELECT * FROM {table_name}'
    result = db.engine.execute(query)
    records = [dict(row) for row in result]
    return jsonify({'status': '200', 'data': records}), 200

# API: Drop a table
@app.route('/api/db/drop', methods=['POST'])
def drop_table():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    query = f'DROP TABLE IF EXISTS {table_name}'
    db.engine.execute(query)
    return jsonify({'status': '200', 'msg': f'Table {table_name} dropped'}), 200

# API: Drop all tables
@app.route('/api/db/drop_all', methods=['POST'])
def drop_all_tables():
    db.drop_all()
    return jsonify({'status': '200', 'msg': 'All tables dropped'}), 200
