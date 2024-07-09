from app import app, db
from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# API: Initialize the database
@app.route('/api/db/init', methods=['GET', 'POST'])
def init_db():
    try:
        db.create_all()
        return jsonify({'status': '200', 'msg': 'Database initialized'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Create a new table
@app.route('/api/db/create', methods=['POST'])
def create_table():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    try:
        query = text(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        )
        ''')
        db.session.execute(query)
        db.session.commit()
        return jsonify({'status': '200', 'msg': f'Table {table_name} created'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Insert a record into a table
@app.route('/api/db/insert', methods=['POST'])
def insert_record():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    table_name = request.json.get('table_name')
    data = request.json.get('data')

    if not table_name or not data:
        return jsonify({'error': 'Missing table name or data'}), 400

    try:
        query = text(f'''
        INSERT INTO {table_name} (data) VALUES (:data)
        ''')
        db.session.execute(query, {'data': data})
        db.session.commit()
        return jsonify({'status': '200', 'msg': 'Record inserted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Query records from a table
@app.route('/api/db/query', methods=['POST'])
def query_records():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    try:
        query = text(f'SELECT * FROM {table_name}')
        result = db.session.execute(query)
        records = [dict(row._mapping) for row in result]  # 使用 _mapping 将行转换为字典
        return jsonify({'status': '200', 'data': records}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Drop a table
@app.route('/api/db/drop', methods=['POST'])
def drop_table():
    table_name = request.json.get('table_name')
    if not table_name:
        return jsonify({'error': 'Missing table name'}), 400

    try:
        query = text(f'DROP TABLE IF EXISTS {table_name}')
        db.session.execute(query)
        db.session.commit()
        return jsonify({'status': '200', 'msg': f'Table {table_name} dropped'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Drop all tables
@app.route('/api/db/drop_all', methods=['POST'])
def drop_all_tables():
    try:
        db.reflect()  # Reflect the database schema to SQLAlchemy
        db.drop_all()  # Drop all reflected tables
        db.session.commit()  # Commit the transaction
        return jsonify({'status': '200', 'msg': 'All tables dropped'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500