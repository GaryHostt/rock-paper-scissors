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
const winningHandContainer = document.getElementById('winning-hand-container');
const winningEmojiEl = document.getElementById('winning-emoji');
const statsPanel = document.getElementById('stats-panel');
const closeStatsBtn = document.getElementById('close-stats-btn');
const difficultyBtns = document.querySelectorAll('.difficulty-btn');

// Menu elements
const menuToggleBtn = document.getElementById('menu-toggle-btn');
const leftSidebar = document.getElementById('left-sidebar');
const closeSidebarBtn = document.getElementById('close-sidebar-btn');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const themeSelect = document.getElementById('theme-select');
const autoPlayerDifficultySelect = document.getElementById('auto-player-difficulty');
const autoPlaySpeedSelect = document.getElementById('auto-play-speed');
const showStatsBtn = document.getElementById('show-stats-btn');
const showTrendsBtn = document.getElementById('show-trends-btn');
const menuResetBtn = document.getElementById('menu-reset-btn');
const menuAutoPlayBtn = document.getElementById('menu-auto-play-btn');
const showAnalysisBtn = document.getElementById('show-analysis-btn');
const aiAnalysisContent = document.getElementById('ai-analysis-content');

// Pattern sidebar (now used in menu)
const patternMessages = document.getElementById('pattern-messages');
const strategyMessages = document.getElementById('strategy-messages');
const patternMessagesMenu = document.getElementById('pattern-messages-menu');
const strategyMessagesMenu = document.getElementById('strategy-messages-menu');
const overallWinRateEl = document.getElementById('overall-win-rate');
const rockWinRateEl = document.getElementById('rock-win-rate');
const paperWinRateEl = document.getElementById('paper-win-rate');
const scissorsWinRateEl = document.getElementById('scissors-win-rate');

// Trend modal
const trendModal = document.getElementById('trend-modal');
const closeTrendModal = document.getElementById('close-trend-modal');
const trendChart = document.getElementById('trend-chart');
const totalGamesStat = document.getElementById('total-games-stat');
const currentStreakStat = document.getElementById('current-streak-stat');
const bestStreakStat = document.getElementById('best-streak-stat');

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

// Load streak data
function loadStreaks() {
    const savedBestStreak = localStorage.getItem('rps-best-streak');
    if (savedBestStreak) {
        bestStreak = parseInt(savedBestStreak);
    }
}

// Save streak data
function saveStreaks() {
    localStorage.setItem('rps-best-streak', bestStreak.toString());
}

// Load trend data
function loadTrend() {
    const savedTrend = localStorage.getItem('rps-trend');
    if (savedTrend) {
        trendData = JSON.parse(savedTrend);
    }
}

// Save trend data
function saveTrend() {
    localStorage.setItem('rps-trend', JSON.stringify(trendData));
}

// Load dark mode
function loadDarkMode() {
    const darkMode = localStorage.getItem('rps-dark-mode');
    if (darkMode === 'true') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
}

// Load theme
function loadTheme() {
    const theme = localStorage.getItem('rps-theme');
    if (theme && theme !== 'default') {
        document.body.classList.add(`theme-${theme}`);
        themeSelect.value = theme;
    }
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
    updateWinRates();
}

// Calculate and update win rates
function updateWinRates() {
    // Overall win rate
    const totalGames = scores.player + scores.computer + scores.ties;
    const overallWinRate = totalGames > 0 ? ((scores.player / totalGames) * 100).toFixed(1) : 0;
    overallWinRateEl.textContent = `${overallWinRate}%`;
    
    // Individual hand win rates
    ['rock', 'paper', 'scissors'].forEach(hand => {
        const stats = handStats[hand];
        const total = stats.wins + stats.losses + stats.ties;
        const winRate = total > 0 ? ((stats.wins / total) * 100).toFixed(1) : 0;
        document.getElementById(`${hand}-win-rate`).textContent = `${winRate}%`;
    });
}

