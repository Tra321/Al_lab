from config import app, init_db
import os

# 确保instance目录存在
if not os.path.exists('instance'):
    os.makedirs('instance')

# 初始化数据库
try:
    init_db()
except Exception as e:
    print(f"数据库初始化失败: {e}")

# 导入路由
from app.routes.user_routes import user_routes
from app.routes.book_routes import book_routes
from app.routes.order_routes import order_routes
from app.routes.address_routes import address_routes

# 注册路由
app.register_blueprint(user_routes, url_prefix='/api/user')
app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(order_routes, url_prefix='/api/orders')
app.register_blueprint(address_routes, url_prefix='/api/addresses')

if __name__ == '__main__':
    app.run(debug=True, port=5000)