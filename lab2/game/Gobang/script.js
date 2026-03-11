// 游戏配置
const CONFIG = {
    boardSize: 15, // 棋盘大小
    cellSize: 30,  // 单元格大小
    pieceRadius: 14, // 棋子半径
    winCount: 5,  // 获胜需要的连子数
    animationSpeed: 300 // 动画速度(ms)
};

// 游戏状态
let gameState = {
    board: Array(CONFIG.boardSize).fill().map(() => Array(CONFIG.boardSize).fill(0)), // 0: 空, 1: 黑棋, 2: 白棋
    currentPlayer: 1, // 1: 黑棋, 2: 白棋
    gameMode: 'human', // human: 双人对战, ai: 人机对战, online: 在线对战
    aiDifficulty: 'easy', // easy: 初级, medium: 中级, hard: 高级
    isGameOver: false,
    isPaused: false,
    moveCount: 0,
    startTime: null,
    elapsedTime: 0,
    moveHistory: [], // 悔棋历史
    redoHistory: [], // 撤销悔棋历史
    boardStyle: 'classic', // 棋盘风格
    pieceStyle: 'classic', // 棋子样式
    isDarkTheme: false, // 深色主题
    stats: {
        wins: 0,
        losses: 0,
        draws: 0
    }
};

// 初始化游戏
function initGame() {
    // 初始化棋盘
    gameState.board = Array(CONFIG.boardSize).fill().map(() => Array(CONFIG.boardSize).fill(0));
    gameState.currentPlayer = 1;
    gameState.isGameOver = false;
    gameState.isPaused = false;
    gameState.moveCount = 0;
    gameState.moveHistory = [];
    gameState.redoHistory = [];
    
    // 重置UI
    updateGameStatus();
    updateMoveCount();
    resetTimer();
    enableButtons();
    
    // 绘制棋盘
    drawBoard();
    
    // 加载本地存储的游戏数据
    loadGameData();
}

// 绘制棋盘
function drawBoard() {
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 绘制棋盘网格
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    
    for (let i = 0; i < CONFIG.boardSize; i++) {
        // 绘制横线
        ctx.beginPath();
        ctx.moveTo(CONFIG.cellSize / 2, CONFIG.cellSize / 2 + i * CONFIG.cellSize);
        ctx.lineTo(canvas.width - CONFIG.cellSize / 2, CONFIG.cellSize / 2 + i * CONFIG.cellSize);
        ctx.stroke();
        
        // 绘制竖线
        ctx.beginPath();
        ctx.moveTo(CONFIG.cellSize / 2 + i * CONFIG.cellSize, CONFIG.cellSize / 2);
        ctx.lineTo(CONFIG.cellSize / 2 + i * CONFIG.cellSize, canvas.height - CONFIG.cellSize / 2);
        ctx.stroke();
    }
    
    // 绘制星位点
    const starPoints = [3, 7, 11];
    ctx.fillStyle = '#333';
    starPoints.forEach(x => {
        starPoints.forEach(y => {
            ctx.beginPath();
            ctx.arc(
                CONFIG.cellSize / 2 + x * CONFIG.cellSize,
                CONFIG.cellSize / 2 + y * CONFIG.cellSize,
                3,
                0,
                2 * Math.PI
            );
            ctx.fill();
        });
    });
    
    // 绘制棋子
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] !== 0) {
                drawPiece(x, y, gameState.board[x][y]);
            }
        }
    }
}

