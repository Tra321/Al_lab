from flask import Blueprint, request, jsonify
from app.models.models import Address
from app import db

address_routes = Blueprint('address_routes', __name__)

@address_routes.route('', methods=['GET'])
def get_addresses():
    """获取地址列表"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    addresses = Address.query.filter_by(user_id=user_id).all()
    
    address_list = []
    for address in addresses:
        address_list.append({
            'id': address.id,
            'receiver': address.receiver,
            'phone': address.phone,
            'address': address.address,
            'is_default': address.is_default
        })
    
    return jsonify({'code': 200, 'data': address_list})

@address_routes.route('', methods=['POST'])
def add_address():
    """新增地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    data = request.get_json()
    is_default = data.get('is_default', 0)
    
    # 如果设置为默认地址，将其他地址设为非默认
    if is_default:
        Address.query.filter_by(user_id=user_id).update({'is_default': 0})
    
    new_address = Address(
        user_id=user_id,
        receiver=data.get('receiver'),
        phone=data.get('phone'),
        address=data.get('address'),
        is_default=is_default
    )
    
    db.session.add(new_address)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址添加成功'})

@address_routes.route('/<int:id>', methods=['PUT'])
def update_address(id):
    """更新地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    address = Address.query.get(id)
    if not address or address.user_id != user_id:
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    data = request.get_json()
    is_default = data.get('is_default', address.is_default)
    
    # 如果设置为默认地址，将其他地址设为非默认
    if is_default:
        Address.query.filter_by(user_id=user_id).update({'is_default': 0})
    
    address.receiver = data.get('receiver', address.receiver)
    address.phone = data.get('phone', address.phone)
    address.address = data.get('address', address.address)
    address.is_default = is_default
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址更新成功'})

@address_routes.route('/<int:id>', methods=['DELETE'])
def delete_address(id):
    """删除地址"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    address = Address.query.get(id)
    if not address or address.user_id != user_id:
        return jsonify({'code': 404, 'message': '地址不存在'})
    
    db.session.delete(address)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址删除成功'})