// Detect patterns in player behavior
function detectPatterns() {
    if (gameHistory.length < 5) {
        return;
    }
    
    const patterns = [];
    const recentHistory = gameHistory.slice(-10);
    
    // Pattern: Playing same hand after winning
    let repeatAfterWin = 0;
    let winCount = 0;
    for (let i = 1; i < recentHistory.length; i++) {
        if (recentHistory[i-1].result === 'player') {
            winCount++;
            if (recentHistory[i].player === recentHistory[i-1].player) {
                repeatAfterWin++;
            }
        }
    }
    if (winCount >= 3 && repeatAfterWin / winCount > 0.6) {
        patterns.push(`You tend to repeat your choice after winning (${((repeatAfterWin/winCount)*100).toFixed(0)}%)`);
    }
    
    // Pattern: Playing same hand after losing
    let repeatAfterLoss = 0;
    let lossCount = 0;
    for (let i = 1; i < recentHistory.length; i++) {
        if (recentHistory[i-1].result === 'computer') {
            lossCount++;
            if (recentHistory[i].player === recentHistory[i-1].player) {
                repeatAfterLoss++;
            }
        }
    }
    if (lossCount >= 3 && repeatAfterLoss / lossCount > 0.6) {
        patterns.push(`You tend to repeat your choice after losing (${((repeatAfterLoss/lossCount)*100).toFixed(0)}%)`);
    }
    
    // Pattern: Favorite hand
    const handCounts = {};
    recentHistory.forEach(game => {
        handCounts[game.player] = (handCounts[game.player] || 0) + 1;
    });
    const favorite = Object.keys(handCounts).reduce((a, b) => handCounts[a] > handCounts[b] ? a : b);
    const favoritePercent = (handCounts[favorite] / recentHistory.length * 100).toFixed(0);
    if (favoritePercent > 40) {
        patterns.push(`You play ${favorite} more often than other hands (${favoritePercent}%)`);
    }
    
    // Update both UIs (menu and sidebar if visible)
    const patternHTML = patterns.length > 0 
        ? patterns.map(p => `<div class="pattern-message">${p}</div>`).join('')
        : '<p class="pattern-placeholder">No clear patterns detected yet...</p>';
    
    if (patternMessagesMenu) patternMessagesMenu.innerHTML = patternHTML;
    if (patternMessages) patternMessages.innerHTML = patternHTML;
}

// Generate strategy suggestions
function generateStrategies() {
    if (gameHistory.length < 5) {
        return;
    }
    
    const strategies = [];
    const recent = gameHistory.slice(-5);
    
    // Analyze computer's recent plays
    const computerCounts = {};
    recent.forEach(game => {
        computerCounts[game.computer] = (computerCounts[game.computer] || 0) + 1;
    });
    
    // Suggest counter to computer's most common
    const computerFavorite = Object.keys(computerCounts).reduce((a, b) => 
        computerCounts[a] > computerCounts[b] ? a : b
    );
    
    const counters = {
        rock: 'paper',
        paper: 'scissors',
        scissors: 'rock'
    };
    
    strategies.push(`Computer recently favored ${computerFavorite}. Try ${counters[computerFavorite]}!`);
    
    // Check if player is in a losing streak
    if (currentStreak < -2 && currentStreakType === 'loss') {
        strategies.push(`You're in a losing streak. Try changing your strategy!`);
    }
    
    // Analyze win rates
    const bestHand = Object.keys(handStats).reduce((a, b) => {
        const aRate = handStats[a].wins / (handStats[a].wins + handStats[a].losses + 1);
        const bRate = handStats[b].wins / (handStats[b].wins + handStats[b].losses + 1);
        return aRate > bRate ? a : b;
    });
    
    if (handStats[bestHand].wins > 3) {
        strategies.push(`Your best hand is ${bestHand}. But the AI may have noticed!`);
    }
    
    // Update both UIs
    const strategyHTML = strategies.length > 0
        ? strategies.map(s => `<div class="strategy-message">${s}</div>`).join('')
        : '<p class="strategy-placeholder">Strategies will appear here...</p>';
    
    if (strategyMessagesMenu) strategyMessagesMenu.innerHTML = strategyHTML;
    if (strategyMessages) strategyMessages.innerHTML = strategyHTML;
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
        // In auto-play mode, use the auto-player difficulty for the player's choice
        // The opponent (computer) will use the regular difficulty setting
        const requestData = {
            choice: playerChoice,
            difficulty: currentDifficulty, // This is the opponent's difficulty
            history: gameHistory.slice(-10)
        };
        
        const response = await fetch('/api/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
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
        
        // Update streak
        if (data.result === 'player') {
            if (currentStreakType === 'win') {
                currentStreak++;
            } else {
                currentStreak = 1;
                currentStreakType = 'win';
            }
        } else if (data.result === 'computer') {
            if (currentStreakType === 'loss') {
                currentStreak--;
            } else {
                currentStreak = -1;
                currentStreakType = 'loss';
            }
        }
        
        // Update best streak
        if (Math.abs(currentStreak) > Math.abs(bestStreak)) {
            bestStreak = currentStreak;
            saveStreaks();
        }
        
        // Add to trend data
        trendData.push({
            player: scores.player,
            computer: scores.computer
        });
        // Keep last 50 data points
        if (trendData.length > 50) {
            trendData.shift();
        }
        saveTrend();
        
        // Detect patterns
        detectPatterns();
        generateStrategies();
        
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
    trendData = [];
    currentStreak = 0;
    currentStreakType = null;
    bestStreak = 0;
    updateScoreDisplay();
    updateHandStatsDisplay();
    updateWinRates();
    saveScores();
    saveHandStats();
    saveTrend();
    saveStreaks();
    resultMessage.textContent = 'Scores reset! Choose your move!';
    resultMessage.classList.remove('win', 'lose', 'tie');
    battleDisplay.innerHTML = '';
    winningHandContainer.classList.remove('visible');
    winningEmojiEl.textContent = '?';
    
    // Reset pattern displays
    const resetPattern = '<p class="pattern-placeholder">Play a few rounds for AI analysis...</p>';
    const resetStrategy = '<p class="strategy-placeholder">Strategies will appear here...</p>';
    if (patternMessages) patternMessages.innerHTML = resetPattern;
    if (strategyMessages) strategyMessages.innerHTML = resetStrategy;
    if (patternMessagesMenu) patternMessagesMenu.innerHTML = resetPattern;
    if (strategyMessagesMenu) strategyMessagesMenu.innerHTML = resetStrategy;
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
        hard: 'Hard mode: Computer predicts your moves! 😈',
        veryhard: 'Very Hard mode: Master strategist with advanced psychology! 👹'
    };
    
    resultMessage.textContent = difficultyMessages[difficulty];
    resultMessage.classList.remove('win', 'lose', 'tie');
}

