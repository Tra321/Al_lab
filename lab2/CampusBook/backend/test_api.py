import requests
import json

base_url = "http://127.0.0.1:5000"

def test_user_register():
    """测试用户注册"""
    print("\n========== 测试用户注册 ==========")
    url = f"{base_url}/api/user/register"
    data = {
        "username": "test001",
        "password": "123456",
        "nickname": "测试用户",
        "phone": "13800138000",
        "email": "test@example.com"
    }
    response = requests.post(url, json=data)
    print(f"URL: {url}")
    print(f"请求数据: {data}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_user_login():
    """测试用户登录"""
    print("\n========== 测试用户登录 ==========")
    url = f"{base_url}/api/user/login"
    data = {
        "username": "test001",
        "password": "123456"
    }
    response = requests.post(url, json=data)
    print(f"URL: {url}")
    print(f"请求数据: {data}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_get_books():
    """测试获取书籍列表"""
    print("\n========== 测试获取书籍列表 ==========")
    url = f"{base_url}/api/books"
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_publish_book():
    """测试发布书籍"""
    print("\n========== 测试发布书籍 ==========")
    url = f"{base_url}/api/books"
    data = {
        "title": "Python编程入门",
        "author": "张三",
        "isbn": "978-7-121-00001-5",
        "category": "教材类",
        "condition": "九成新",
        "price": 25.00,
        "description": "一本很好的Python入门书籍",
        "stock": 1,
        "delivery_type": "自提+快递"
    }
    response = requests.post(url, json=data)
    print(f"URL: {url}")
    print(f"请求数据: {data}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_get_book_detail(book_id):
    """测试获取书籍详情"""
    print("\n========== 测试获取书籍详情 ==========")
    url = f"{base_url}/api/books/{book_id}"
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_search_books():
    """测试搜索书籍"""
    print("\n========== 测试搜索书籍 ==========")
    url = f"{base_url}/api/books/search?keyword=Python"
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_add_address():
    """测试添加地址"""
    print("\n========== 测试添加地址 ==========")
    url = f"{base_url}/api/addresses"
    data = {
        "receiver": "张三",
        "phone": "13800138000",
        "address": "北京市海淀区清华大学",
        "is_default": 1
    }
    response = requests.post(url, json=data)
    print(f"URL: {url}")
    print(f"请求数据: {data}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_get_addresses():
    """测试获取地址列表"""
    print("\n========== 测试获取地址列表 ==========")
    url = f"{base_url}/api/addresses"
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_create_order():
    """测试创建订单"""
    print("\n========== 测试创建订单 ==========")
    url = f"{base_url}/api/orders"
    data = {
        "book_id": 1,
        "address_id": 1
    }
    response = requests.post(url, json=data)
    print(f"URL: {url}")
    print(f"请求数据: {data}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

def test_get_orders():
    """测试获取订单列表"""
    print("\n========== 测试获取订单列表 ==========")
    url = f"{base_url}/api/orders"
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    return response.json()

if __name__ == "__main__":
    try:
        # 1. 测试用户注册
        test_user_register()

        # 2. 测试用户登录
        test_user_login()

        # 3. 测试获取书籍列表
        test_get_books()

        # 4. 测试发布书籍
        publish_result = test_publish_book()

        # 5. 测试获取书籍详情
        if publish_result.get('code') == 200:
            test_get_book_detail(1)

        # 6. 测试搜索书籍
        test_search_books()

        # 7. 测试添加地址
        test_add_address()

        # 8. 测试获取地址列表
        test_get_addresses()

        # 9. 测试创建订单
        test_create_order()

        # 10. 测试获取订单列表
        test_get_orders()

        print("\n========== 所有测试完成 ==========")

    except requests.exceptions.ConnectionError:
        print("错误：无法连接到后端服务，请确保后端已启动在 http://127.0.0.1:5000")
    except Exception as e:
        print(f"错误：{e}")
