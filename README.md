# AI Lab 项目

## 项目结构

```
AI_lab/
├── lab1/             # 实验1相关代码
│   ├── desktop_clock.py     # 桌面时钟应用
│   ├── test_kimi.py         # Kimi API 测试
│   └── test1/               # 测试目录
├── lab2/             # 实验2相关代码
│   ├── game/                # 游戏目录
│   │   ├── Gobang/          # 五子棋游戏
│   │   │   ├── index.html
│   │   │   ├── script.js
│   │   │   └── style.css
│   │   └── snake/           # 贪吃蛇游戏
│   │       ├── index.html
│   │       ├── script.js
│   │       └── style.css
│   └── Gobang/              # 另一个五子棋实现
├── test_env.py       # 环境测试脚本
└── README.md         # 项目说明文档
```

## 游戏说明

### 1. 贪吃蛇 (Snake)
- **位置**: `lab2/game/snake/`
- **玩法**: 使用方向键控制蛇的移动，吃掉食物增长身体，避免撞到墙壁或自身
- **技术**: 使用HTML5 Canvas和JavaScript实现

### 2. 五子棋 (Gobang)
- **位置**: `lab2/game/Gobang/`
- **玩法**: 黑白双方轮流下棋，先在一条直线上形成五子连线者获胜
- **技术**: 使用HTML5 Canvas和JavaScript实现，支持人机对战

## 运行方法

### 贪吃蛇游戏
1. 打开 `lab2/game/snake/index.html` 文件
2. 使用键盘方向键控制蛇的移动

### 五子棋游戏
1. 打开 `lab2/game/Gobang/index.html` 文件
2. 点击棋盘开始游戏，黑白双方轮流下棋

## 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **Python**: Tkinter (桌面时钟应用)
- **API**: OpenAI SDK (Kimi API测试)

## 项目目的

本项目用于学习和实践AI相关技术，包括：
- 前端游戏开发
- Python桌面应用开发
- 大语言模型API调用

## 版本控制

项目使用Git进行版本控制，远程仓库地址：
`https://github.com/Tra321/Al_lab.git`