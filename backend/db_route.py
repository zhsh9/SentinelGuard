from app import app, db
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from database.model import *
from sqlalchemy import inspect

"""
tables: maintain all tables created in the database
{
    'formatted_time1': {
        'class': HttpRequestLog_20210901120000,
        'table_name': 'http_request_log_20210901120000',
        'using': True,
    },
    'formatted_time2': {
        'class': HttpRequestLog_20220901120000,
        'table_name': 'http_request_log_20220901120000',
        'using': False,
    },
}
"""
tables = {}

# Init: check existing tables in the database -> tables

# API: Initialize the database
@app.route('/api/db/init', methods=['GET', 'POST'])
def init_db():
    try:
        # 使用 inspect 来检查数据库是否已经初始化
        inspector = inspect(db.engine)
        if inspector.has_table('http_request_log'):
            return jsonify({'status': '200', 'msg': 'Database is already initialized'}), 200
        
        # 创建所有表
        db.create_all()
        return jsonify({'status': '200', 'msg': 'Database initialized'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Create a new table for HttpRequestLog based on time
@app.route('/api/db/create_table', methods=['POST'])
def create_table():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.json
    time = data.get('time')
    if not time:
        return jsonify({'error': 'Time is required'}), 400
    
    try:
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        new_table, table_name = create_dynamic_http_request_log_class(time)
        
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            # 创建表
            tables[time] = {
                'class': new_table,
                'table_name': table_name,
                'using': True,
            }
            tables[time]['class'].__table__.create(db.engine)
            return jsonify({'status': '200', 'message': f'Table {table_name} created successfully'}), 200
        else:
            return jsonify({'status': '200', 'message': f'Table {table_name} already exists'}), 200
        
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': 'Invalid time format. Expected format: YYYY-MM-DD HH:MM:SS'}), 400

def is_valid_datetime_format(date_string):
    try:
        # 尝试解析字符串为日期时间对象
        datetime.strptime(date_string, app.config['SQL_TIME_FORMAT'])
        return True
    except ValueError:
        # 如果解析失败，抛出 ValueError 异常
        return False

# API: Insert a record into HttpRequestLog table
@app.route('/api/db/insert', methods=['POST'])
def insert_record():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.json
    table_name = data.get('table_name')
    time = table_name.split('_')[-1]

    if not table_name or time not in tables or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    required_fields = [
        'category', 'source_ip', 'source_port', 'destination_ip', 'destination_port',
        'request_method', 'request_uri', 'http_version', 'header_fields'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        table_cls = tables[time]['class']
        if table_cls is None:
            return jsonify({'error': 'Table class not found'}), 500
        
        # 检查 time 的格式是否正确
        time = data.get('time', None)
        if time is None or not is_valid_datetime_format(time):
            time = datetime.now().strftime(app.config['SQL_TIME_FORMAT'])
        
        record = table_cls(
            category=data['category'],
            source_ip=data['source_ip'],
            source_port=data['source_port'],
            destination_ip=data['destination_ip'],
            destination_port=data['destination_port'],
            time=time,
            request_method=data['request_method'],
            request_uri=data['request_uri'],
            http_version=data['http_version'],
            header_fields=data['header_fields'],
            request_body=data.get('request_body')
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'status': '200', 'msg': 'Record inserted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Query records from HttpRequestLog table
@app.route('/api/db/query', methods=['POST'])
def query_records():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.json
    table_name = data.get('table_name')
    time = table_name.split('_')[-1]
    
    if not table_name or time not in tables or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name'}), 400

    try:
        table_cls = tables[time]['class']
        if table_cls is None:
            return jsonify({'error': 'Table class not found'}), 500
        
        records = db.session.query(table_cls).all()
        result = [
            {
                'id': record.id,
                'category': record.category,
                'source_ip': record.source_ip,
                'source_port': record.source_port,
                'destination_ip': record.destination_ip,
                'destination_port': record.destination_port,
                'time': record.time,
                'request_method': record.request_method,
                'request_uri': record.request_uri,
                'http_version': record.http_version,
                'header_fields': record.header_fields,
                'request_body': record.request_body
            } for record in records
        ]
        return jsonify({'status': '200', 'data': result}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# API: Drop HttpRequestLog table
@app.route('/api/db/drop', methods=['POST'])
def drop_table():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    table_name = request.json.get('table_name')
    time = table_name.split('_')[-1]

    if not table_name or time not in tables or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name'}), 400

    try:
        table_cls = tables[time]['class']
        if table_cls is None:
            return jsonify({'error': 'Table class not found'}), 500
        
        table_cls.__table__.drop(db.engine)
        del tables[time]
        db.session.commit()
        return jsonify({'status': '200', 'msg': f'Table {app.config['SQL_TABLE_NAME_PREFIX']}{table_name} dropped'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: Drop all tables
@app.route('/api/db/drop_all', methods=['GET', 'POST'])
def drop_all_tables():
    try:
        db.reflect()  # Reflect the database schema to SQLAlchemy
        db.drop_all()  # Drop all reflected tables
        db.session.commit()  # Commit the transaction
        tables.clear()
        return jsonify({'status': '200', 'msg': 'All tables dropped'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# API: 定义查看所有表名的 API 端点
@app.route('/api/db/tables', methods=['GET'])
def list_tables():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

# API: 定义正在使用的表名 using=True