from flask import Blueprint, request, jsonify
from app.models.models import Order, Book, Address, User
from app import db
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
    
    # 检查书籍是否存在
    book = Book.query.get(book_id)
    if not book or book.status == 0:
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查地址是否存在
    address = Address.query.get(address_id)
    if not address or address.user_id != user_id:
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    # 检查库存
    if book.stock <= 0:
        return jsonify({'code': 400, 'message': '库存不足'})
    
    # 创建订单
    order_no = generate_order_no()
    new_order = Order(
        order_no=order_no,
        user_id=user_id,
        book_id=book_id,
        address_id=address_id,
        total_price=book.price,
        status=0  # 待付款
    )
    
    # 减少库存
    book.stock -= 1
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '订单创建成功', 'data': {
        'order_id': new_order.id,
        'order_no': new_order.order_no
    }})

@order_routes.route('', methods=['GET'])
def get_orders():
    """获取订单列表"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    status = request.args.get('status', '')
    query = Order.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=int(status))
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    order_list = []
    for order in orders:
        book = Book.query.get(order.book_id)
        address = Address.query.get(order.address_id)
        order_list.append({
            'id': order.id,
            'order_no': order.order_no,
            'book_title': book.title if book else '未知书籍',
            'price': order.total_price,
            'status': order.status,
            'status_text': ['待付款', '待发货', '待收货', '已完成', '已取消'][order.status],
            'address': f'{address.receiver} {address.phone} {address.address}' if address else '',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'code': 200, 'data': order_list})

@order_routes.route('/<int:id>', methods=['GET'])
def get_order_detail(id):
    """获取订单详情"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    order = Order.query.get(id)
    if not order or order.user_id != user_id:
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    book = Book.query.get(order.book_id)
    address = Address.query.get(order.address_id)
    seller = User.query.get(book.user_id) if book else None
    
    return jsonify({'code': 200, 'data': {
        'id': order.id,
        'order_no': order.order_no,
        'book': {
            'title': book.title if book else '未知书籍',
            'author': book.author if book else '',
            'price': book.price if book else 0,
            'images': book.images if book else '[]'
        },
        'seller': {
            'nickname': seller.nickname if seller else '未知',
            'phone': seller.phone if seller else ''
        },
        'address': {
            'receiver': address.receiver if address else '',
            'phone': address.phone if address else '',
            'address': address.address if address else ''
        },
        'total_price': order.total_price,
        'status': order.status,
        'status_text': ['待付款', '待发货', '待收货', '已完成', '已取消'][order.status],
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }})

@order_routes.route('/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    """取消订单"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    order = Order.query.get(id)
    if not order or order.user_id != user_id:
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    if order.status != 0:  # 只有待付款状态可以取消
        return jsonify({'code': 400, 'message': '只能取消待付款的订单'})
    
    # 恢复库存
    book = Book.query.get(order.book_id)
    if book:
        book.stock += 1
    
    order.status = 4  # 已取消
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '订单已取消'})

@order_routes.route('/<int:id>/confirm', methods=['PUT'])
def confirm_order(id):
    """确认收货"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    order = Order.query.get(id)
    if not order or order.user_id != user_id:
        return jsonify({'code': 404, 'message': '订单不存在'})
    
    if order.status != 2:  # 只有待收货状态可以确认
        return jsonify({'code': 400, 'message': '只能确认待收货的订单'})
    
    order.status = 3  # 已完成
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '确认收货成功'})