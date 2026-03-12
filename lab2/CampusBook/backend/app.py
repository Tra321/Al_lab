from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/campus_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

CORS(app)
db = SQLAlchemy(app)

# 导入路由
from app.routes import user_routes, book_routes, order_routes, address_routes

# 注册路由
app.register_blueprint(user_routes, url_prefix='/api/user')
app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(order_routes, url_prefix='/api/orders')
app.register_blueprint(address_routes, url_prefix='/api/addresses')

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)