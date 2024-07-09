"""
Model Design:
    ID: int
    Category: string
    Source IP Address: string
    Source Port: string
    Destination IP Address: string
    Destination Port: string
    Timestamp: string
    Request Method: string
    Request URI: string
    HTTP Version: string
    Header Fields: string (json string)
    Request Body (POST requests only): string (json string)
"""
import sys
sys.path.append('..')

from app import db
from datetime import datetime


class IntrusionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False)
    source_ip = db.Column(db.String(64), nullable=False)
    source_port = db.Column(db.String(64), nullable=False)
    destination_ip = db.Column(db.String(64), nullable=False)
    destination_port = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.String(64), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    request_method = db.Column(db.String(16), nullable=False)
    request_uri = db.Column(db.String(256), nullable=False)
    http_version = db.Column(db.String(16), nullable=False)
    header_fields = db.Column(db.Text, nullable=False)  # JSON string
    request_body = db.Column(db.Text, nullable=True)  # JSON string, for POST requests only

    def __repr__(self):
        return f'<IntrusionLog {self.source_ip}:{self.source_port} -> {self.destination_ip}:{self.destination_port}: {self.timestamp} - {self.request_method} - {self.request_uri}'