// 绘制棋子
function drawPiece(x, y, player) {
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    
    const centerX = CONFIG.cellSize / 2 + x * CONFIG.cellSize;
    const centerY = CONFIG.cellSize / 2 + y * CONFIG.cellSize;
    
    // 根据棋子样式绘制
    if (gameState.pieceStyle === 'classic') {
        ctx.fillStyle = player === 1 ? '#333' : '#fff';
        ctx.beginPath();
        ctx.arc(centerX, centerY, CONFIG.pieceRadius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.stroke();
    } else if (gameState.pieceStyle === '3d') {
        // 3D棋子效果
        const gradient = ctx.createRadialGradient(
            centerX - 5, centerY - 5, 0,
            centerX - 5, centerY - 5, CONFIG.pieceRadius
        );
        
        if (player === 1) {
            gradient.addColorStop(0, '#555');
            gradient.addColorStop(1, '#000');
        } else {
            gradient.addColorStop(0, '#fff');
            gradient.addColorStop(1, '#e0e0e0');
        }
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(centerX, centerY, CONFIG.pieceRadius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.stroke();
    } else if (gameState.pieceStyle === 'glass') {
        // 玻璃棋子效果
        ctx.fillStyle = player === 1 ? 'rgba(51, 51, 51, 0.9)' : 'rgba(255, 255, 255, 0.9)';
        ctx.beginPath();
        ctx.arc(centerX, centerY, CONFIG.pieceRadius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
}

// 检查落子位置是否合法
function isLegalMove(x, y) {
    return x >= 0 && x < CONFIG.boardSize && y >= 0 && y < CONFIG.boardSize && gameState.board[x][y] === 0;
}

// 落子
function makeMove(x, y) {
    if (!isLegalMove(x, y) || gameState.isGameOver || gameState.isPaused) return false;
    
    // 记录落子
    gameState.board[x][y] = gameState.currentPlayer;
    gameState.moveCount++;
    gameState.moveHistory.push({x, y, player: gameState.currentPlayer});
    gameState.redoHistory = [];
    
    // 绘制棋子
    drawPiece(x, y, gameState.currentPlayer);
    
    // 更新UI
    updateMoveCount();
    
    // 检查胜负
    if (checkWin(x, y, gameState.currentPlayer)) {
        gameOver(gameState.currentPlayer);
        return true;
    }
    
    // 检查平局
    if (isBoardFull()) {
        gameOver(0); // 0表示平局
        return true;
    }
    
    // 切换玩家
    gameState.currentPlayer = gameState.currentPlayer === 1 ? 2 : 1;
    updateGameStatus();
    
    // 如果是人机对战且当前是AI回合，AI落子
    if (gameState.gameMode === 'ai' && gameState.currentPlayer === 2) {
        setTimeout(() => {
            aiMove();
        }, 500);
    }
    
    return true;
}

// 检查胜负
function checkWin(x, y, player) {
    const directions = [
        [1, 0],   // 水平
        [0, 1],   // 垂直
        [1, 1],   // 对角线
        [1, -1]   // 反对角线
    ];
    
    for (const [dx, dy] of directions) {
        let count = 1;
        
        // 向一个方向检查
        for (let i = 1; i < CONFIG.winCount; i++) {
            const nx = x + dx * i;
            const ny = y + dy * i;
            if (nx < 0 || nx >= CONFIG.boardSize || ny < 0 || ny >= CONFIG.boardSize || gameState.board[nx][ny] !== player) {
                break;
            }
            count++;
        }
        
        // 向相反方向检查
        for (let i = 1; i < CONFIG.winCount; i++) {
            const nx = x - dx * i;
            const ny = y - dy * i;
            if (nx < 0 || nx >= CONFIG.boardSize || ny < 0 || ny >= CONFIG.boardSize || gameState.board[nx][ny] !== player) {
                break;
            }
            count++;
        }
        
        if (count >= CONFIG.winCount) {
            // 绘制胜利连线
            drawWinLine(x, y, dx, dy, count);
            return true;
        }
    }
    
    return false;
}

// 绘制胜利连线
function drawWinLine(x, y, dx, dy, count) {
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    
    const startX = x - dx * (count - 1);
    const startY = y - dy * (count - 1);
    const endX = x + dx * (count - 1);
    const endY = y + dy * (count - 1);
    
    ctx.strokeStyle = '#f00';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(
        CONFIG.cellSize / 2 + startX * CONFIG.cellSize,
        CONFIG.cellSize / 2 + startY * CONFIG.cellSize
    );
    ctx.lineTo(
        CONFIG.cellSize / 2 + endX * CONFIG.cellSize,
        CONFIG.cellSize / 2 + endY * CONFIG.cellSize
    );
    ctx.stroke();
}

// 检查棋盘是否已满
function isBoardFull() {
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] === 0) {
                return false;
            }
        }
    }
    return true;
}

// 游戏结束
function gameOver(winner) {
    gameState.isGameOver = true;
    clearInterval(gameState.timerInterval);
    
    const gameOverElement = document.getElementById('game-over');
    const gameOverMessage = document.getElementById('game-over-message');
    
    if (winner === 0) {
        gameOverMessage.textContent = '平局！';
        gameState.stats.draws++;
    } else {
        gameOverMessage.textContent = `${winner === 1 ? '黑棋' : '白棋'}获胜！`;
        if (gameState.gameMode === 'ai') {
            if (winner === 1) {
                gameState.stats.wins++;
            } else {
                gameState.stats.losses++;
            }
        }
    }
    
    gameOverElement.classList.remove('hidden');
    updateStats();
    saveGameData();
}