// Toggle menu sidebar
function toggleMenu() {
    leftSidebar.classList.toggle('open');
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('rps-dark-mode', isDark.toString());
}

// Change theme
function changeTheme(theme) {
    // Remove all theme classes
    document.body.classList.remove('theme-halloween', 'theme-christmas', 'theme-spring', 'theme-ocean');
    
    // Add new theme
    if (theme !== 'default') {
        document.body.classList.add(`theme-${theme}`);
    }
    
    localStorage.setItem('rps-theme', theme);
}

// Show trend graph modal
function showTrendGraph() {
    trendModal.classList.add('open');
    
    // Update stats
    totalGamesStat.textContent = scores.player + scores.computer + scores.ties;
    currentStreakStat.textContent = currentStreak >= 0 ? `+${currentStreak}` : currentStreak;
    bestStreakStat.textContent = bestStreak >= 0 ? `+${bestStreak}` : bestStreak;
    
    // Draw chart
    setTimeout(() => {
        drawTrendChart(trendChart, trendData);
    }, 100);
}

// Close trend modal
function closeTrendGraphModal() {
    trendModal.classList.remove('open');
}

// Toggle auto-play mode
function toggleAutoPlay() {
    autoPlayActive = !autoPlayActive;
    
    if (autoPlayActive) {
        // Start auto-play
        menuAutoPlayBtn.textContent = '⏸️ Stop Auto-Play';
        menuAutoPlayBtn.classList.add('active');
        
        // Disable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = true);
        difficultyBtns.forEach(btn => btn.disabled = true);
        
        // Get auto-play settings
        autoPlayerDifficulty = autoPlayerDifficultySelect.value;
        const speedSetting = autoPlaySpeedSelect.value;
        const speeds = { slow: 2000, normal: 1500, fast: 800, turbo: 300 };
        autoPlaySpeed = speeds[speedSetting] || 1500;
        
        // Start the auto-play loop
        startAutoPlay();
    } else {
        // Stop auto-play
        menuAutoPlayBtn.textContent = '▶️ Start Auto-Play';
        menuAutoPlayBtn.classList.remove('active');
        
        // Re-enable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = false);
        difficultyBtns.forEach(btn => btn.disabled = false);
        
        // Stop the auto-play loop
        stopAutoPlay();
    }
}

