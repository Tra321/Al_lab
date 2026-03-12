from flask import Blueprint, request, jsonify
from app.models.models import Book, User
from app import db

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('', methods=['GET'])
def get_books():
    """获取书籍列表"""
    books = Book.query.filter_by(status=1).order_by(Book.created_at.desc()).all()
    
    book_list = []
    for book in books:
        user = User.query.get(book.user_id)
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'condition': book.condition,
            'category': book.category,
            'delivery_type': book.delivery_type,
            'images': book.images,
            'seller': user.nickname if user else '未知',
            'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'code': 200, 'data': book_list})

@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    """获取书籍详情"""
    book = Book.query.get(id)
    if not book or book.status == 0:
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    user = User.query.get(book.user_id)
    return jsonify({'code': 200, 'data': {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'category': book.category,
        'condition': book.condition,
        'price': book.price,
        'description': book.description,
        'stock': book.stock,
        'delivery_type': book.delivery_type,
        'images': book.images,
        'seller': {
            'nickname': user.nickname if user else '未知',
            'created_at': user.created_at.strftime('%Y-%m-%d') if user else ''
        }
    }})

@book_routes.route('', methods=['POST'])
def publish_book():
    """发布书籍"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    data = request.get_json()
    new_book = Book(
        title=data.get('title'),
        author=data.get('author', ''),
        isbn=data.get('isbn', ''),
        category=data.get('category'),
        condition=data.get('condition'),
        price=data.get('price'),
        description=data.get('description', ''),
        stock=data.get('stock', 1),
        delivery_type=data.get('delivery_type'),
        images=data.get('images', '[]'),
        user_id=user_id
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '发布成功'})

@book_routes.route('/<int:id>', methods=['PUT'])
def update_book(id):
    """更新书籍"""
    book = Book.query.get(id)
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查是否是书籍的卖家
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    if book.user_id != user_id:
        return jsonify({'code': 403, 'message': '无权限操作'})
    
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.category = data.get('category', book.category)
    book.condition = data.get('condition', book.condition)
    book.price = data.get('price', book.price)
    book.description = data.get('description', book.description)
    book.stock = data.get('stock', book.stock)
    book.delivery_type = data.get('delivery_type', book.delivery_type)
    book.images = data.get('images', book.images)
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '更新成功'})

@book_routes.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    """删除书籍"""
    book = Book.query.get(id)
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查是否是书籍的卖家
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    if book.user_id != user_id:
        return jsonify({'code': 403, 'message': '无权限操作'})
    
    book.status = 0  # 下架
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '删除成功'})

@book_routes.route('/search', methods=['GET'])
def search_books():
    """搜索书籍"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', 0)
    max_price = request.args.get('max_price', 999999)
    condition = request.args.get('condition', '')
    
    query = Book.query.filter_by(status=1)
    
    if keyword:
        query = query.filter(Book.title.like(f'%{keyword}%'))
    if category:
        query = query.filter_by(category=category)
    if condition:
        query = query.filter_by(condition=condition)
    query = query.filter(Book.price >= min_price, Book.price <= max_price)
    
    books = query.all()
    
    book_list = []
    for book in books:
        user = User.query.get(book.user_id)
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'condition': book.condition,
            'category': book.category,
            'delivery_type': book.delivery_type,
            'images': book.images,
            'seller': user.nickname if user else '未知'
        })
    
    return jsonify({'code': 200, 'data': book_list})