// AI落子
function aiMove() {
    let move;
    
    switch (gameState.aiDifficulty) {
        case 'easy':
            move = getRandomMove();
            break;
        case 'medium':
            move = getMediumMove();
            break;
        case 'hard':
            move = getHardMove();
            break;
    }
    
    if (move) {
        makeMove(move.x, move.y);
    }
}

// 随机落子（初级AI）
function getRandomMove() {
    const emptyCells = [];
    
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] === 0) {
                emptyCells.push({x, y});
            }
        }
    }
    
    if (emptyCells.length > 0) {
        const randomIndex = Math.floor(Math.random() * emptyCells.length);
        return emptyCells[randomIndex];
    }
    
    return null;
}

// 简单策略落子（中级AI）
function getMediumMove() {
    // 检查是否有获胜机会
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] === 0) {
                gameState.board[x][y] = 2;
                if (checkWin(x, y, 2)) {
                    gameState.board[x][y] = 0;
                    return {x, y};
                }
                gameState.board[x][y] = 0;
            }
        }
    }
    
    // 检查是否需要防守
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] === 0) {
                gameState.board[x][y] = 1;
                if (checkWin(x, y, 1)) {
                    gameState.board[x][y] = 0;
                    return {x, y};
                }
                gameState.board[x][y] = 0;
            }
        }
    }
    
    // 优先在中心区域落子
    const centerArea = [
        {x: 6, y: 6}, {x: 6, y: 7}, {x: 6, y: 8},
        {x: 7, y: 6}, {x: 7, y: 7}, {x: 7, y: 8},
        {x: 8, y: 6}, {x: 8, y: 7}, {x: 8, y: 8}
    ];
    
    for (const cell of centerArea) {
        if (gameState.board[cell.x][cell.y] === 0) {
            return cell;
        }
    }
    
    // 随机落子
    return getRandomMove();
}

// 深度策略落子（高级AI）
function getHardMove() {
    // 简化版的极大极小算法
    let bestScore = -Infinity;
    let bestMove = null;
    
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (gameState.board[x][y] === 0) {
                gameState.board[x][y] = 2;
                const score = minimax(gameState.board, 0, false);
                gameState.board[x][y] = 0;
                
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = {x, y};
                }
            }
        }
    }
    
    return bestMove || getMediumMove();
}

