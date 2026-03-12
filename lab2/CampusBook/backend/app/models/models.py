import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import db
from datetime import datetime

class User(db.Model):
    """用户表模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(255), default='')
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(100), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Book(db.Model):
    """书籍表模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), default='')
    isbn = db.Column(db.String(20), default='')
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, default='')
    stock = db.Column(db.Integer, default=1)
    delivery_type = db.Column(db.String(50), nullable=False)
    images = db.Column(db.String(500), default='[]')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Integer, default=1)  # 1:上架 0:下架
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    """订单表模型"""
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=0)  # 0:待付款 1:待发货 2:待收货 3:已完成 4:已取消
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Address(db.Model):
    """地址表模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_default = db.Column(db.Integer, default=0)  # 0:非默认 1:默认