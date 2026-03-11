// 获取画布和上下文
const canvas = document.getElementById('game-board');
const ctx = canvas.getContext('2d');

// 游戏变量
let snake = [{x: 200, y: 200}, {x: 190, y: 200}, {x: 180, y: 200}];
let direction = 'right';
let food = {x: 100, y: 100};
let score = 0;
let gameInterval;
let isGameRunning = false;
let isPaused = false;

// 格子大小
const gridSize = 10;

// 初始化游戏
function initGame() {
    snake = [{x: 200, y: 200}, {x: 190, y: 200}, {x: 180, y: 200}];
    direction = 'right';
    generateFood();
    score = 0;
    document.getElementById('score').textContent = score;
    isGameRunning = false;
    isPaused = false;
    clearInterval(gameInterval);
    drawGame();
}

// 绘制游戏
function drawGame() {
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 绘制蛇
    ctx.fillStyle = '#4CAF50';
    snake.forEach(segment => {
        ctx.fillRect(segment.x, segment.y, gridSize, gridSize);
    });
    
    // 绘制食物
    ctx.fillStyle = '#f44336';
    ctx.fillRect(food.x, food.y, gridSize, gridSize);
    
    // 绘制分数
    ctx.fillStyle = '#333';
    ctx.font = '16px Arial';
    ctx.fillText(`分数: ${score}`, 10, 20);
    
    // 绘制游戏状态
    if (!isGameRunning) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('按开始按钮开始游戏', canvas.width / 2, canvas.height / 2);
    } else if (isPaused) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('游戏已暂停', canvas.width / 2, canvas.height / 2);
    }
}

// 移动蛇
function moveSnake() {
    if (!isGameRunning || isPaused) return;
    
    // 创建新的头部
    const head = {x: snake[0].x, y: snake[0].y};
    
    // 根据方向移动头部
    switch (direction) {
        case 'up':
            head.y -= gridSize;
            break;
        case 'down':
            head.y += gridSize;
            break;
        case 'left':
            head.x -= gridSize;
            break;
        case 'right':
            head.x += gridSize;
            break;
    }
    
    // 将新头部添加到蛇的前面
    snake.unshift(head);
    
    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        document.getElementById('score').textContent = score;
        generateFood();
    } else {
        // 移除尾部
        snake.pop();
    }
    
    // 检查碰撞
    if (checkCollision()) {
        gameOver();
    }
    
    // 绘制游戏
    drawGame();
}

// 检查碰撞
function checkCollision() {
    const head = snake[0];
    
    // 检查边界碰撞
    if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) {
        return true;
    }
    
    // 检查自身碰撞
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }
    
    return false;
}

// 生成食物
function generateFood() {
    // 随机生成食物位置
    food.x = Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize;
    food.y = Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize;
    
    // 确保食物不会出现在蛇身上
    snake.forEach(segment => {
        if (food.x === segment.x && food.y === segment.y) {
            generateFood();
        }
    });
}

// 游戏结束
function gameOver() {
    isGameRunning = false;
    clearInterval(gameInterval);
    drawGame();
    alert(`游戏结束！最终分数: ${score}`);
}

// 开始游戏
function startGame() {
    if (!isGameRunning) {
        isGameRunning = true;
        isPaused = false;
        gameInterval = setInterval(moveSnake, 100);
        drawGame();
    }
}

// 暂停游戏
function pauseGame() {
    if (isGameRunning) {
        isPaused = !isPaused;
        drawGame();
    }
}

// 重新开始游戏
function restartGame() {
    initGame();
}

// 键盘控制
document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowUp':
            if (direction !== 'down') direction = 'up';
            break;
        case 'ArrowDown':
            if (direction !== 'up') direction = 'down';
            break;
        case 'ArrowLeft':
            if (direction !== 'right') direction = 'left';
            break;
        case 'ArrowRight':
            if (direction !== 'left') direction = 'right';
            break;
    }
});

// 按钮事件监听
document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('pause-btn').addEventListener('click', pauseGame);
document.getElementById('restart-btn').addEventListener('click', restartGame);

// 初始化游戏
initGame();