"""
Model Design: DDL (Data Definition Language)
DynamicHttpRequestLog
    ID: int
    Category: string
    Source IP Address: string
    Source Port: string
    Destination IP Address: string
    Destination Port: string
    Time: string
    Request Method: string
    Request URI: string
    HTTP Version: string
    Header Fields: string (json string)
    Request Body (POST requests only): string (json string)
TableNameMapper
    Table Name in Frontend: string
    Table Name in Backend: string
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, Text, LargeBinary
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from datetime import datetime, timezone
from app import app, db

# 定义一个表名映射表
class TableMapper(db.Model):
    __tablename__ = 'table_mapper'
    id = db.Column(db.Integer, primary_key=True)
    frontend_table_name = db.Column(db.String(256), nullable=False, unique=True)
    backend_table_name = db.Column(db.String(256), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=lambda : datetime.now(timezone.utc))  # ensure that the created_at field gets the current time at the moment when a new record is created, not when the class is defined.

    def __repr__(self):
        return f'<TableMapping {self.frontend_table_name} -> {self.backend_table_name}>'


# 获取 SQLAlchemy 的 Model 元类
ModelMeta = type(db.Model)

# 定义一个新的元类，继承 SQLAlchemy 的 Model 元类和自定义的 ModelGenerator 元类
class CustomModelMeta(ModelMeta, DeclarativeMeta):
    pass

# 定义一个元类，用于动态生成类
class ModelGenerator(CustomModelMeta):
    def __new__(cls, name, bases, dct):
        dct['id'] = Column(Integer, primary_key=True)
        dct['category'] = Column(String(64), nullable=False)
        dct['source_ip'] = Column(String(64), nullable=False)
        dct['source_port'] = Column(String(64), nullable=False)
        dct['destination_ip'] = Column(String(64), nullable=False)
        dct['destination_port'] = Column(String(64), nullable=False)
        dct['time'] = Column(String(64), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        dct['request_method'] = Column(String(16), nullable=False)
        dct['request_uri'] = Column(String(256), nullable=False)
        dct['http_version'] = Column(String(16), nullable=False)
        dct['header_fields'] = Column(Text, nullable=False)  # JSON string
        dct['request_body'] = Column(Text, nullable=True)  # JSON string, for POST requests only
        dct['raw_packet'] = Column(Text, nullable=False)  # Base64 encoded string for the raw packet

        def __repr__(self):
            return (f'<{name} {self.source_ip}:{self.source_port} -> '
                    f'{self.destination_ip}:{self.destination_port}: '
                    f'{self.time} - {self.request_method} - {self.request_uri}>')

        dct['__repr__'] = __repr__

        return super(ModelGenerator, cls).__new__(cls, name, bases, dct)

# 使用元类生成 HttpRequestLog 类
def create_dynamic_http_request_log_class(ds: str, frontend_table_name: str):
    """动态创建带有给定时间戳和表名包含时间戳的 HttpRequestLog 类"""
    class_name = f"{app.config['SQL_CLASS_NAME_PREFIX']}{ds}"
    table_name = f"{app.config['SQL_TABLE_NAME_PREFIX']}{ds}"

    # 定义类属性和方法
    class_attributes = {
        '__tablename__': table_name,
        '__table_args__': {'sqlite_autoincrement': True, 'extend_existing': True},
        'id': Column(Integer, primary_key=True),
        'category': Column(String(64), nullable=False),
        'source_ip': Column(String(64), nullable=False),
        'source_port': Column(String(64), nullable=False),
        'destination_ip': Column(String(64), nullable=False),
        'destination_port': Column(String(64), nullable=False),
        'time': Column(String(64), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'request_method': Column(String(16), nullable=False),
        'request_uri': Column(String(256), nullable=False),
        'http_version': Column(String(16), nullable=False),
        'header_fields': Column(Text, nullable=False),  # JSON string
        'request_body': Column(Text, nullable=True),  # JSON string, for POST requests only,
        'raw_packet': Column(Text, nullable=False),  # Base64 encoded string for the raw packet
        '__repr__': lambda self: (
            f'<HttpRequestLog {self.source_ip}:{self.source_port} -> '
            f'{self.destination_ip}:{self.destination_port}: '
            f'{self.time} - {self.request_method} - {self.request_uri}>'
        ),
    }

    # 使用 type 创建类
    DynamicHttpRequestLog = ModelGenerator(class_name, (db.Model,), class_attributes)
    
    # 创建映射记录
    mapping_record = TableMapper(frontend_table_name=frontend_table_name, backend_table_name=table_name)
    db.session.add(mapping_record)
    db.session.commit()

    return DynamicHttpRequestLog, table_name

# 创建表的方式1
# class HttpRequestLog(db.Model, metaclass=ModelGenerator):
#     __tablename__ = 'http_request_log'

# 创建表的方式2
# 根据当前时间(format: %Y%m%d%H%M%S) 去创建相同格式的表
# a = create_dynamic_http_request_log_class('20210901120000')
# b = create_dynamic_http_request_log_class('20210901120001')
# c = create_dynamic_http_request_log_class('20210901120002')
