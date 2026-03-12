from flask import Flask
import sqlite3

# 创建Flask应用实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# 简单的CORS实现
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# 数据库连接函数
def get_db():
    conn = sqlite3.connect('instance/campus_book.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'campus_book.db')
    conn = sqlite3.connect(db_path)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()