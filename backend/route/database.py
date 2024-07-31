"""
API for database operations
- /api/db/init: 初始化数据库和环境变量
- /api/db/create: 创建表
- /api/db/cur_db: 获得正在使用的表
- /api/db/use: 切换表
- /api/db/drop: 删除表
- /api/db/drop_all: 删除所有表
- /api/db/info: 列出所有表，以及表环境变量

- /api/db/<table_name>/info: 获取表的信息
- /api/db/<table_name>/insert: 插入数据
- /api/db/<table_name>/select: 查询数据
- /api/db/<table_name>/update: 更新数据
- /api/db/<table_name>/delete: 删除数据
- /api/db/<table_name>/clean: 清空表
- /api/db/<table_name>/drop: 删除表

- /api/db/mapper/insert: 插入表名映射关系
- /api/db/mapper/select: 查询所有的表名映射关系
- /api/db/mapper/update: 更新表名映射关系
- /api/db/mapper/delete: 删除表名映射关系
"""
import json
from app import app, db
from flask import jsonify, request, send_file
from datetime import datetime, timezone
from database.model import *
import requests
import csv
import base64
import dpkt
# 数据库操作
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData, inspect, select, func, insert, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

"""
tables: maintain all tables created in the database
{
    'frontend_table_name1': {
        'backend_table_name': 'http_request_log_20210901120000',
        'using': True,
    },
    'frontend_table_name1': {
        'backend_table_name': 'http_request_log_20220901120000',
        'using': False,
    },
}
table_name_mapper: 维护表名到表的映射关系
{
    'frontend_table_name1': 'http_request_log_20210901120000',
    'frontend_table_name2': 'http_request_log_20220901120000',
}
"""
# 用于存储表信息的字典
tables = app.config['TABLES']
table_mapper = app.config['TABLE_MAPPER']
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
def set_using(frontend_table_name: str):    
    # 调用 use API 设置当前的 frontend_tablename 为 using=True 的状态
    use_api_url = request.host_url + 'api/db/use'
    response = requests.post(use_api_url, json={'frontend_table_name': frontend_table_name})
    # time = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') # 获取当前时间
    
    # 根据前端表名查找后端表名
    if frontend_table_name not in tables:
        return {'error': 'Table not found'}, None, 404, None, None
    backend_table_name = tables[frontend_table_name]['backend_table_name']
    
    # 检查后端表是否存在
    inspector = inspect(db.engine)
    if not inspector.has_table(backend_table_name):
        return {'error': 'Table not found'}, None, 404, None, None
    
    # 判断修改表的状态为正在使用成功与否
    if response.status_code != 200:
        return {'error': 'Failed to set table as using'}, False, response.status_code, None, None
    else:
        return {'message': 'Successfully set table as using'}, True, response.status_code, frontend_table_name, backend_table_name

# 查询数据库中的映射表，更新 table_mapper 中的映射关系（环境变量更新）
def update_table_mapper():
    # 检查映射表，添加到 table_mapper 中
    with app.app_context():
        # 查询映射表
        table_mapper_records = TableMapper.query.all()
        # print('table_mapper_records:', table_mapper_records)
        for record in table_mapper_records:
            table_mapper[record.frontend_table_name] = record.backend_table_name

def update_tables():
    # 检查数据库中已经存在的表，添加到 tables 中
    with app.app_context():
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        # print('table_names:', table_names)
        # 如果 table_names 中有 table_mapper 表，则删除
        if 'table_mapper' in table_names:
            table_names.remove('table_mapper')
        
        # 构建 tables 字典
        for table_name in table_names:
            if table_name not in table_mapper.values():
                return jsonify({'error': 'Failed to initialize database'}), 500
            # 查找对应的前端表
            for k, v in table_mapper.items():
                if v == table_name:
                    tables[k] = {
                        "backend_table_name": table_name,
                        "using": False
                    } # 刚启动时，默认没有使用任何表

"""
第一部分: DCL (Data Control Language) 数据控制
- /api/db/init: 初始化数据库和环境变量
- /api/db/create: 创建表
- /api/db/use: 切换表
- /api/db/drop: 删除表
- /api/db/drop_all: 删除所有表
- /api/db/info: 列出所有表，以及表环境变量
"""

