"""
API for database operations
- /api/db/init: 初始化数据库和环境变量
- /api/db/create: 创建表
- /api/db/use: 切换表
- /api/db/drop: 删除表
- /api/db/drop_all: 删除所有表
- /api/db/info: 列出所有表，以及表环境变量
- /api/db/<table_name>/info: 获取表的信息
- /api/db/<table_name>/insert: 插入数据
- /api/db/<table_name>/select: 查询数据
- /api/db/<table_name>/delete: 删除数据
- /api/db/<table_name>/clean: 清空表
"""
import json
from app import app, db
from flask import jsonify, request
from datetime import datetime
from database.model import *
import requests
# 数据库操作
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData, inspect, select, func, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

"""
tables: maintain all tables created in the database
{
    'formatted_time1': {
        'table_name': 'http_request_log_20210901120000',
        'using': True,
    },
    'formatted_time2': {
        'table_name': 'http_request_log_20220901120000',
        'using': False,
    },
}
"""
# 用于存储表信息的字典
tables = app.config['TABLES']
initialized = False  # 初始化标志

# 把 tables 转换为格式化的字符串
def format_log_dict(log_dict):
    formatted_str = "{\n"
    for key, value in log_dict.items():
        class_name = value['class'].__name__
        table_name = value['table_name']
        using = value['using']
        formatted_str += f"    '{key}': {{\n"
        formatted_str += f"        'class': {class_name},\n"
        formatted_str += f"        'table_name': '{table_name}',\n"
        formatted_str += f"        'using': {using},\n"
        formatted_str += f"    }},\n"
    formatted_str += "}"
    return formatted_str

# 根据 time | 表名 把当前表设置为正在使用
# 可以接受的输入为：20210901120000, dynamic_http_request_log_20210901120000
def set_using(table_name: str):
    if table_name.startswith(app.config['SQL_TABLE_NAME_PREFIX']):
        # 表名就符合规则的 dynamic_http_request_log_20210901120000 格式
        time = table_name.split('_')[-1]
    else:
        # 构造表名
        time = table_name
        table_name = app.config['SQL_TABLE_NAME_PREFIX'] + time
    
    # 调用 use API 设置当前的 table_name 为 using=True 的状态
    use_api_url = request.host_url + 'api/db/use'
    response = requests.post(use_api_url, json={'table_name': table_name})
    
    # 判断修改表的状态为正在使用成功与否
    if response.status_code != 200:
        return {'error': 'Failed to set table as using'}, False, response.status_code, None, None
    else:
        return {'message': 'Successfully set table as using'}, True, response.status_code, table_name, time

"""
第一部分: DCL (Data Control Language) 数据控制
- /api/db/init: 初始化数据库和环境变量
- /api/db/create: 创建表
- /api/db/use: 切换表
- /api/db/drop: 删除表
- /api/db/drop_all: 删除所有表
- /api/db/info: 列出所有表，以及表环境变量
"""

# 启动时，检查数据库中已经存在的表，添加到 tables 中
@app.before_request
def init():
    global initialized
    if not initialized:
        with app.app_context():
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            
            # 刚启动的时候，没有表是被使用的
            for table_name in table_names:
                time = table_name.split('_')[-1]
                tables[time] = {
                    'table_name': table_name,
                    'using': False,
                }

        initialized = True

# API: Create a new table for HttpRequestLog based on time
@app.route('/api/db/create', methods=['POST'])
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
                'table_name': table_name,
                'using': False,
            }
            new_table.__table__.create(db.engine)
            return jsonify({'status': '200', 'message': f'Table {table_name} created successfully'}), 200
        else:
            return jsonify({'status': '200', 'message': f'Table {table_name} already exists'}), 200
        
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': 'Invalid time format. Expected format: YYYY-MM-DD HH:MM:SS'}), 400

