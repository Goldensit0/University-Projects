
// Variables globales para el Tres en Raya
const boardElement = document.getElementById('board');
const messageElement = document.getElementById('message');
let currentPlayer = 'X';
let board = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;

// Configuración inicial del tablero
function createBoard() {
    boardElement.innerHTML = '';
    board.forEach((cell, index) => {
        const cellElement = document.createElement('div');
        cellElement.classList.add('cell');
        cellElement.dataset.index = index;
        cellElement.addEventListener('click', handleCellClick);
        boardElement.appendChild(cellElement);
    });
}

// Maneja el clic en una celda
function handleCellClick(event) {
    const index = event.target.dataset.index;

    if (board[index] !== '' || !gameActive) {
        return;
    }

    board[index] = currentPlayer;
    event.target.textContent = currentPlayer;
    event.target.classList.add('disabled');

    if (checkWinner()) {
        gameActive = false;
        messageElement.textContent = `¡El jugador ${currentPlayer} ha ganado!`;
    } else if (board.every(cell => cell !== '')) {
        gameActive = false;
        messageElement.textContent = '¡Empate!';
    } else {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        messageElement.textContent = `Turno del jugador ${currentPlayer}`;
    }
}

// Verifica si hay un ganador
function checkWinner() {
    const winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columnas
        [0, 4, 8], [2, 4, 6]             // Diagonales
    ];

    return winningCombinations.some(combination => {
        const [a, b, c] = combination;
        return board[a] && board[a] === board[b] && board[a] === board[c];
    });
}

// Reinicia el juego
function resetGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    currentPlayer = 'X';
    messageElement.textContent = `Turno del jugador ${currentPlayer}`;
    createBoard();
}