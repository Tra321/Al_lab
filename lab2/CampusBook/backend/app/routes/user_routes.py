from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db
import hashlib

user_routes = Blueprint('user_routes', __name__)

def hash_password(password):
    """密码加密"""
    return hashlib.sha256(password.encode()).hexdigest()

@user_routes.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname')
    phone = data.get('phone', '')
    email = data.get('email', '')
    
    # 检查用户名是否已存在
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id FROM user WHERE username = ?', (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'code': 400, 'message': '用户名已存在'})
    
    # 创建新用户
    cur.execute('''
        INSERT INTO user (username, password, nickname, phone, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, hash_password(password), nickname, phone, email))
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '注册成功'})

@user_routes.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 查找用户
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, nickname, avatar, password FROM user WHERE username = ?', (username,))
    user = cur.fetchone()
    conn.close()
    
    if not user or user['password'] != hash_password(password):
        return jsonify({'code': 400, 'message': '用户名或密码错误'})
    
    return jsonify({'code': 200, 'message': '登录成功', 'data': {
        'id': user['id'],
        'nickname': user['nickname'],
        'avatar': user['avatar']
    }})

@user_routes.route('/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, nickname, avatar, phone, email FROM user WHERE id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    return jsonify({'code': 200, 'data': {
        'id': user['id'],
        'nickname': user['nickname'],
        'avatar': user['avatar'],
        'phone': user['phone'],
        'email': user['email']
    }})

@user_routes.route('/profile', methods=['PUT'])
def update_profile():
    """更新用户信息"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id FROM user WHERE id = ?', (user_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    data = request.get_json()
    nickname = data.get('nickname')
    avatar = data.get('avatar')
    
    if nickname:
        cur.execute('UPDATE user SET nickname = ? WHERE id = ?', (nickname, user_id))
    if avatar:
        cur.execute('UPDATE user SET avatar = ? WHERE id = ?', (avatar, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '更新成功'})