# API: 定义正在使用的表名 using=True
@app.route('/api/db/use', methods=['GET', 'POST'])
def change_using():
    if request.method == 'GET':
        # 如果是 GET 请求，返回当前正在使用的表名
        if True in [tables[key]['using'] for key in tables]:
            current_using_tables = [tables[key]['table_name'] for key in tables if tables[key]['using']]
            if len(current_using_tables) == 1:
                return jsonify({'status': '200', 'msg': f'Currently using table {current_using_tables[0]}'}), 200
            else:
                # Only one table is allowed to configured as using
                # Set all tables to using=False
                for key in tables:
                    tables[key]['using'] = False
                return jsonify({'status': '400', 'msg': 'Multiple tables are currently being used'}), 400
        else:
            return jsonify({'status': '200', 'msg': 'No table is currently being used'}), 200
    elif request.method == 'POST':
        # 如果是 POST 请求，更改正在使用的表名
        if request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        time_str = request.json.get('table_name')
        time = time_str.split('_')[-1]

        # 检查表名是否有效 + 是否正在被使用 如果没有 就切换正在使用的表
        if not time_str or time not in tables.keys():
            return jsonify({'error': 'Invalid table name'}), 400
        
        # 构造表名
        table_name = app.config['SQL_TABLE_NAME_PREFIX'] + time

        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 检查表是否正在被使用
        if not tables[time]['using']:
            # 寻找当前正在使用的表，置为不使用
            for key in tables:
                if tables[key]['using']:
                    tables[key]['using'] = False
                    break
            # 切换正在使用的表
            tables[time]['using'] = True
        
        return jsonify({'status': '200', 'msg': f'Table {table_name} is now being used'}), 200

# API: Drop HttpRequestLog table
@app.route('/api/db/drop', methods=['POST'])
def drop_table():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    time_str = request.json.get('table_name') # 可以输入一长串表名字符串，也可以只输入最后的时间格式
    time = time_str.split('_')[-1]

    # 检查输入是否符合格式
    if not time_str or time not in tables.keys() or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name'}), 400
    
    # 构造表名
    table_name = app.config['SQL_TABLE_NAME_PREFIX'] + time

    # 检查表是否存在
    inspector = inspect(db.engine)
    if not inspector.has_table(table_name):
        return jsonify({'error': 'Table not found'}), 404

    try:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)

        table.drop(db.engine)
        del tables[time]

        db.session.commit()
        return jsonify({'status': '200', 'msg': f'Table {table_name} dropped'}), 200
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
@app.route('/api/db/info', methods=['GET'])
def list_tables():
    inspector = db.inspect(db.engine)
    ret_tables = inspector.get_table_names()

    # ret_tables_str = format_log_dict(tables)
    # print(ret_tables_str)
    
    # 检查数据库中的表和环境变量中的表是否一致
    checker1 = set(ret_tables)
    checker2 = set([v['table_name'] for v in tables.values()])
    if len(checker1 - checker2) != 0:
        return jsonify({'error': 'Database and environment variables are inconsistent'}), 500
    
    return jsonify({'tables': ret_tables, 'tables_verbose': tables}), 200

def is_valid_datetime_format(date_string):
    try:
        # 尝试解析字符串为日期时间对象
        datetime.strptime(date_string, app.config['SQL_TIME_FORMAT'])
        return True
    except ValueError:
        # 如果解析失败，抛出 ValueError 异常
        return False

"""
第二个部分: DML (Data Manipulation Language) 数据操作, DQL (Data Query Language) 数据查询
- /api/db/<table_name>/info: 获取表的信息
- /api/db/<table_name>/insert: 插入数据
- /api/db/<table_name>/select: 查询数据
- /api/db/<table_name>/delete: 删除数据
- /api/db/<table_name>/clean: 清空表
"""

# 获取这个表的相关信息
@app.route('/api/db/<table_name>/info', methods=['GET'])
def get_table_info(table_name):
    # 可以输入一长串表名字符串，也可以只输入最后的时间格式
    time_str = table_name
    time = time_str.split('_')[-1]

    # 检查输入是否符合格式
    if not time_str or time not in tables.keys():
        return jsonify({'error': 'Invalid table name'}), 400
    
    # 构造表名
    table_name = app.config['SQL_TABLE_NAME_PREFIX'] + time
    
    # 检查表是否存在
    inspector = inspect(db.engine)
    if not inspector.has_table(table_name):
        return jsonify({'error': 'Table not found'}), 404
    
    # 获取表的结构
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=db.engine)
    columns = [column.name for column in table.columns]
    
    # 获取表当前含有的记录数量
    with db.session() as session:
        num_records = session.query(table).count()

    return jsonify(dict([
        ('table_name', table_name),
        ('using', tables[time]['using']),
        ('columns', columns),
        ('num_records', num_records)
    ])), 200

