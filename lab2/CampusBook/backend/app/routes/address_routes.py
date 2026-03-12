from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db

address_routes = Blueprint('address_routes', __name__)

@address_routes.route('', methods=['GET'])
def get_addresses():
    """获取地址列表"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, receiver, phone, address, is_default FROM address WHERE user_id = ?', (user_id,))
    addresses = cur.fetchall()
    conn.close()
    
    address_list = []
    for address in addresses:
        address_list.append({
            'id': address['id'],
            'receiver': address['receiver'],
            'phone': address['phone'],
            'address': address['address'],
            'is_default': address['is_default']
        })
    
    return jsonify({'code': 200, 'data': address_list})

@address_routes.route('', methods=['POST'])
def add_address():
    """新增地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    data = request.get_json()
    is_default = data.get('is_default', 0)
    
    conn = get_db()
    cur = conn.cursor()
    
    # 如果设置为默认地址，先将其他地址设为非默认
    if is_default:
        cur.execute('UPDATE address SET is_default = 0 WHERE user_id = ?', (user_id,))
    
    # 添加新地址
    cur.execute('''
        INSERT INTO address (user_id, receiver, phone, address, is_default)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, data.get('receiver'), data.get('phone'), data.get('address'), is_default))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '地址添加成功'})

@address_routes.route('/<int:id>', methods=['PUT'])
def update_address(id):
    """更新地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    
    # 检查地址是否存在
    cur.execute('SELECT id FROM address WHERE id = ? AND user_id = ?', (id, user_id))
    if not cur.fetchone():
        conn.close()
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    data = request.get_json()
    is_default = data.get('is_default', 0)
    
    # 如果设置为默认地址，先将其他地址设为非默认
    if is_default:
        cur.execute('UPDATE address SET is_default = 0 WHERE user_id = ? AND id != ?', (user_id, id))
    
    # 更新地址
    update_fields = []
    update_values = []
    
    if 'receiver' in data:
        update_fields.append('receiver = ?')
        update_values.append(data['receiver'])
    if 'phone' in data:
        update_fields.append('phone = ?')
        update_values.append(data['phone'])
    if 'address' in data:
        update_fields.append('address = ?')
        update_values.append(data['address'])
    update_fields.append('is_default = ?')
    update_values.append(is_default)
    
    if update_fields:
        update_query = f"UPDATE address SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(id)
        cur.execute(update_query, update_values)
        conn.commit()
    
    conn.close()
    return jsonify({'code': 200, 'message': '地址更新成功'})

@address_routes.route('/<int:id>', methods=['DELETE'])
def delete_address(id):
    """删除地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    
    # 检查地址是否存在
    cur.execute('SELECT id FROM address WHERE id = ? AND user_id = ?', (id, user_id))
    if not cur.fetchone():
        conn.close()
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    # 删除地址
    cur.execute('DELETE FROM address WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '地址删除成功'})