# 启动时，创建数据库表
@app.before_request
def create_tables():
    db.create_all()

# 启动时，检查数据库中已经存在的表，添加到 tables 中
# 启动时，检查映射表，添加到 table_mapper 中
@app.before_request
def init():
    global initialized
    if not initialized:
        # 检查映射表，添加到 table_mapper 中
        update_table_mapper()

        # 检查数据库中已经存在的表，添加到 tables 中
        update_tables()
        
        print(f'Initialized database successfully:\ntable_mapper:{table_mapper}\ntables:{tables}')
        initialized = True

# API: Create a new table for HttpRequestLog based on time
@app.route('/api/db/create', methods=['POST'])
def create_table():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.json
    frontend_tablename = data.get('fontend_tablename', '')
    if len(frontend_tablename) == 0:
        return jsonify({'error': 'Table name is required'}), 400
    
    try:
        # 检查前端表名是否存在
        if frontend_tablename in table_mapper:
            return jsonify({'status': '200', 'deplicated': True, 'message': f'Table {frontend_tablename} already exists'}), 200
        
        time = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        new_table, backend_tablename = create_dynamic_http_request_log_class(time, frontend_tablename) # 创建表的时候，需要传入前端的表名，用于创建映射关系
        
        # 检查后端表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(backend_tablename):
            # 创建表
            tables[frontend_tablename] = {
                'backend_table_name': backend_tablename,
                'using': False,
            }
            new_table.__table__.create(db.engine)
            
            # 更新配置
            update_table_mapper()
            update_tables()
            set_using(frontend_tablename)
            
            # return jsonify({'status': '200', 'deplicated': False, 'message': f'Table {{frontend_tablename: {frontend_tablename}, backend_tablename: {backend_tablename}}} created successfully'}), 200
            return jsonify({'status': '200', 'deplicated': False, 'message': f'Table {frontend_tablename} created successfully'}), 200
        else:
            return jsonify({'status': '200', 'deplicated': True, 'message': f'Table {frontend_tablename} already exists'}), 200

        # 检查映射表是否存在
        
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# API: 定义正在使用的后端表名 using=True
@app.route('/api/db/use', methods=['GET', 'POST'])
def change_using():
    if request.method == 'GET':
        # 如果是 GET 请求，更改正在使用的表名
        frontend_table_name = request.args.get('frontend_table_name') # http://localhost:8001/api/db/use?table_name=frontend_table_name
    elif request.method == 'POST':
        # 如果是 POST 请求，更改正在使用的表名
        if request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        frontend_table_name = request.json.get('frontend_table_name') # post body: {"table_name": "frontend_table_name"}
        frontend_table_name = frontend_table_name[0] if isinstance(frontend_table_name, list) else frontend_table_name

    if frontend_table_name is None:
        return jsonify({'error': 'Table name is required'}), 400
    
    # 获取后端表名
    if frontend_table_name in table_mapper.keys():
        backend_table_name = table_mapper[frontend_table_name]

    # 检查前端表名是否有效 + 是否正在被使用 如果没有 就切换正在使用的表
    if frontend_table_name not in table_mapper.keys() or backend_table_name is None:
        return jsonify({'error': 'Invalid table name'}), 400

    # 检查后端表是否存在
    inspector = inspect(db.engine)
    if not inspector.has_table(backend_table_name):
        return jsonify({'error': 'Table not found'}), 404
    
    # 检查表是否正在被使用
    if not tables[frontend_table_name]['using']:
        # 寻找当前正在使用的表，置为不使用
        for key in tables:
            if tables[key]['using']:
                tables[key]['using'] = False
                break
        # 切换正在使用的表
        tables[frontend_table_name]['using'] = True
    
    return jsonify({'status': '200', 'msg': f'Table {frontend_table_name} is now being used'}), 200

# 删除指定的后端表，并且更新 table_mapper 表中的表名映射 TODO
@app.route('/api/db/drop', methods=['GET', 'POST'])
def drop_table():
    pass

# 删除除了 table_mapper 的所有表，并且把 table_mapper 表清空，其中的数据更新到环境变量 tables TODO
@app.route('/api/db/drop_all', methods=['GET', 'POST'])
def drop_all_tables():
    pass