// Toggle AI analysis visibility
function toggleAnalysis() {
    const isVisible = aiAnalysisContent.style.display !== 'none';
    aiAnalysisContent.style.display = isVisible ? 'none' : 'block';
    showAnalysisBtn.textContent = isVisible ? 'View Pattern Analysis' : 'Hide Pattern Analysis';
}

// Start auto-play loop
function startAutoPlay() {
    const choices = ['rock', 'paper', 'scissors'];
    
    // Play immediately
    playAutoRound();
    
    // Then continue playing at intervals
    autoPlayInterval = setInterval(() => {
        playAutoRound();
    }, autoPlaySpeed);
}

// Play one auto round
function playAutoRound() {
    if (!autoPlayActive) return;
    
    const choices = ['rock', 'paper', 'scissors'];
    let playerChoice;
    
    // Use AI to select player's choice based on auto-player difficulty
    if (autoPlayerDifficulty === 'easy') {
        playerChoice = choices[Math.floor(Math.random() * choices.length)];
    } else if (autoPlayerDifficulty === 'medium' && gameHistory.length >= 3) {
        // Auto-player analyzes opponent (computer) patterns
        const opponentChoices = gameHistory.slice(-10).map(g => g.computer);
        const counts = {};
        opponentChoices.forEach(c => counts[c] = (counts[c] || 0) + 1);
        const mostCommon = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
        
        // Counter the opponent's most common choice 70% of the time
        const counters = { rock: 'paper', paper: 'scissors', scissors: 'rock' };
        playerChoice = Math.random() < 0.7 ? counters[mostCommon] : choices[Math.floor(Math.random() * choices.length)];
    } else if (autoPlayerDifficulty === 'hard' && gameHistory.length >= 5) {
        // Advanced auto-player strategy
        const recent = gameHistory.slice(-5);
        const lastGame = recent[recent.length - 1];
        
        // Analyze opponent's patterns
        const opponentChoices = recent.map(g => g.computer);
        const counts = {};
        opponentChoices.forEach(c => counts[c] = (counts[c] || 0) + 1);
        
        // Check if opponent repeats after winning
        if (lastGame.result === 'computer' && Math.random() < 0.6) {
            const counters = { rock: 'paper', paper: 'scissors', scissors: 'rock' };
            playerChoice = counters[lastGame.computer];
        } else if (lastGame.result === 'player' && Math.random() < 0.6) {
            // Check if opponent switches after losing
            const nextInSequence = { rock: 'paper', paper: 'scissors', scissors: 'rock' };
            const predicted = nextInSequence[lastGame.computer];
            const counters = { rock: 'paper', paper: 'scissors', scissors: 'rock' };
            playerChoice = counters[predicted];
        } else {
            // Counter most common
            const mostCommon = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
            const counters = { rock: 'paper', paper: 'scissors', scissors: 'rock' };
            playerChoice = counters[mostCommon];
        }
    } else {
        playerChoice = choices[Math.floor(Math.random() * choices.length)];
    }
    
    playGame(playerChoice, true);
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

// Menu event listeners
menuToggleBtn.addEventListener('click', toggleMenu);
closeSidebarBtn.addEventListener('click', toggleMenu);
darkModeToggle.addEventListener('click', toggleDarkMode);
themeSelect.addEventListener('change', (e) => changeTheme(e.target.value));
showAnalysisBtn.addEventListener('click', toggleAnalysis);
showStatsBtn.addEventListener('click', () => {
    statsPanel.classList.toggle('open');
    toggleMenu(); // Close menu after opening stats
});
showTrendsBtn.addEventListener('click', () => {
    showTrendGraph();
    toggleMenu(); // Close menu after opening trend
});
menuResetBtn.addEventListener('click', () => {
    resetScores();
    toggleMenu(); // Close menu after reset
});
menuAutoPlayBtn.addEventListener('click', toggleAutoPlay);

// Stats panel
closeStatsBtn.addEventListener('click', () => {
    statsPanel.classList.remove('open');
});

// Trend modal
closeTrendModal.addEventListener('click', closeTrendGraphModal);
trendModal.addEventListener('click', (e) => {
    if (e.target === trendModal) {
        closeTrendGraphModal();
    }
});

// Difficulty button listeners
difficultyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const difficulty = btn.dataset.difficulty;
        setDifficulty(difficulty);
    });
});

// Load all saved data on page load
loadScores();
loadHandStats();
loadDifficulty();
loadStreaks();
loadTrend();
loadDarkMode();
loadTheme();
updateWinRates();

