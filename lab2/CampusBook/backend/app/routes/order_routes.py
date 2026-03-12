from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db
import datetime
import random

order_routes = Blueprint('order_routes', __name__)

def generate_order_no():
    """生成订单号"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(1000, 9999)
    return f'{timestamp}{random_num}'

@order_routes.route('', methods=['POST'])
def create_order():
    """创建订单"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    data = request.get_json()
    book_id = data.get('book_id')
    address_id = data.get('address_id')
    
    conn = get_db()
    cur = conn.cursor()
    
    # 检查书籍是否存在
    cur.execute('SELECT price, status, stock, user_id FROM book WHERE id = ?', (book_id,))
    book = cur.fetchone()
    if not book or book['status'] == 0:
        conn.close()
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查地址是否存在
    cur.execute('SELECT id, receiver, phone, address FROM address WHERE id = ? AND user_id = ?', (address_id, user_id))
    address = cur.fetchone()
    if not address:
        conn.close()
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    # 检查库存
    if book['stock'] <= 0:
        conn.close()
        return jsonify({'code': 400, 'message': '库存不足'})
    
    # 创建订单
    order_no = generate_order_no()
    total_price = book['price']
    
    cur.execute('''
        INSERT INTO "order" (order_no, user_id, book_id, address_id, total_price, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (order_no, user_id, book_id, address_id, total_price, 0))
    order_id = cur.lastrowid
    
    # 减少库存
    cur.execute('UPDATE book SET stock = stock - 1 WHERE id = ?', (book_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '订单创建成功', 'data': {
        'order_id': order_id,
        'order_no': order_no
    }})

@order_routes.route('', methods=['GET'])
def get_orders():
    """获取订单列表"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    status = request.args.get('status', '')
    conn = get_db()
    cur = conn.cursor()
    
    query = 'SELECT o.id, o.order_no, o.total_price, o.status, o.created_at, b.title, a.receiver, a.phone, a.address FROM "order" o JOIN book b ON o.book_id = b.id JOIN address a ON o.address_id = a.id WHERE o.user_id = ?'
    params = [user_id]
    
    if status:
        query += ' AND o.status = ?'
        params.append(int(status))
    
    query += ' ORDER BY o.created_at DESC'
    cur.execute(query, params)
    orders = cur.fetchall()
    conn.close()
    
    order_list = []
    for order in orders:
        order_list.append({
            'id': order['id'],
            'order_no': order['order_no'],
            'book_title': order['title'] if order['title'] else '未知书籍',
            'price': order['total_price'],
            'status': order['status'],
            'status_text': ['待付款', '待发货', '待收货', '已完成', '已取消'][order['status']],
            'address': f"{order['receiver']} {order['phone']} {order['address']}" if order['receiver'] else '',
            'created_at': order['created_at']
        })
    
    return jsonify({'code': 200, 'data': order_list})

@order_routes.route('/<int:id>', methods=['GET'])
def get_order_detail(id):
    """获取订单详情"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.*, b.title, b.author, b.price, b.images, b.user_id as seller_id, 
               a.receiver, a.phone, a.address, u.nickname as seller_nickname, u.phone as seller_phone
        FROM "order" o
        JOIN book b ON o.book_id = b.id
        JOIN address a ON o.address_id = a.id
        LEFT JOIN user u ON b.user_id = u.id
        WHERE o.id = ? AND o.user_id = ?
    ''', (id, user_id))
    order = cur.fetchone()
    conn.close()
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    return jsonify({'code': 200, 'data': {
        'id': order['id'],
        'order_no': order['order_no'],
        'book': {
            'title': order['title'] if order['title'] else '未知书籍',
            'author': order['author'] if order['author'] else '',
            'price': order['price'] if order['price'] else 0,
            'images': order['images'] if order['images'] else '[]'
        },
        'seller': {
            'nickname': order['seller_nickname'] if order['seller_nickname'] else '未知',
            'phone': order['seller_phone'] if order['seller_phone'] else ''
        },
        'address': {
            'receiver': order['receiver'] if order['receiver'] else '',
            'phone': order['phone'] if order['phone'] else '',
            'address': order['address'] if order['address'] else ''
        },
        'total_price': order['total_price'],
        'status': order['status'],
        'status_text': ['待付款', '待发货', '待收货', '已完成', '已取消'][order['status']],
        'created_at': order['created_at'],
        'updated_at': order['updated_at']
    }})

@order_routes.route('/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    """取消订单"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    
    # 检查订单是否存在
    cur.execute('SELECT status, book_id FROM "order" WHERE id = ? AND user_id = ?', (id, user_id))
    order = cur.fetchone()
    if not order:
        conn.close()
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    if order['status'] != 0:  # 只有待付款状态可以取消
        conn.close()
        return jsonify({'code': 400, 'message': '只能取消待付款的订单'})
    
    # 恢复库存
    cur.execute('UPDATE book SET stock = stock + 1 WHERE id = ?', (order['book_id'],))
    
    # 更新订单状态
    cur.execute('UPDATE "order" SET status = 4 WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '订单已取消'})

@order_routes.route('/<int:id>/confirm', methods=['PUT'])
def confirm_order(id):
    """确认收货"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    conn = get_db()
    cur = conn.cursor()
    
    # 检查订单是否存在
    cur.execute('SELECT status FROM "order" WHERE id = ? AND user_id = ?', (id, user_id))
    order = cur.fetchone()
    if not order:
        conn.close()
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    if order['status'] != 2:  # 只有待收货状态可以确认
        conn.close()
        return jsonify({'code': 400, 'message': '只能确认待收货的订单'})
    
    # 更新订单状态
    cur.execute('UPDATE "order" SET status = 3, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '确认收货成功'})