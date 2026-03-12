from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('', methods=['GET'])
def get_books():
    """获取书籍列表"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT b.id, b.title, b.author, b.price, b.condition, b.category, 
               b.delivery_type, b.images, b.created_at, u.nickname
        FROM book b
        JOIN user u ON b.user_id = u.id
        WHERE b.status = 1
        ORDER BY b.created_at DESC
    ''')
    books = cur.fetchall()
    conn.close()
    
    book_list = []
    for book in books:
        book_list.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price'],
            'condition': book['condition'],
            'category': book['category'],
            'delivery_type': book['delivery_type'],
            'images': book['images'],
            'seller': book['nickname'] if book['nickname'] else '未知',
            'created_at': book['created_at']
        })
    
    return jsonify({'code': 200, 'data': book_list})

@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    """获取书籍详情"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT b.*, u.nickname, u.created_at as user_created
        FROM book b
        JOIN user u ON b.user_id = u.id
        WHERE b.id = ? AND b.status = 1
    ''', (id,))
    book = cur.fetchone()
    conn.close()
    
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    return jsonify({'code': 200, 'data': {
        'id': book['id'],
        'title': book['title'],
        'author': book['author'],
        'isbn': book['isbn'],
        'category': book['category'],
        'condition': book['condition'],
        'price': book['price'],
        'description': book['description'],
        'stock': book['stock'],
        'delivery_type': book['delivery_type'],
        'images': book['images'],
        'seller': {
            'nickname': book['nickname'] if book['nickname'] else '未知',
            'created_at': book['user_created'].split(' ')[0] if book['user_created'] else ''
        }
    }})

@book_routes.route('', methods=['POST'])
def publish_book():
    """发布书籍"""
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO book (title, author, isbn, category, condition, price, 
                         description, stock, delivery_type, images, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'),
        data.get('author', ''),
        data.get('isbn', ''),
        data.get('category'),
        data.get('condition'),
        data.get('price'),
        data.get('description', ''),
        data.get('stock', 1),
        data.get('delivery_type'),
        data.get('images', '[]'),
        user_id
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '发布成功'})

@book_routes.route('/<int:id>', methods=['PUT'])
def update_book(id):
    """更新书籍"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM book WHERE id = ?', (id,))
    book = cur.fetchone()
    
    if not book:
        conn.close()
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查是否是书籍的卖家
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    if book['user_id'] != user_id:
        conn.close()
        return jsonify({'code': 403, 'message': '无权限操作'})
    
    data = request.get_json()
    update_fields = []
    update_values = []
    
    if 'title' in data:
        update_fields.append('title = ?')
        update_values.append(data['title'])
    if 'author' in data:
        update_fields.append('author = ?')
        update_values.append(data['author'])
    if 'isbn' in data:
        update_fields.append('isbn = ?')
        update_values.append(data['isbn'])
    if 'category' in data:
        update_fields.append('category = ?')
        update_values.append(data['category'])
    if 'condition' in data:
        update_fields.append('condition = ?')
        update_values.append(data['condition'])
    if 'price' in data:
        update_fields.append('price = ?')
        update_values.append(data['price'])
    if 'description' in data:
        update_fields.append('description = ?')
        update_values.append(data['description'])
    if 'stock' in data:
        update_fields.append('stock = ?')
        update_values.append(data['stock'])
    if 'delivery_type' in data:
        update_fields.append('delivery_type = ?')
        update_values.append(data['delivery_type'])
    if 'images' in data:
        update_fields.append('images = ?')
        update_values.append(data['images'])
    
    if update_fields:
        update_query = f"UPDATE book SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(id)
        cur.execute(update_query, update_values)
        conn.commit()
    
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功'})

@book_routes.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    """删除书籍"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM book WHERE id = ?', (id,))
    book = cur.fetchone()
    
    if not book:
        conn.close()
        return jsonify({'code': 404, 'message': '书籍不存在'})
    
    # 检查是否是书籍的卖家
    # 这里应该从token中获取用户ID，暂时使用固定ID
    user_id = 1
    if book['user_id'] != user_id:
        conn.close()
        return jsonify({'code': 403, 'message': '无权限操作'})
    
    cur.execute('UPDATE book SET status = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'code': 200, 'message': '删除成功'})

@book_routes.route('/search', methods=['GET'])
def search_books():
    """搜索书籍"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', 0)
    max_price = request.args.get('max_price', 999999)
    condition = request.args.get('condition', '')
    
    conn = get_db()
    cur = conn.cursor()
    
    query = 'SELECT b.id, b.title, b.author, b.price, b.condition, b.category, b.delivery_type, b.images, u.nickname FROM book b JOIN user u ON b.user_id = u.id WHERE b.status = 1'
    params = []
    
    if keyword:
        query += ' AND b.title LIKE ?'
        params.append(f'%{keyword}%')
    if category:
        query += ' AND b.category = ?'
        params.append(category)
    if condition:
        query += ' AND b.condition = ?'
        params.append(condition)
    query += ' AND b.price >= ? AND b.price <= ?'
    params.extend([min_price, max_price])
    
    cur.execute(query, params)
    books = cur.fetchall()
    conn.close()
    
    book_list = []
    for book in books:
        book_list.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price'],
            'condition': book['condition'],
            'category': book['category'],
            'delivery_type': book['delivery_type'],
            'images': book['images'],
            'seller': book['nickname'] if book['nickname'] else '未知'
        })
    
    return jsonify({'code': 200, 'data': book_list})