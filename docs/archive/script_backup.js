// Game state
let scores = {
    player: 0,
    computer: 0,
    ties: 0
};

// Hand statistics
let handStats = {
    rock: { wins: 0, losses: 0, ties: 0 },
    paper: { wins: 0, losses: 0, ties: 0 },
    scissors: { wins: 0, losses: 0, ties: 0 }
};

// Game in progress flag
let gameInProgress = false;

// Auto-play mode
let autoPlayActive = false;
let autoPlayInterval = null;
let autoPlayerDifficulty = 'easy';
let autoPlaySpeed = 1500;

// Difficulty level
let currentDifficulty = 'easy';

// Game history for AI
let gameHistory = [];

// Streak tracking
let currentStreak = 0;
let currentStreakType = null; // 'win' or 'loss'
let bestStreak = 0;

// Trend data
let trendData = [];

// Emoji mapping
const emojiMap = {
    rock: '✊',
    paper: '✋',
    scissors: '✌️'
};

// DOM elements
const choiceBtns = document.querySelectorAll('.choice-btn');
const resultMessage = document.getElementById('result-message');
const battleDisplay = document.getElementById('battle-display');
const playerScoreEl = document.getElementById('player-score');
const computerScoreEl = document.getElementById('computer-score');
const tieScoreEl = document.getElementById('tie-score');
const resetBtn = document.getElementById('reset-btn');
const winningHandContainer = document.getElementById('winning-hand-container');
const winningEmojiEl = document.getElementById('winning-emoji');
const statsBtn = document.getElementById('stats-btn');
const statsPanel = document.getElementById('stats-panel');
const closeStatsBtn = document.getElementById('close-stats-btn');
const autoPlayBtn = document.getElementById('auto-play-btn');
const difficultyBtns = document.querySelectorAll('.difficulty-btn');

// Load scores from localStorage
function loadScores() {
    const savedScores = localStorage.getItem('rps-scores');
    if (savedScores) {
        scores = JSON.parse(savedScores);
        updateScoreDisplay();
    }
}

// Save scores to localStorage
function saveScores() {
    localStorage.setItem('rps-scores', JSON.stringify(scores));
}

// Load hand statistics from localStorage
function loadHandStats() {
    const savedStats = localStorage.getItem('rps-hand-stats');
    if (savedStats) {
        handStats = JSON.parse(savedStats);
        updateHandStatsDisplay();
    }
}

// Save hand statistics to localStorage
function saveHandStats() {
    localStorage.setItem('rps-hand-stats', JSON.stringify(handStats));
}

// Load difficulty from localStorage
function loadDifficulty() {
    const savedDifficulty = localStorage.getItem('rps-difficulty');
    if (savedDifficulty) {
        currentDifficulty = savedDifficulty;
        updateDifficultyDisplay();
    }
}

// Save difficulty to localStorage
function saveDifficulty() {
    localStorage.setItem('rps-difficulty', currentDifficulty);
}