# API: Insert a record into HttpRequestLog table
@app.route('/api/db/<table_name>/insert', methods=['POST'])
def insert_record(table_name):
    mesg, is_done, status_code, table_name, time = set_using(table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not table_name or time not in tables.keys() or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400
    
    # 如果不是 POST 请求直接抛错
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.json

    required_fields = [
        'category', 'source_ip', 'source_port', 'destination_ip', 'destination_port',
        'request_method', 'request_uri', 'http_version', 'header_fields'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 利用反射，获取表的结构
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)
        
        # 检查 time 的格式是否正确，如果不存在或者格式不正确，则使用当前时间
        time = data.get('time', None)
        if time is None or not is_valid_datetime_format(time):
            time = datetime.now().strftime(app.config['SQL_TIME_FORMAT'])
        
        # 创建记录
        record = {
            'category': data['category'],
            'source_ip': data['source_ip'],
            'source_port': data['source_port'],
            'destination_ip': data['destination_ip'],
            'destination_port': data['destination_port'],
            'time': time,
            'request_method': data['request_method'],
            'request_uri': data['request_uri'],
            'http_version': data['http_version'],
            'header_fields': data['header_fields'],
            'request_body': data.get('request_body')
        }
        
        # 插入记录
        stmt = insert(table).values(record)
        with db.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        
        # 插入成功返回
        return jsonify({'status': '200', 'msg': 'Record inserted', 'data': record}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API: 查询表中的记录
@app.route('/api/db/<table_name>/select', methods=['GET'])
def query_records(table_name):
    mesg, is_done, status_code, table_name, time = set_using(table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not table_name or time not in tables.keys() or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 动态加载表实例
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)

        # 查询所有记录
        with db.session() as session:
            records = session.query(table).all()
        
        print(records)

        # 转换记录为字典列表
        result = [
            {column.name: getattr(record, column.name) for column in table.columns}
            for record in records
        ]

        return jsonify({'status': '200', 'data': result}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        # 记录并返回详细错误信息
        error_details = str(e.__dict__.get('orig', e))
        app.logger.error(f"SQLAlchemyError: {error_details}")
        return jsonify({'error': error_details}), 500
    except Exception as e:
        # 捕获所有其他异常并记录
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API: 根据id删除表中的记录
@app.route('/api/db/<table_name>/delete/<id>', methods=['GET'])
def delete(table_name, id):
    mesg, is_done, status_code, table_name, time = set_using(table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not table_name or time not in tables.keys() or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 动态加载表实例
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)

        # 检查表中id是否存在
        with db.session() as session:
            record = session.query(table).filter(table.c.id == id).first()
            if not record:
                return jsonify({'error': 'Record not found'}), 404

        # 删除记录
        with db.session() as session:
            session.query(table).filter(table.c.id == id).delete()
            session.commit()
        
        return jsonify({'status': '200', 'msg': 'Record deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        # 记录并返回详细错误信息
        error_details = str(e.__dict__.get('orig', e))
        app.logger.error(f"SQLAlchemyError: {error_details}")
        return jsonify({'error': error_details}), 500
    except Exception as e:
        # 捕获所有其他异常并记录
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API: 清空表中的所有记录
@app.route('/api/db/<table_name>/clean', methods=['GET'])
def clean_table(table_name):
    mesg, is_done, status_code, table_name, time = set_using(table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not table_name or time not in tables.keys() or not tables[time]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 动态加载表实例
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)

        # 删除所有记录
        with db.session() as session:
            session.query(table).delete()
            session.commit()
        
        return jsonify({'status': '200', 'msg': 'Table cleaned'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        # 记录并返回详细错误信息
        error_details = str(e.__dict__.get('orig', e))
        app.logger.error(f"SQLAlchemyError: {error_details}")
        return jsonify({'error': error_details}), 500
    except Exception as e:
        # 捕获所有其他异常并记录
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500