// 极小极大算法
function minimax(board, depth, isMaximizing) {
    // 检查游戏状态
    for (let x = 0; x < CONFIG.boardSize; x++) {
        for (let y = 0; y < CONFIG.boardSize; y++) {
            if (board[x][y] === 2 && checkWin(x, y, 2)) {
                return 100 - depth;
            }
            if (board[x][y] === 1 && checkWin(x, y, 1)) {
                return depth - 100;
            }
        }
    }
    
    if (isBoardFull() || depth >= 3) {
        return 0;
    }
    
    if (isMaximizing) {
        let bestScore = -Infinity;
        for (let x = 0; x < CONFIG.boardSize; x++) {
            for (let y = 0; y < CONFIG.boardSize; y++) {
                if (board[x][y] === 0) {
                    board[x][y] = 2;
                    const score = minimax(board, depth + 1, false);
                    board[x][y] = 0;
                    bestScore = Math.max(score, bestScore);
                }
            }
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for (let x = 0; x < CONFIG.boardSize; x++) {
            for (let y = 0; y < CONFIG.boardSize; y++) {
                if (board[x][y] === 0) {
                    board[x][y] = 1;
                    const score = minimax(board, depth + 1, true);
                    board[x][y] = 0;
                    bestScore = Math.min(score, bestScore);
                }
            }
        }
        return bestScore;
    }
}

// 悔棋
function undoMove() {
    if (gameState.moveHistory.length === 0 || gameState.isGameOver) return;
    
    const lastMove = gameState.moveHistory.pop();
    gameState.board[lastMove.x][lastMove.y] = 0;
    gameState.redoHistory.push(lastMove);
    gameState.currentPlayer = lastMove.player;
    gameState.moveCount--;
    
    drawBoard();
    updateGameStatus();
    updateMoveCount();
    enableButtons();
}

// 撤销悔棋
function redoMove() {
    if (gameState.redoHistory.length === 0 || gameState.isGameOver) return;
    
    const move = gameState.redoHistory.pop();
    gameState.board[move.x][move.y] = move.player;
    gameState.moveHistory.push(move);
    gameState.currentPlayer = move.player === 1 ? 2 : 1;
    gameState.moveCount++;
    
    drawBoard();
    updateGameStatus();
    updateMoveCount();
    enableButtons();
}

// 重新开始游戏
function restartGame() {
    if (confirm('确定要重新开始游戏吗？')) {
        initGame();
    }
}

// 开始游戏
function startGame() {
    if (!gameState.startTime) {
        gameState.startTime = Date.now();
        startTimer();
    }
    gameState.isPaused = false;
    updateGameStatus();
    enableButtons();
}

// 暂停游戏
function pauseGame() {
    gameState.isPaused = true;
    clearInterval(gameState.timerInterval);
    updateGameStatus();
    enableButtons();
}

// 开始计时
function startTimer() {
    gameState.timerInterval = setInterval(() => {
        if (!gameState.isPaused && !gameState.isGameOver) {
            gameState.elapsedTime = Math.floor((Date.now() - gameState.startTime) / 1000);
            updateTimer();
        }
    }, 1000);
}

// 重置计时
function resetTimer() {
    clearInterval(gameState.timerInterval);
    gameState.startTime = null;
    gameState.elapsedTime = 0;
    updateTimer();
}

// 更新计时器
function updateTimer() {
    const minutes = Math.floor(gameState.elapsedTime / 60);
    const seconds = gameState.elapsedTime % 60;
    document.getElementById('timer').textContent = `时间: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// 更新游戏状态
function updateGameStatus() {
    const currentPlayerElement = document.getElementById('current-player');
    const gameStatusElement = document.getElementById('game-status');
    
    currentPlayerElement.innerHTML = `当前玩家: <span class="${gameState.currentPlayer === 1 ? 'text-black' : 'text-white bg-black px-1 rounded'}">${gameState.currentPlayer === 1 ? '黑棋' : '白棋'}</span>`;
    
    if (gameState.isGameOver) {
        gameStatusElement.textContent = '游戏状态: 游戏结束';
    } else if (gameState.isPaused) {
        gameStatusElement.textContent = '游戏状态: 已暂停';
    } else if (!gameState.startTime) {
        gameStatusElement.textContent = '游戏状态: 准备开始';
    } else {
        gameStatusElement.textContent = '游戏状态: 进行中';
    }
}

// 更新步数
function updateMoveCount() {
    document.getElementById('move-count').textContent = `步数: ${gameState.moveCount}`;
}

// 更新战绩
function updateStats() {
    document.getElementById('wins').textContent = gameState.stats.wins;
    document.getElementById('losses').textContent = gameState.stats.losses;
    document.getElementById('draws').textContent = gameState.stats.draws;
}

// 启用/禁用按钮
function enableButtons() {
    document.getElementById('undo-move').disabled = gameState.moveHistory.length === 0 || gameState.isGameOver;
    document.getElementById('redo-move').disabled = gameState.redoHistory.length === 0 || gameState.isGameOver;
    document.getElementById('start-game').disabled = gameState.isGameOver;
}

// 保存游戏数据
function saveGameData() {
    localStorage.setItem('gobangGameState', JSON.stringify(gameState));
}

// 加载游戏数据
function loadGameData() {
    const savedState = localStorage.getItem('gobangGameState');
    if (savedState) {
        try {
            const parsedState = JSON.parse(savedState);
            gameState = { ...gameState, ...parsedState };
            updateStats();
            drawBoard();
            updateGameStatus();
            updateMoveCount();
            updateTimer();
            enableButtons();
        } catch (e) {
            console.error('加载游戏数据失败:', e);
        }
    }
}

// 切换主题
function toggleTheme() {
    gameState.isDarkTheme = !gameState.isDarkTheme;
    document.body.classList.toggle('dark-theme', gameState.isDarkTheme);
    saveGameData();
}

// 切换棋盘风格
function setBoardStyle(style) {
    gameState.boardStyle = style;
    const board = document.getElementById('board');
    
    // 移除所有棋盘风格类
    board.classList.remove('board-wood', 'board-modern');
    
    // 添加选中的棋盘风格类
    if (style === 'wood') {
        board.classList.add('board-wood');
    } else if (style === 'modern') {
        board.classList.add('board-modern');
    }
    
    saveGameData();
}

// 切换棋子样式
function setPieceStyle(style) {
    gameState.pieceStyle = style;
    drawBoard();
    saveGameData();
}

// 切换游戏模式
function setGameMode(mode) {
    gameState.gameMode = mode;
    
    // 显示/隐藏AI难度选择
    const aiDifficultyElement = document.getElementById('ai-difficulty');
    if (mode === 'ai') {
        aiDifficultyElement.classList.remove('hidden');
    } else {
        aiDifficultyElement.classList.add('hidden');
    }
    
    // 重置游戏
    initGame();
    saveGameData();
}

// 设置AI难度
function setAiDifficulty(difficulty) {
    gameState.aiDifficulty = difficulty;
    saveGameData();
}

// 显示教程
function showTutorial() {
    document.getElementById('tutorial-modal').classList.remove('hidden');
}

// 隐藏教程
function hideTutorial() {
    document.getElementById('tutorial-modal').classList.add('hidden');
}

// 初始化事件监听
function initEventListeners() {
    // 棋盘点击事件
    const canvas = document.getElementById('board');
    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = Math.round((e.clientX - rect.left - CONFIG.cellSize / 2) / CONFIG.cellSize);
        const y = Math.round((e.clientY - rect.top - CONFIG.cellSize / 2) / CONFIG.cellSize);
        makeMove(x, y);
    });
    
    // 悬停预览效果
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = Math.round((e.clientX - rect.left - CONFIG.cellSize / 2) / CONFIG.cellSize);
        const y = Math.round((e.clientY - rect.top - CONFIG.cellSize / 2) / CONFIG.cellSize);
        
        // 清除之前的预览
        const existingPreview = document.querySelector('.hover-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // 创建新的预览
        if (isLegalMove(x, y) && !gameState.isGameOver && !gameState.isPaused) {
            const preview = document.createElement('div');
            preview.className = 'hover-preview';
            preview.style.width = `${CONFIG.pieceRadius * 2}px`;
            preview.style.height = `${CONFIG.pieceRadius * 2}px`;
            preview.style.left = `${rect.left + CONFIG.cellSize / 2 + x * CONFIG.cellSize - CONFIG.pieceRadius}px`;
            preview.style.top = `${rect.top + CONFIG.cellSize / 2 + y * CONFIG.cellSize - CONFIG.pieceRadius}px`;
            preview.style.backgroundColor = gameState.currentPlayer === 1 ? 'rgba(51, 51, 51, 0.5)' : 'rgba(255, 255, 255, 0.5)';
            document.body.appendChild(preview);
        }
    });
    
    // 鼠标离开棋盘时清除预览
    canvas.addEventListener('mouseleave', () => {
        const existingPreview = document.querySelector('.hover-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
    });
    
    // 游戏控制按钮
    document.getElementById('start-game').addEventListener('click', startGame);
    document.getElementById('restart-game').addEventListener('click', restartGame);
    document.getElementById('undo-move').addEventListener('click', undoMove);
    document.getElementById('redo-move').addEventListener('click', redoMove);
    document.getElementById('save-game').addEventListener('click', saveGameData);
    document.getElementById('load-game').addEventListener('click', loadGameData);
    
    // 游戏模式按钮
    document.getElementById('mode-human').addEventListener('click', () => setGameMode('human'));
    document.getElementById('mode-ai').addEventListener('click', () => setGameMode('ai'));
    document.getElementById('mode-online').addEventListener('click', () => setGameMode('online'));
    
    // AI难度按钮
    document.getElementById('ai-easy').addEventListener('click', () => setAiDifficulty('easy'));
    document.getElementById('ai-medium').addEventListener('click', () => setAiDifficulty('medium'));
    document.getElementById('ai-hard').addEventListener('click', () => setAiDifficulty('hard'));
    
    // 棋盘风格按钮
    document.getElementById('board-classic').addEventListener('click', () => setBoardStyle('classic'));
    document.getElementById('board-wood').addEventListener('click', () => setBoardStyle('wood'));
    document.getElementById('board-modern').addEventListener('click', () => setBoardStyle('modern'));
    
    // 棋子样式按钮
    document.getElementById('piece-classic').addEventListener('click', () => setPieceStyle('classic'));
    document.getElementById('piece-glass').addEventListener('click', () => setPieceStyle('glass'));
    document.getElementById('piece-3d').addEventListener('click', () => setPieceStyle('3d'));
    
    // 主题切换按钮
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    
    // 教程按钮
    document.getElementById('tutorial-btn').addEventListener('click', showTutorial);
    document.getElementById('close-tutorial').addEventListener('click', hideTutorial);
    document.getElementById('close-tutorial-btn').addEventListener('click', hideTutorial);
    
    // 再玩一局按钮
    document.getElementById('play-again').addEventListener('click', () => {
        document.getElementById('game-over').classList.add('hidden');
        initGame();
    });
}

// 初始化游戏
window.onload = function() {
    initGame();
    initEventListeners();
};