// Update difficulty button display
function updateDifficultyDisplay() {
    difficultyBtns.forEach(btn => {
        if (btn.dataset.difficulty === currentDifficulty) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Update hand statistics display
function updateHandStatsDisplay() {
    // Rock stats
    document.getElementById('rock-wins').textContent = handStats.rock.wins;
    document.getElementById('rock-losses').textContent = handStats.rock.losses;
    document.getElementById('rock-ties').textContent = handStats.rock.ties;
    document.getElementById('rock-total').textContent = handStats.rock.wins + handStats.rock.losses + handStats.rock.ties;
    
    // Paper stats
    document.getElementById('paper-wins').textContent = handStats.paper.wins;
    document.getElementById('paper-losses').textContent = handStats.paper.losses;
    document.getElementById('paper-ties').textContent = handStats.paper.ties;
    document.getElementById('paper-total').textContent = handStats.paper.wins + handStats.paper.losses + handStats.paper.ties;
    
    // Scissors stats
    document.getElementById('scissors-wins').textContent = handStats.scissors.wins;
    document.getElementById('scissors-losses').textContent = handStats.scissors.losses;
    document.getElementById('scissors-ties').textContent = handStats.scissors.ties;
    document.getElementById('scissors-total').textContent = handStats.scissors.wins + handStats.scissors.losses + handStats.scissors.ties;
}

// Update hand statistics based on game result
function updateHandStats(playerChoice, result) {
    if (result === 'player') {
        handStats[playerChoice].wins++;
    } else if (result === 'computer') {
        handStats[playerChoice].losses++;
    } else if (result === 'tie') {
        handStats[playerChoice].ties++;
    }
    
    saveHandStats();
    updateHandStatsDisplay();
}

// Update score display
function updateScoreDisplay() {
    playerScoreEl.textContent = scores.player;
    computerScoreEl.textContent = scores.computer;
    tieScoreEl.textContent = scores.ties;
}

// Display winning hand
function displayWinningHand(winningHand) {
    if (winningHand === null) {
        // For ties, show both hands tied
        winningEmojiEl.textContent = '🤝';
        winningHandContainer.classList.add('visible');
    } else {
        // Show the winning hand with emoji
        winningEmojiEl.textContent = emojiMap[winningHand];
        winningHandContainer.classList.add('visible');
    }
}

// Play game
async function playGame(playerChoice, isAutoPlay = false) {
    // Prevent multiple simultaneous games
    if (gameInProgress) {
        return;
    }
    
    // Set game in progress flag
    gameInProgress = true;
    
    // Disable buttons during game (unless auto-play)
    if (!isAutoPlay) {
        choiceBtns.forEach(btn => btn.disabled = true);
    }
    
    // Highlight selected choice (only in manual mode)
    if (!isAutoPlay) {
        choiceBtns.forEach(btn => btn.classList.remove('selected'));
        event.target.closest('.choice-btn').classList.add('selected');
    }
    
    try {
        const response = await fetch('/api/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                choice: playerChoice,
                difficulty: currentDifficulty,
                history: gameHistory.slice(-10) // Send last 10 games for pattern analysis
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultMessage.textContent = data.error;
            return;
        }
        
        // Display battle
        battleDisplay.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-top: 10px;">
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">You</div>
                    <span class="battle-emoji">${emojiMap[data.player_choice]}</span>
                </div>
                <div style="font-size: 2rem; color: #667eea;">VS</div>
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">Computer</div>
                    <span class="battle-emoji">${emojiMap[data.computer_choice]}</span>
                </div>
            </div>
        `;
        
        // Update result message
        resultMessage.classList.remove('win', 'lose', 'tie');
        
        let winningHand = null;
        
        if (data.result === 'player') {
            resultMessage.textContent = '🎉 You Win!';
            resultMessage.classList.add('win');
            scores.player++;
            winningHand = data.player_choice;
        } else if (data.result === 'computer') {
            resultMessage.textContent = '😢 You Lose!';
            resultMessage.classList.add('lose');
            scores.computer++;
            winningHand = data.computer_choice;
        } else {
            resultMessage.textContent = '🤝 It\'s a Tie!';
            resultMessage.classList.add('tie');
            scores.ties++;
            winningHand = null; // No winner in a tie
        }
        
        // Display winning hand
        displayWinningHand(winningHand);
        
        // Update hand statistics
        updateHandStats(data.player_choice, data.result);
        
        // Add to game history for AI learning
        gameHistory.push({
            player: data.player_choice,
            computer: data.computer_choice,
            result: data.result
        });
        
        // Keep only last 50 games in history
        if (gameHistory.length > 50) {
            gameHistory.shift();
        }
        
        // Update and save scores
        updateScoreDisplay();
        saveScores();
        
    } catch (error) {
        console.error('Error:', error);
        resultMessage.textContent = 'Error connecting to server!';
    } finally {
        // Re-enable buttons after a short delay
        const delay = isAutoPlay ? 500 : 1000;
        setTimeout(() => {
            if (!isAutoPlay) {
                choiceBtns.forEach(btn => {
                    btn.disabled = false;
                    btn.classList.remove('selected');
                });
            }
            gameInProgress = false;
        }, delay);
    }
}

// Reset scores
function resetScores() {
    scores = {
        player: 0,
        computer: 0,
        ties: 0
    };
    handStats = {
        rock: { wins: 0, losses: 0, ties: 0 },
        paper: { wins: 0, losses: 0, ties: 0 },
        scissors: { wins: 0, losses: 0, ties: 0 }
    };
    gameHistory = []; // Clear game history
    updateScoreDisplay();
    updateHandStatsDisplay();
    saveScores();
    saveHandStats();
    resultMessage.textContent = 'Scores reset! Choose your move!';
    resultMessage.classList.remove('win', 'lose', 'tie');
    battleDisplay.innerHTML = '';
    winningHandContainer.classList.remove('visible');
    winningEmojiEl.textContent = '?';
}

// Toggle statistics panel
function toggleStatsPanel() {
    statsPanel.classList.toggle('open');
    statsBtn.classList.toggle('active');
    
    if (statsPanel.classList.contains('open')) {
        statsBtn.textContent = 'Hide Statistics';
    } else {
        statsBtn.textContent = 'Display Aggregate Statistics';
    }
}

// Set difficulty level
function setDifficulty(difficulty) {
    currentDifficulty = difficulty;
    updateDifficultyDisplay();
    saveDifficulty();
    
    // Show message about difficulty change
    const difficultyMessages = {
        easy: 'Easy mode: Computer plays randomly 🎲',
        medium: 'Medium mode: Computer adapts to your patterns 🤔',
        hard: 'Hard mode: Computer predicts your moves! 😈'
    };
    
    resultMessage.textContent = difficultyMessages[difficulty];
    resultMessage.classList.remove('win', 'lose', 'tie');
}

// Toggle auto-play mode
function toggleAutoPlay() {
    autoPlayActive = !autoPlayActive;
    
    if (autoPlayActive) {
        // Start auto-play
        autoPlayBtn.textContent = '⏸️ Disable Auto-Play Mode';
        autoPlayBtn.classList.add('active');
        
        // Disable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = true);
        difficultyBtns.forEach(btn => btn.disabled = true);
        
        // Start the auto-play loop
        startAutoPlay();
    } else {
        // Stop auto-play
        autoPlayBtn.textContent = '🤖 Enable Auto-Play Mode';
        autoPlayBtn.classList.remove('active');
        
        // Re-enable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = false);
        difficultyBtns.forEach(btn => btn.disabled = false);
        
        // Stop the auto-play loop
        stopAutoPlay();
    }
}

// Start auto-play loop
function startAutoPlay() {
    const choices = ['rock', 'paper', 'scissors'];
    
    // Play immediately
    playAutoRound();
    
    // Then continue playing at intervals
    autoPlayInterval = setInterval(() => {
        playAutoRound();
    }, 1500); // Play every 1.5 seconds
}

// Play one auto round
function playAutoRound() {
    if (!autoPlayActive) return;
    
    const choices = ['rock', 'paper', 'scissors'];
    const randomChoice = choices[Math.floor(Math.random() * choices.length)];
    
    playGame(randomChoice, true);
}

// Stop auto-play loop
function stopAutoPlay() {
    if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
    }
}

// Event listeners
choiceBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const choice = btn.dataset.choice;
        playGame(choice);
    });
});

resetBtn.addEventListener('click', resetScores);

autoPlayBtn.addEventListener('click', toggleAutoPlay);

statsBtn.addEventListener('click', toggleStatsPanel);

closeStatsBtn.addEventListener('click', toggleStatsPanel);

// Difficulty button listeners
difficultyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const difficulty = btn.dataset.difficulty;
        setDifficulty(difficulty);
    });
});

// Load scores, stats, and difficulty on page load
loadScores();
loadHandStats();
loadDifficulty();

