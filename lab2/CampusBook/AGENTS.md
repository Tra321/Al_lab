# AGENTS.md - 校园二手书交易平台项目规范

## 1. 项目概述

本项目为**校园二手书交易平台 v1.0**，基于需求文档 `需求文档v1.0.md` 开发。

### 技术栈
- **前端**: Vue 3 + Element Plus + Pinia + Vue Router
- **后端**: Python Flask + Flask-SQLAlchemy + SQLite 3

---

## 2. 功能范围（严格遵守）

### 2.1 用户模块
| 功能 | 说明 |
|------|------|
| 用户注册 | 支持校园邮箱(@gzus.edu.cn)和手机号注册，密码6-20位 |
| 用户登录 | 账号密码登录，支持记住密码 |
| 用户信息管理 | 查看/修改昵称、头像 |

### 2.2 书籍模块
| 功能 | 说明 |
|------|------|
| 书籍发布 | 书名(必填)、作者、ISBN、分类(必填)、成色(必填)、价格(必填)、描述、交易方式(必填)、库存(默认1)、图片(最多3张) |
| 书籍浏览 | 首页分页展示(每页20条)，分类浏览 |
| 书籍搜索 | 按书名模糊搜索，支持分类/价格区间/成色筛选 |
| 书籍详情 | 展示基本信息、图片、卖家信息，立即购买按钮 |

### 2.3 订单模块
| 功能 | 说明 |
|------|------|
| 创建订单 | 选择收货地址 -> 确认订单 -> 提交 |
| 订单状态 | 待付款 -> 待发货 -> 待收货 -> 已完成 / 已取消 |
| 订单管理 | 查看订单列表、订单详情、取消订单(待付款)、确认收货(待收货) |
| 地址管理 | 新增、查看、设置默认收货地址 |

---

## 3. 页面结构

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | / | 展示最新书籍列表 |
| 登录 | /login | 用户登录 |
| 注册 | /register | 用户注册 |
| 书籍详情 | /book/:id | 书籍详情页 |
| 发布书籍 | /publish | 发布二手书籍 |
| 分类浏览 | /category/:type | 按分类浏览 |
| 搜索结果 | /search | 搜索结果页 |
| 订单列表 | /orders | 我的订单 |
| 订单详情 | /order/:id | 订单详情页 |
| 地址管理 | /address | 收货地址管理 |
| 个人中心 | /profile | 个人资料 |

---

## 4. 数据库模型

### 4.1 用户表 (User)
- id, username, password, nickname, avatar, phone, email, created_at

### 4.2 书籍表 (Book)
- id, title, author, isbn, category, condition, price, description, stock, delivery_type, images, user_id, status, created_at

### 4.3 订单表 (Order)
- id, order_no, user_id, book_id, address_id, total_price, status, created_at, updated_at

### 4.4 地址表 (Address)
- id, user_id, receiver, phone, address, is_default

---

## 5. API规范

### 5.1 用户相关
- POST /api/user/register - 用户注册
- POST /api/user/login - 用户登录
- GET /api/user/profile - 获取用户信息
- PUT /api/user/profile - 更新用户信息

### 5.2 书籍相关
- GET /api/books - 获取书籍列表
- GET /api/books/:id - 获取书籍详情
- POST /api/books - 发布书籍
- PUT /api/books/:id - 更新书籍
- DELETE /api/books/:id - 删除书籍
- GET /api/books/search - 搜索书籍

### 5.3 订单相关
- POST /api/orders - 创建订单
- GET /api/orders - 获取订单列表
- GET /api/orders/:id - 获取订单详情
- PUT /api/orders/:id/cancel - 取消订单
- PUT /api/orders/:id/confirm - 确认收货

### 5.4 地址相关
- GET /api/addresses - 获取地址列表
- POST /api/addresses - 新增地址
- PUT /api/addresses/:id - 更新地址
- DELETE /api/addresses/:id - 删除地址

---

## 6. 开发规范

### 6.1 代码规范
- 使用中文注释（函数级注释必须）
- 遵循需求文档v1.0中的功能定义，不得擅自添加或修改功能
- 避免代码冗余
- 禁止编写测试代码

### 6.2 安全要求
- 用户密码必须加密存储（SHA256）
- 防止SQL注入
- 敏感信息脱敏处理

### 6.3 性能要求
- 页面加载时间不超过3秒
- 搜索响应时间不超过1秒

---

## 7. 验收标准

- [ ] 用户可以成功注册账号（邮箱/手机）
- [ ] 用户可以登录和退出
- [ ] 用户可以修改昵称和头像
- [ ] 用户可以发布二手书籍（填写基本信息、上传图片）
- [ ] 首页展示最新发布的书籍列表
- [ ] 用户可以按分类浏览书籍
- [ ] 用户可以搜索书籍（书名、分类、价格、成色）
- [ ] 用户可以查看书籍详情
- [ ] 用户可以新增收货地址
- [ ] 用户可以创建订单（立即购买）
- [ ] 用户可以查看订单列表
- [ ] 用户可以取消订单（待付款状态）
- [ ] 用户可以确认收货（待收货状态）
- [ ] 系统运行稳定，无崩溃
- [ ] 界面基本可用，符合用户体验