# API: 定义查看所有表名的 API 端点
@app.route('/api/db/info', methods=['GET'])
def list_tables():
    inspector = db.inspect(db.engine)
    ret_tables = inspector.get_table_names()
    # 如果存在，变量中删除 table_mapper 这个表
    if 'table_mapper' in ret_tables:
        ret_tables.remove('table_mapper')

    # ret_tables_str = format_log_dict(tables)
    # print(ret_tables_str)
    
    # 检查数据库中的表和环境变量中的表是否一致
    # print('/api/db/info', tables)
    checker1 = set(ret_tables)
    checker2 = set([v['backend_table_name'] for v in tables.values()])
    if len(checker1 - checker2) != 0:
        return jsonify({'error': 'Database and environment variables are inconsistent', 'ret_tables': ret_tables, 'tables': tables}), 500
    
    return jsonify({'tables': ret_tables, 'tables_verbose': tables, 'table_mapper': table_mapper}), 200

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
- /api/db/<table_name>/update: 更新数据
- /api/db/<table_name>/delete: 删除数据
- /api/db/<table_name>/clean: 清空表
"""

# 获取这个表的相关信息
@app.route('/api/db/<frontend_table_name>/info', methods=['GET'])
def get_table_info(frontend_table_name):
    # 根据前端表名查找后端表名
    if frontend_table_name not in tables:
        return jsonify({'error': 'Table not found'}), 404
    backend_table_name = tables[frontend_table_name]['backend_table_name']
    
    # 检查表是否存在
    inspector = inspect(db.engine)
    if not inspector.has_table(backend_table_name):
        return jsonify({'error': 'Table not found'}), 404
    
    # 获取表的结构
    metadata = MetaData()
    table = Table(backend_table_name, metadata, autoload_with=db.engine)
    columns = [column.name for column in table.columns]
    
    # 获取表当前含有的记录数量
    with db.session() as session:
        num_records = session.query(table).count()
    return jsonify(dict([
        ('frontend_table_name', frontend_table_name),
        ('backend_table_name', backend_table_name),
        ('using', tables[frontend_table_name]['using']),
        ('columns', columns),
        ('num_records', num_records)
    ])), 200

# API: Insert a record into HttpRequestLog table TODO
@app.route('/api/db/<frontend_table_name>/insert', methods=['POST'])
def insert_record(frontend_table_name):
    mesg, is_done, status_code, _, backend_table_name = set_using(frontend_table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not backend_table_name or frontend_table_name not in tables.keys() or not tables[frontend_table_name]['using']:
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
        if not inspector.has_table(backend_table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 动态加载表实例
        metadata = MetaData()
        table = Table(backend_table_name, metadata, autoload_with=db.engine)

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
            'request_body': data.get('request_body', ''),
            'raw_packet': data.get('raw_packet', ''),
        }
        
        # 插入记录a
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
@app.route('/api/db/<frontend_table_name>/select', methods=['GET'])
def query_records(frontend_table_name):
    mesg, is_done, status_code, _, backend_table_name = set_using(frontend_table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not backend_table_name or frontend_table_name not in tables.keys() or not tables[frontend_table_name]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(backend_table_name):
            return jsonify({'error': 'Table not found'}), 404
        
        # 动态加载表实例
        metadata = MetaData()
        table = Table(backend_table_name, metadata, autoload_with=db.engine)

        # 查询所有记录
        with db.session() as session:
            records = session.query(table).all()
        
        # print(records)

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

# API: 根据id删除表中的记录 TODO
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
@app.route('/api/db/<frontend_table_name>/clean', methods=['GET'])
def clean_table(frontend_table_name):
    mesg, is_done, status_code, _, backend_table_name = set_using(frontend_table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not backend_table_name or frontend_table_name not in tables.keys() or not tables[frontend_table_name]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(backend_table_name):
            return jsonify({'error': 'Table not found'}), 404

        # 动态加载表实例
        metadata = MetaData()
        table = Table(backend_table_name, metadata, autoload_with=db.engine)

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

def export_to_csv(table, backend_table_name):
    """Export table data to a CSV file excluding raw_packet."""
    query = db.session.query(table).all()
    csv_filename = f"{backend_table_name}.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow([
            'id', 'category', 'source_ip', 'source_port',
            'destination_ip', 'destination_port', 'time',
            'request_method', 'request_uri', 'http_version',
            'header_fields', 'request_body'
        ])
        # Write data rows
        for row in query:
            writer.writerow([
                row.id, row.category, row.source_ip, row.source_port,
                row.destination_ip, row.destination_port, row.time,
                row.request_method, row.request_uri, row.http_version,
                row.header_fields, row.request_body
            ])
    return csv_filename

def export_to_pcap(table, backend_table_name):
    """Export raw_packet data to a PCAP file."""
    query = db.session.query(table.c.raw_packet).all()
    pcap_filename = f"{backend_table_name}.pcap"
    with open(pcap_filename, 'wb') as pcapfile:
        writer = dpkt.pcap.Writer(pcapfile)
        for row in query:
            raw_packet = base64.b64decode(row.raw_packet)
            writer.writepkt(raw_packet)
    return pcap_filename

@app.route('/api/db/<frontend_table_name>/export/<format>', methods=['GET'])
def export_table(frontend_table_name, format):
    mesg, is_done, status_code, _, backend_table_name = set_using(frontend_table_name)

    if not is_done:
        return jsonify(mesg), status_code

    # 检查输入是否符合格式
    if not backend_table_name or frontend_table_name not in tables.keys() or not tables[frontend_table_name]['using']:
        return jsonify({'error': 'Invalid or inactive table name', 'tables': str(tables)}), 400
    
    # 检查导出格式是否符合要求
    if format not in ['csv', 'pcap']:
        return jsonify({'error': 'Invalid export format'}), 400

    try:
        # 检查表是否存在
        inspector = inspect(db.engine)
        if not inspector.has_table(backend_table_name):
            return jsonify({'error': 'Table not found'}), 404
    
        # 动态加载表实例
        metadata = MetaData()
        table = Table(backend_table_name, metadata, autoload_with=db.engine)
        
        if format == 'csv':
            filename = export_to_csv(table, backend_table_name)
        
        elif format == 'pcap':
            filename = export_to_pcap(table, backend_table_name)
        
        return send_file(filename, as_attachment=True)

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

"""
API:
- /api/db/cur_db: get current using db
"""
@app.route('/api/db/cur_db', methods=['GET'])
def get_cur_db():
    if True in [tables[key]['using'] for key in tables]:
        # 获取后端表名
        current_using_tables = [tables[key]['backend_table_name'] for key in tables if tables[key]['using']]
        if len(current_using_tables) == 1:
            # 根据映射表查询前端表名
            for k,v in table_mapper.items():
                if v == current_using_tables[0]:
                    return jsonify({'status': '200', 'table_name': f'{k}', 'msg': f'Currently using table {k}'}), 200
                    # return jsonify({'status': '200', 'table_name': f'{current_using_tables[0]}', 'msg': f'Currently using table {current_using_tables[0]}'}), 200
            return jsonify({'status': '400', 'msg': 'Frontend table name and backend table name are not matched.'}), 400
        else:
            # Only one table is allowed to configured as using
            # Set all tables to using=False
            for key in tables:
                tables[key]['using'] = False
            return jsonify({'status': '400', 'msg': 'Multiple tables are currently being used'}), 400
    else:
        return jsonify({'status': '200', 'msg': 'No table is currently being used'}), 200


"""
API:
- /api/db/mapper/insert: 插入表名映射关系
- /api/db/mapper/select: 查询所有的表名映射关系
- /api/db/mapper/update: 更新表名映射关系
- /api/db/mapper/delete: 删除表名映射关系
"""
@app.route('/api/db/mapper/select', methods=['GET'])
def select_table_mapping():
    try:
        # 查询所有的表名映射关系
        table_mapper_records = TableMapper.query.all()
        if not table_mapper_records:
            return jsonify({'status': '200', 'msg': 'No table mapping found'}), 200
        
        # 返回所有表名映射关系
        return jsonify({'status': '200', 'msg': 'Table mapping found', 'table_mappings': [{'id': table_mapping.id, 'frontend_table_name': table_mapping.frontend_table_name, 'backend_table_name': table_mapping.backend_table_name, 'created_at': table_mapping.created_at.strftime('%Y-%m-%d %H:%M:%S')} for table_mapping in table_mapper_records]}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        # 记录并返回详细错误信息
        error_details = str(e.__dict__.get('orig', e))
        return jsonify({'error': error_details}), 500
