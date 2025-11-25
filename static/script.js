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
let longestWinningStreak = 0;
let longestLosingStreak = 0;

// Trend data
let trendData = [];

// Current language
let currentLanguage = 'en';

// Translation dictionary
const translations = {
    en: {
        // Game interface
        'game.title': 'Rock Paper Scissors',
        'game.you': 'You',
        'game.ties': 'Ties',
        'game.computer': 'Computer',
        'game.opponentDifficulty': 'Opponent Difficulty:',
        'game.chooseMove': 'Choose your move!',
        'game.winningHand': 'Winning Hand:',
        'game.youWin': '🎉 You Win!',
        'game.youLose': '😢 You Lose!',
        'game.tie': '🤝 It\'s a Tie!',
        'game.scoresReset': 'Scores reset! Choose your move!',
        
        // Hands
        'hand.rock': 'Rock',
        'hand.paper': 'Paper',
        'hand.scissors': 'Scissors',
        
        // Difficulty levels
        'difficulty.easy': 'Easy',
        'difficulty.medium': 'Medium',
        'difficulty.hard': 'Hard',
        'difficulty.veryHard': 'Very Hard',
        'difficulty.easyRandom': 'Easy (Random)',
        'difficulty.mediumAdaptive': 'Medium (Adaptive)',
        'difficulty.hardPredictive': 'Hard (Predictive)',
        'difficulty.veryHardMaster': 'Very Hard (Master)',
        
        // Difficulty messages
        'difficultyMsg.easy': 'Easy mode: Computer plays randomly 🎲',
        'difficultyMsg.medium': 'Medium mode: Computer adapts to your patterns 🤔',
        'difficultyMsg.hard': 'Hard mode: Computer predicts your moves! 😈',
        'difficultyMsg.veryhard': 'Very Hard mode: Master strategist with advanced psychology! 👹',
        
        // Menu
        'menu.appearance': '🎨 Appearance',
        'menu.darkMode': '🌙 Dark Mode',
        'menu.theme': 'Theme:',
        'menu.autoPlay': '🤖 Auto-Play',
        'menu.startAutoPlay': '▶️ Start Auto-Play',
        'menu.stopAutoPlay': '⏸️ Stop Auto-Play',
        'menu.playerAI': 'Player AI Level:',
        'menu.speed': 'Speed:',
        'menu.aiAnalysis': '🧠 AI Analysis',
        'menu.viewPattern': 'View Local Pattern Analysis',
        'menu.viewOpenAI': '🤖 View OpenAI Commentary',
        'menu.hidePattern': 'Hide Pattern Analysis',
        'menu.statistics': '📊 Statistics',
        'menu.viewHandStats': 'Aggregated Data',
        'menu.showTrendGraph': '📈 Trend Graph',
        'menu.game': '🎮 Game',
        'menu.resetScores': 'Reset Scores',
        
        // Themes
        'theme.default': 'Default',
        'theme.spring': 'Spring',
        'theme.ocean': 'Ocean',
        
        // Speed
        'speed.slow': 'Slow (2s)',
        'speed.normal': 'Normal (1.5s)',
        'speed.fast': 'Fast (0.8s)',
        'speed.turbo': 'Turbo (0.3s)',
        
        // Analysis
        'analysis.patternDetection': 'Pattern Detection - Last 50 Games',
        'analysis.playForAnalysis': 'Play a few rounds for AI analysis...',
        'analysis.strategyTips': '💡 Strategy Tips',
        'analysis.strategiesAppear': 'Strategies will appear here...',
        'analysis.winRates': '📈 Win Rates',
        'analysis.noPatternsYet': 'No clear patterns detected yet...',
        
        // Stats
        'stats.handStats': 'Hand Statistics',
        'stats.overall': 'Overall',
        'stats.wins': 'Wins',
        'stats.losses': 'Losses',
        'stats.ties': 'Ties',
        'stats.totalPlayed': 'Total Played',
        'stats.winRate': 'Win Rate',
        
        // Streak messages
        'streak.noStreak': 'No Streak',
        'streak.winning': 'Winning Streak',
        'streak.losing': 'Losing Streak',
        'streak.onFire': 'ON FIRE',
        'streak.unstoppable': 'UNSTOPPABLE',
        'streak.legendary': 'LEGENDARY',
        'streak.longestWinning': 'Longest Winning Streak',
        'streak.longestLosing': 'Longest Losing Streak',
        
        // Patterns
        'pattern.repeatAfterWin': 'You tend to repeat your choice after winning',
        'pattern.repeatAfterLoss': 'You tend to repeat your choice after losing',
        'pattern.playsMoreOften': 'You play {hand} more often than other hands',
        
        // Strategies
        'strategy.computerFavored': 'Computer recently favored {hand}. Try {counter}!',
        'strategy.losingStreak': 'You\'re in a losing streak. Try changing your strategy!',
        'strategy.bestHand': 'Your best hand is {hand}. But the AI may have noticed!',
        
        // Battle display
        'battle.you': 'You',
        'battle.computer': 'Computer',
        
        // OpenAI Commentary
        'openai.placeholder': 'Click "View OpenAI Commentary" to get AI-powered analysis of your gameplay.',
        'openai.loading': 'Analyzing your gameplay...',
        'openai.error': 'Error fetching commentary. Check API key or try again.',
        'openai.noData': 'Play at least 5 games to get meaningful commentary.'
    },
    fr: {
        // Interface de jeu
        'game.title': 'Pierre Papier Ciseaux',
        'game.you': 'Vous',
        'game.ties': 'Égalités',
        'game.computer': 'Ordinateur',
        'game.opponentDifficulty': 'Difficulté de l\'adversaire:',
        'game.chooseMove': 'Choisissez votre coup!',
        'game.winningHand': 'Main gagnante:',
        'game.youWin': '🎉 Vous gagnez!',
        'game.youLose': '😢 Vous perdez!',
        'game.tie': '🤝 Égalité!',
        'game.scoresReset': 'Scores réinitialisés! Choisissez votre coup!',
        
        // Mains
        'hand.rock': 'Pierre',
        'hand.paper': 'Papier',
        'hand.scissors': 'Ciseaux',
        
        // Niveaux de difficulté
        'difficulty.easy': 'Facile',
        'difficulty.medium': 'Moyen',
        'difficulty.hard': 'Difficile',
        'difficulty.veryHard': 'Très Difficile',
        'difficulty.easyRandom': 'Facile (Aléatoire)',
        'difficulty.mediumAdaptive': 'Moyen (Adaptatif)',
        'difficulty.hardPredictive': 'Difficile (Prédictif)',
        'difficulty.veryHardMaster': 'Très Difficile (Maître)',
        
        // Messages de difficulté
        'difficultyMsg.easy': 'Mode facile: L\'ordinateur joue aléatoirement 🎲',
        'difficultyMsg.medium': 'Mode moyen: L\'ordinateur s\'adapte à vos schémas 🤔',
        'difficultyMsg.hard': 'Mode difficile: L\'ordinateur prédit vos coups! 😈',
        'difficultyMsg.veryhard': 'Mode très difficile: Stratège maître avec psychologie avancée! 👹',
        
        // Menu
        'menu.appearance': '🎨 Apparence',
        'menu.darkMode': '🌙 Mode Sombre',
        'menu.theme': 'Thème:',
        'menu.autoPlay': '🤖 Lecture Auto',
        'menu.startAutoPlay': '▶️ Démarrer Lecture Auto',
        'menu.stopAutoPlay': '⏸️ Arrêter Lecture Auto',
        'menu.playerAI': 'Niveau IA du Joueur:',
        'menu.speed': 'Vitesse:',
        'menu.aiAnalysis': '🧠 Analyse IA',
        'menu.viewPattern': 'Voir l\'Analyse de Motifs',
        'menu.hidePattern': 'Masquer l\'Analyse de Motifs',
        'menu.statistics': '📊 Statistiques',
        'menu.viewHandStats': 'Données Agrégées',
        'menu.showTrendGraph': '📈 Graphique de Tendance',
        'menu.game': '🎮 Jeu',
        'menu.resetScores': 'Réinitialiser les Scores',
        
        // Thèmes
        'theme.default': 'Par Défaut',
        'theme.spring': 'Printemps',
        'theme.ocean': 'Océan',
        
        // Vitesse
        'speed.slow': 'Lent (2s)',
        'speed.normal': 'Normal (1.5s)',
        'speed.fast': 'Rapide (0.8s)',
        'speed.turbo': 'Turbo (0.3s)',
        
        // Analyse
        'analysis.patternDetection': 'Détection de Motifs - 50 Derniers Jeux',
        'analysis.playForAnalysis': 'Jouez quelques rounds pour l\'analyse IA...',
        'analysis.strategyTips': '💡 Conseils de Stratégie',
        'analysis.strategiesAppear': 'Les stratégies apparaîtront ici...',
        'analysis.winRates': '📈 Taux de Victoire',
        'analysis.noPatternsYet': 'Aucun motif clair détecté pour le moment...',
        
        // Stats
        'stats.handStats': 'Statistiques des Mains',
        'stats.overall': 'Global',
        'stats.wins': 'Victoires',
        'stats.losses': 'Défaites',
        'stats.ties': 'Égalités',
        'stats.totalPlayed': 'Total Joué',
        'stats.winRate': 'Taux de Victoire',
        
        // Messages de série
        'streak.noStreak': 'Aucune Série',
        'streak.winning': 'Série de Victoires',
        'streak.losing': 'Série de Défaites',
        'streak.onFire': 'EN FEU',
        'streak.unstoppable': 'INARRÊTABLE',
        'streak.legendary': 'LÉGENDAIRE',
        'streak.longestWinning': 'Série Gagnante la Plus Longue',
        'streak.longestLosing': 'Série Perdante la Plus Longue',
        
        // Motifs
        'pattern.repeatAfterWin': 'Vous avez tendance à répéter votre choix après avoir gagné',
        'pattern.repeatAfterLoss': 'Vous avez tendance à répéter votre choix après avoir perdu',
        'pattern.playsMoreOften': 'Vous jouez {hand} plus souvent que les autres mains',
        
        // Stratégies
        'strategy.computerFavored': 'L\'ordinateur a récemment favorisé {hand}. Essayez {counter}!',
        'strategy.losingStreak': 'Vous êtes dans une série de défaites. Essayez de changer votre stratégie!',
        'strategy.bestHand': 'Votre meilleure main est {hand}. Mais l\'IA l\'a peut-être remarqué!',
        
        // Affichage de bataille
        'battle.you': 'Vous',
        'battle.computer': 'Ordinateur',
        
        // OpenAI Commentary
        'openai.title': '🤖 Commentaire OpenAI',
        'openai.placeholder': 'Cliquez sur "Voir Commentaire OpenAI" pour obtenir une analyse IA de votre jeu.',
        'openai.loading': 'Analyse de votre jeu...',
        'openai.error': 'Erreur lors de l\'obtention du commentaire. Vérifiez la clé API ou réessayez.',
        'openai.noData': 'Jouez au moins 5 jeux pour obtenir un commentaire significatif.'
    },
    es: {
        // Interfaz del juego
        'game.title': 'Piedra Papel Tijeras',
        'game.you': 'Tú',
        'game.ties': 'Empates',
        'game.computer': 'Computadora',
        'game.opponentDifficulty': 'Dificultad del Oponente:',
        'game.chooseMove': '¡Elige tu jugada!',
        'game.winningHand': 'Mano Ganadora:',
        'game.youWin': '🎉 ¡Ganaste!',
        'game.youLose': '😢 ¡Perdiste!',
        'game.tie': '🤝 ¡Es un Empate!',
        'game.scoresReset': '¡Puntuaciones reiniciadas! ¡Elige tu jugada!',
        
        // Manos
        'hand.rock': 'Piedra',
        'hand.paper': 'Papel',
        'hand.scissors': 'Tijeras',
        
        // Niveles de dificultad
        'difficulty.easy': 'Fácil',
        'difficulty.medium': 'Medio',
        'difficulty.hard': 'Difícil',
        'difficulty.veryHard': 'Muy Difícil',
        'difficulty.easyRandom': 'Fácil (Aleatorio)',
        'difficulty.mediumAdaptive': 'Medio (Adaptativo)',
        'difficulty.hardPredictive': 'Difícil (Predictivo)',
        'difficulty.veryHardMaster': 'Muy Difícil (Maestro)',
        
        // Mensajes de dificultad
        'difficultyMsg.easy': 'Modo fácil: La computadora juega aleatoriamente 🎲',
        'difficultyMsg.medium': 'Modo medio: La computadora se adapta a tus patrones 🤔',
        'difficultyMsg.hard': 'Modo difícil: ¡La computadora predice tus movimientos! 😈',
        'difficultyMsg.veryhard': 'Modo muy difícil: ¡Estratega maestro con psicología avanzada! 👹',
        
        // Menú
        'menu.appearance': '🎨 Apariencia',
        'menu.darkMode': '🌙 Modo Oscuro',
        'menu.theme': 'Tema:',
        'menu.autoPlay': '🤖 Juego Automático',
        'menu.startAutoPlay': '▶️ Iniciar Juego Automático',
        'menu.stopAutoPlay': '⏸️ Detener Juego Automático',
        'menu.playerAI': 'Nivel de IA del Jugador:',
        'menu.speed': 'Velocidad:',
        'menu.aiAnalysis': '🧠 Análisis de IA',
        'menu.viewPattern': 'Ver Análisis de Patrones Locales',
        'menu.viewOpenAI': '🤖 Ver Comentario de OpenAI',
        'menu.hidePattern': 'Ocultar Análisis de Patrones',
        'menu.statistics': '📊 Estadísticas',
        'menu.viewHandStats': 'Datos Agregados',
        'menu.showTrendGraph': '📈 Gráfico de Tendencia',
        'menu.game': '🎮 Juego',
        'menu.resetScores': 'Reiniciar Puntuaciones',
        
        // Temas
        'theme.default': 'Predeterminado',
        'theme.spring': 'Primavera',
        'theme.ocean': 'Océano',
        
        // Velocidad
        'speed.slow': 'Lento (2s)',
        'speed.normal': 'Normal (1.5s)',
        'speed.fast': 'Rápido (0.8s)',
        'speed.turbo': 'Turbo (0.3s)',
        
        // Análisis
        'analysis.patternDetection': 'Detección de Patrones - Últimos 50 Juegos',
        'analysis.playForAnalysis': 'Juega algunas rondas para análisis de IA...',
        'analysis.strategyTips': '💡 Consejos de Estrategia',
        'analysis.strategiesAppear': 'Las estrategias aparecerán aquí...',
        'analysis.winRates': '📈 Tasas de Victoria',
        'analysis.noPatternsYet': 'No se detectaron patrones claros aún...',
        
        // Stats
        'stats.handStats': 'Estadísticas de Manos',
        'stats.overall': 'General',
        'stats.wins': 'Victorias',
        'stats.losses': 'Derrotas',
        'stats.ties': 'Empates',
        'stats.totalPlayed': 'Total Jugado',
        'stats.winRate': 'Tasa de Victoria',
        
        // Mensajes de racha
        'streak.noStreak': 'Sin Racha',
        'streak.winning': 'Racha de Victorias',
        'streak.losing': 'Racha de Derrotas',
        'streak.onFire': '¡EN LLAMAS!',
        'streak.unstoppable': '¡IMPARABLE!',
        'streak.legendary': '¡LEGENDARIO!',
        'streak.longestWinning': 'Racha Ganadora Más Larga',
        'streak.longestLosing': 'Racha Perdedora Más Larga',
        
        // Patrones
        'pattern.repeatAfterWin': 'Tiendes a repetir tu elección después de ganar',
        'pattern.repeatAfterLoss': 'Tiendes a repetir tu elección después de perder',
        'pattern.playsMoreOften': 'Juegas {hand} más a menudo que otras manos',
        
        // Estrategias
        'strategy.computerFavored': 'La computadora favoreció recientemente {hand}. ¡Prueba {counter}!',
        'strategy.losingStreak': '¡Estás en una racha perdedora! ¡Intenta cambiar tu estrategia!',
        'strategy.bestHand': 'Tu mejor mano es {hand}. ¡Pero la IA puede haberlo notado!',
        
        // Pantalla de batalla
        'battle.you': 'Tú',
        'battle.computer': 'Computadora',
        
        // OpenAI Commentary
        'openai.title': '🤖 Comentario de OpenAI',
        'openai.placeholder': 'Haz clic en "Ver Comentario de OpenAI" para obtener un análisis IA de tu juego.',
        'openai.loading': 'Analizando tu juego...',
        'openai.error': 'Error al obtener comentario. Verifica la clave API o intenta nuevamente.',
        'openai.noData': 'Juega al menos 5 juegos para obtener un comentario significativo.'
    }
};

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
console.log('=== DIFFICULTY BUTTONS CHECK ===');
console.log('Found difficulty buttons:', difficultyBtns);
console.log('Number of buttons:', difficultyBtns.length);

// Streak elements
const streakDisplay = document.getElementById('streak-display');
const streakEmoji = document.getElementById('streak-emoji');
const streakText = document.getElementById('streak-text');
const longestWinningStreakEl = document.getElementById('longest-winning-streak');
const longestLosingStreakEl = document.getElementById('longest-losing-streak');

// Menu elements
const menuToggleBtn = document.getElementById('menu-toggle-btn');
const leftSidebar = document.getElementById('left-sidebar');
const closeSidebarBtn = document.getElementById('close-sidebar-btn');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const themeSelect = document.getElementById('theme-select');
const languageSelect = document.getElementById('language-select');
const autoPlayerDifficultySelect = document.getElementById('auto-player-difficulty');
const autoPlaySpeedSelect = document.getElementById('auto-play-speed');
const showStatsBtn = document.getElementById('show-stats-btn');
const showTrendsBtn = document.getElementById('show-trends-btn');
const menuResetBtn = document.getElementById('menu-reset-btn');
const menuAutoPlayBtn = document.getElementById('menu-auto-play-btn');
const showAnalysisBtn = document.getElementById('show-analysis-btn');
const showOpenAIBtn = document.getElementById('show-openai-btn');
const aiAnalysisContent = document.getElementById('ai-analysis-content');

// OpenAI sidebar elements
const openaiSidebar = document.getElementById('openai-sidebar');
const closeOpenAIBtn = document.getElementById('close-openai-btn');
const openaiContent = document.getElementById('openai-content');
const openaiLoading = document.getElementById('openai-loading');

// Add console logs to verify elements
console.log('=== OPENAI ELEMENTS CHECK ===');
console.log('openaiSidebar:', openaiSidebar);
console.log('closeOpenAIBtn:', closeOpenAIBtn);
console.log('openaiContent:', openaiContent);
console.log('openaiLoading:', openaiLoading);

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
const closeTrendModalBtn = document.getElementById('close-trend-modal');
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
    const savedLongestWinning = localStorage.getItem('rps-longest-winning-streak');
    const savedLongestLosing = localStorage.getItem('rps-longest-losing-streak');
    
    if (savedBestStreak) {
        bestStreak = parseInt(savedBestStreak);
    }
    if (savedLongestWinning) {
        longestWinningStreak = parseInt(savedLongestWinning);
    }
    if (savedLongestLosing) {
        longestLosingStreak = parseInt(savedLongestLosing);
    }
    updateLongestStreaksDisplay();
}

// Save streak data
function saveStreaks() {
    localStorage.setItem('rps-best-streak', bestStreak.toString());
    localStorage.setItem('rps-longest-winning-streak', longestWinningStreak.toString());
    localStorage.setItem('rps-longest-losing-streak', longestLosingStreak.toString());
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

// Translation functions
function t(key, replacements = {}) {
    let text = translations[currentLanguage][key] || translations['en'][key] || key;
    
    // Replace placeholders
    Object.keys(replacements).forEach(placeholder => {
        text = text.replace(`{${placeholder}}`, replacements[placeholder]);
    });
    
    return text;
}

function updateAllTranslations() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = t(key);
    });
    
    // Update placeholder texts
    if (patternMessagesMenu) {
        patternMessagesMenu.innerHTML = `<p class="pattern-placeholder">${t('analysis.playForAnalysis')}</p>`;
    }
    if (strategyMessagesMenu) {
        strategyMessagesMenu.innerHTML = `<p class="strategy-placeholder">${t('analysis.strategiesAppear')}</p>`;
    }
}

function changeLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('rps-language', lang);
    updateAllTranslations();
    
    // Re-generate patterns and strategies in new language if they exist
    if (gameHistory.length >= 5) {
        detectPatterns();
        generateStrategies();
    }
}

function loadLanguage() {
    const saved = localStorage.getItem('rps-language');
    if (saved && translations[saved]) {
        currentLanguage = saved;
        languageSelect.value = saved;
        updateAllTranslations();
    }
}

// Update longest streaks display
function updateLongestStreaksDisplay() {
    if (longestWinningStreakEl) {
        longestWinningStreakEl.textContent = longestWinningStreak;
    }
    if (longestLosingStreakEl) {
        longestLosingStreakEl.textContent = longestLosingStreak;
    }
}

// Update streak display
function updateStreakDisplay() {
    const absStreak = Math.abs(currentStreak);
    
    // Remove all classes
    streakDisplay.classList.remove('active', 'winning', 'losing', 'on-fire');
    
    if (absStreak === 0) {
        // No streak
        streakDisplay.classList.remove('active');
        streakText.textContent = t('streak.noStreak');
        streakEmoji.textContent = '🎯';
        return;
    }
    
    // Show streak
    streakDisplay.classList.add('active');
    
    if (currentStreak > 0) {
        // Winning streak
        streakDisplay.classList.add('winning');
        
        if (absStreak >= 10) {
            streakDisplay.classList.add('on-fire');
            streakEmoji.textContent = '👑';
            streakText.textContent = `${t('streak.legendary')} +${absStreak}!`;
        } else if (absStreak >= 5) {
            streakDisplay.classList.add('on-fire');
            streakEmoji.textContent = '🔥';
            streakText.textContent = `${t('streak.unstoppable')} +${absStreak}!`;
        } else if (absStreak >= 3) {
            streakDisplay.classList.add('on-fire');
            streakEmoji.textContent = '🔥';
            streakText.textContent = `${t('streak.onFire')} +${absStreak}!`;
        } else {
            streakEmoji.textContent = '✨';
            streakText.textContent = `${t('streak.winning')} +${absStreak}`;
        }
    } else {
        // Losing streak
        streakDisplay.classList.add('losing');
        
        if (absStreak >= 5) {
            streakEmoji.textContent = '💀';
            streakText.textContent = `${t('streak.losing')} -${absStreak}`;
        } else if (absStreak >= 3) {
            streakEmoji.textContent = '😰';
            streakText.textContent = `${t('streak.losing')} -${absStreak}`;
        } else {
            streakEmoji.textContent = '😕';
            streakText.textContent = `${t('streak.losing')} -${absStreak}`;
        }
    }
}

// Update hand statistics display
function updateHandStatsDisplay() {
    // Rock stats
    const rockTotal = handStats.rock.wins + handStats.rock.losses + handStats.rock.ties;
    const rockWinRate = rockTotal > 0 ? ((handStats.rock.wins / rockTotal) * 100).toFixed(1) : 0;
    document.getElementById('rock-wins').textContent = handStats.rock.wins;
    document.getElementById('rock-losses').textContent = handStats.rock.losses;
    document.getElementById('rock-ties').textContent = handStats.rock.ties;
    document.getElementById('rock-total').textContent = rockTotal;
    document.getElementById('rock-winrate').textContent = `${rockWinRate}%`;
    
    // Paper stats
    const paperTotal = handStats.paper.wins + handStats.paper.losses + handStats.paper.ties;
    const paperWinRate = paperTotal > 0 ? ((handStats.paper.wins / paperTotal) * 100).toFixed(1) : 0;
    document.getElementById('paper-wins').textContent = handStats.paper.wins;
    document.getElementById('paper-losses').textContent = handStats.paper.losses;
    document.getElementById('paper-ties').textContent = handStats.paper.ties;
    document.getElementById('paper-total').textContent = paperTotal;
    document.getElementById('paper-winrate').textContent = `${paperWinRate}%`;
    
    // Scissors stats
    const scissorsTotal = handStats.scissors.wins + handStats.scissors.losses + handStats.scissors.ties;
    const scissorsWinRate = scissorsTotal > 0 ? ((handStats.scissors.wins / scissorsTotal) * 100).toFixed(1) : 0;
    document.getElementById('scissors-wins').textContent = handStats.scissors.wins;
    document.getElementById('scissors-losses').textContent = handStats.scissors.losses;
    document.getElementById('scissors-ties').textContent = handStats.scissors.ties;
    document.getElementById('scissors-total').textContent = scissorsTotal;
    document.getElementById('scissors-winrate').textContent = `${scissorsWinRate}%`;
    
    // Overall stats
    const totalWins = scores.player;
    const totalLosses = scores.computer;
    const totalTies = scores.ties;
    const totalGames = totalWins + totalLosses + totalTies;
    const overallWinRate = totalGames > 0 ? ((totalWins / totalGames) * 100).toFixed(1) : 0;
    document.getElementById('overall-wins').textContent = totalWins;
    document.getElementById('overall-losses').textContent = totalLosses;
    document.getElementById('overall-ties').textContent = totalTies;
    document.getElementById('overall-total').textContent = totalGames;
    document.getElementById('overall-winrate').textContent = `${overallWinRate}%`;
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
    const recentHistory = gameHistory.slice(-50);
    
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
        patterns.push(`${t('pattern.repeatAfterWin')} (${((repeatAfterWin/winCount)*100).toFixed(0)}%)`);
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
        patterns.push(`${t('pattern.repeatAfterLoss')} (${((repeatAfterLoss/lossCount)*100).toFixed(0)}%)`);
    }
    
    // Pattern: Favorite hand
    const handCounts = {};
    recentHistory.forEach(game => {
        handCounts[game.player] = (handCounts[game.player] || 0) + 1;
    });
    const favorite = Object.keys(handCounts).reduce((a, b) => handCounts[a] > handCounts[b] ? a : b);
    const favoritePercent = (handCounts[favorite] / recentHistory.length * 100).toFixed(0);
    if (favoritePercent > 40) {
        const handName = t(`hand.${favorite}`);
        patterns.push(t('pattern.playsMoreOften', { hand: handName }) + ` (${favoritePercent}%)`);
    }
    
    // Update both UIs (menu and sidebar if visible)
    const patternHTML = patterns.length > 0 
        ? patterns.map(p => `<div class="pattern-message">${p}</div>`).join('')
        : `<p class="pattern-placeholder">${t('analysis.noPatternsYet')}</p>`;
    
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
    
    const handName = t(`hand.${computerFavorite}`);
    const counterName = t(`hand.${counters[computerFavorite]}`);
    strategies.push(t('strategy.computerFavored', { hand: handName, counter: counterName }));
    
    // Check if player is in a losing streak
    if (currentStreak < -2 && currentStreakType === 'loss') {
        strategies.push(t('strategy.losingStreak'));
    }
    
    // Analyze win rates
    const bestHand = Object.keys(handStats).reduce((a, b) => {
        const aRate = handStats[a].wins / (handStats[a].wins + handStats[a].losses + 1);
        const bRate = handStats[b].wins / (handStats[b].wins + handStats[b].losses + 1);
        return aRate > bRate ? a : b;
    });
    
    if (handStats[bestHand].wins > 3) {
        const bestHandName = t(`hand.${bestHand}`);
        strategies.push(t('strategy.bestHand', { hand: bestHandName }));
    }
    
    // Update both UIs
    const strategyHTML = strategies.length > 0
        ? strategies.map(s => `<div class="strategy-message">${s}</div>`).join('')
        : `<p class="strategy-placeholder">${t('analysis.strategiesAppear')}</p>`;
    
    if (strategyMessagesMenu) strategyMessagesMenu.innerHTML = strategyHTML;
    if (strategyMessages) strategyMessages.innerHTML = strategyHTML;
}

// Update score display
function updateScoreDisplay() {
    console.log('updateScoreDisplay called with:', scores);
    console.log('playerScoreEl:', playerScoreEl);
    console.log('computerScoreEl:', computerScoreEl);
    console.log('tieScoreEl:', tieScoreEl);
    playerScoreEl.textContent = scores.player;
    computerScoreEl.textContent = scores.computer;
    tieScoreEl.textContent = scores.ties;
    console.log('After update - playerScoreEl.textContent:', playerScoreEl.textContent);
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
                    <div style="font-size: 2.0rem; color: #666; margin-bottom: 5px; font-weight: 600;">${t('battle.you')}</div>
                    <span class="battle-emoji">${emojiMap[data.player_choice]}</span>
                </div>
                <div style="font-size: 2rem; color: #667eea;">VS</div>
                <div style="text-align: center;">
                    <div style="font-size: 2.0rem; color: #666; margin-bottom: 5px; font-weight: 600;">${t('battle.computer')}</div>
                    <span class="battle-emoji">${emojiMap[data.computer_choice]}</span>
                </div>
            </div>
        `;
        
        // Update result message
        resultMessage.classList.remove('win', 'lose', 'tie');
        
        let winningHand = null;
        
        if (data.result === 'player') {
            resultMessage.textContent = t('game.youWin');
            resultMessage.classList.add('win');
            scores.player++;
            winningHand = data.player_choice;
        } else if (data.result === 'computer') {
            resultMessage.textContent = t('game.youLose');
            resultMessage.classList.add('lose');
            scores.computer++;
            winningHand = data.computer_choice;
        } else {
            resultMessage.textContent = t('game.tie');
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
        
        // Update longest winning/losing streaks
        if (currentStreak > longestWinningStreak) {
            longestWinningStreak = currentStreak;
            updateLongestStreaksDisplay();
            saveStreaks();
        }
        if (Math.abs(currentStreak) > longestLosingStreak && currentStreak < 0) {
            longestLosingStreak = Math.abs(currentStreak);
            updateLongestStreaksDisplay();
            saveStreaks();
        }
        
        // Update streak display
        updateStreakDisplay();
        
        // Add to trend data
        trendData.push({
            player: scores.player,
            computer: scores.computer
        });
        // Keep last 100 data points
        if (trendData.length > 100) {
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
        
        // Update trend graph if it's open
        updateTrendGraphIfOpen();
        
    } catch (error) {
        console.error('=== GAME ERROR ===');
        console.error('Error object:', error);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
        console.error('Request data was:', requestData);
        resultMessage.textContent = 'Error connecting to server! Check console (Cmd+Option+I)';
        resultMessage.style.fontSize = '0.9rem';
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
    longestWinningStreak = 0;
    longestLosingStreak = 0;
    updateScoreDisplay();
    updateHandStatsDisplay();
    updateWinRates();
    updateStreakDisplay();
    updateLongestStreaksDisplay();
    saveScores();
    saveHandStats();
    saveTrend();
    saveStreaks();
    resultMessage.textContent = t('game.scoresReset');
    resultMessage.classList.remove('win', 'lose', 'tie');
    battleDisplay.innerHTML = '';
    winningHandContainer.classList.remove('visible');
    winningEmojiEl.textContent = '?';
    
    // Reset pattern displays
    const resetPattern = `<p class="pattern-placeholder">${t('analysis.playForAnalysis')}</p>`;
    const resetStrategy = `<p class="strategy-placeholder">${t('analysis.strategiesAppear')}</p>`;
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
    console.log('setDifficulty called with:', difficulty);
    console.log('Current difficulty before:', currentDifficulty);
    currentDifficulty = difficulty;
    console.log('Current difficulty after:', currentDifficulty);
    updateDifficultyDisplay();
    saveDifficulty();
    
    // Show message about difficulty change
    resultMessage.textContent = t(`difficultyMsg.${difficulty}`);
    resultMessage.classList.remove('win', 'lose', 'tie');
    console.log('Result message set to:', resultMessage.textContent);
}

// Toggle menu sidebar
function toggleMenu() {
    leftSidebar.classList.toggle('open');
    document.body.classList.toggle('menu-open');
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
    console.log('showTrendGraph called');
    console.log('Trend modal:', trendModal);
    
    // Toggle the graph
    const isOpen = trendModal.classList.contains('open');
    
    if (isOpen) {
        // Close it
        trendModal.classList.remove('open');
        document.body.classList.remove('trends-open');
    } else {
        // Open it
        trendModal.classList.add('open');
        document.body.classList.add('trends-open');
        
        // Update the title with total game count (capped at 100)
        const trendTitle = document.getElementById('trend-graph-title');
        const totalGames = scores.player + scores.computer + scores.ties;
        if (trendTitle) {
            // Cap the title at 100 games
            const displayGames = Math.min(totalGames, 100);
            trendTitle.textContent = `📈 Data from last ${displayGames} games`;
        }
        
        // Update stats
        totalGamesStat.textContent = totalGames;
        currentStreakStat.textContent = currentStreak >= 0 ? `+${currentStreak}` : currentStreak;
        bestStreakStat.textContent = bestStreak >= 0 ? `+${bestStreak}` : bestStreak;
        
        // Draw chart
        setTimeout(() => {
            drawTrendChart(trendChart, trendData);
        }, 100);
    }
}

// Close trend modal
function closeTrendGraphModal() {
    console.log('closeTrendGraphModal called');
    trendModal.classList.remove('open');
    document.body.classList.remove('trends-open');
}

// Update trend graph if it's currently open
function updateTrendGraphIfOpen() {
    if (trendModal && trendModal.classList.contains('open')) {
        const trendTitle = document.getElementById('trend-graph-title');
        const totalGames = scores.player + scores.computer + scores.ties;
        if (trendTitle) {
            // Cap the title at 100 games
            const displayGames = Math.min(totalGames, 100);
            trendTitle.textContent = `📈 Data from last ${displayGames} games`;
        }
        
        // Update stats
        if (totalGamesStat) totalGamesStat.textContent = totalGames;
        if (currentStreakStat) currentStreakStat.textContent = currentStreak >= 0 ? `+${currentStreak}` : currentStreak;
        if (bestStreakStat) bestStreakStat.textContent = bestStreak >= 0 ? `+${bestStreak}` : bestStreak;
        
        // Redraw chart
        if (trendChart && trendData) {
            drawTrendChart(trendChart, trendData);
        }
    }
}

// Toggle auto-play mode
function toggleAutoPlay() {
    autoPlayActive = !autoPlayActive;
    
    if (autoPlayActive) {
        // Start auto-play
        menuAutoPlayBtn.textContent = t('menu.stopAutoPlay');
        menuAutoPlayBtn.classList.add('active');
        
        // Disable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = true);
        difficultyBtns.forEach(btn => btn.disabled = true);
        
        // Disable auto-play settings dropdowns
        autoPlayerDifficultySelect.disabled = true;
        autoPlaySpeedSelect.disabled = true;
        
        // Get auto-play settings
        autoPlayerDifficulty = autoPlayerDifficultySelect.value;
        const speedSetting = autoPlaySpeedSelect.value;
        const speeds = { slow: 2000, normal: 1500, fast: 800, turbo: 300 };
        autoPlaySpeed = speeds[speedSetting] || 1500;
        
        // Start the auto-play loop
        startAutoPlay();
    } else {
        // Stop auto-play
        menuAutoPlayBtn.textContent = t('menu.startAutoPlay');
        menuAutoPlayBtn.classList.remove('active');
        
        // Re-enable manual play buttons and difficulty buttons
        choiceBtns.forEach(btn => btn.disabled = false);
        difficultyBtns.forEach(btn => btn.disabled = false);
        
        // Re-enable auto-play settings dropdowns
        autoPlayerDifficultySelect.disabled = false;
        autoPlaySpeedSelect.disabled = false;
        
        // Stop the auto-play loop
        stopAutoPlay();
    }
}

// Toggle AI analysis visibility
function toggleAnalysis() {
    const isVisible = aiAnalysisContent.style.display !== 'none';
    aiAnalysisContent.style.display = isVisible ? 'none' : 'block';
    showAnalysisBtn.textContent = isVisible ? t('menu.viewPattern') : t('menu.hidePattern');
}

// Toggle OpenAI sidebar
function toggleOpenAISidebar() {
    if (openaiSidebar) {
        openaiSidebar.classList.toggle('open');
    }
}

// Close OpenAI sidebar
function closeOpenAISidebar() {
    if (openaiSidebar) {
        openaiSidebar.classList.remove('open');
        // Stop the timer when closing
        if (commentaryTimerInterval) {
            clearInterval(commentaryTimerInterval);
            commentaryTimerInterval = null;
        }
    }
}

// Fetch OpenAI commentary
async function fetchOpenAICommentary() {
    console.log('=== FETCH OPENAI COMMENTARY CALLED ===');
    
    if (!openaiSidebar || !openaiContent || !openaiLoading) {
        console.error('OpenAI elements not found!');
        alert('Error: OpenAI sidebar elements not found. Please refresh the page.');
        return;
    }
    
    if (gameHistory.length < 5) {
        openaiContent.innerHTML = `<div class="openai-error"><p>${t('openai.noData')}</p></div>`;
        openaiSidebar.classList.add('open');
        return;
    }
    
    // Show loading
    openaiContent.style.display = 'none';
    openaiLoading.style.display = 'block';
    openaiSidebar.classList.add('open');
    
    console.log('Sending request to OpenAI endpoint...');
    
    try {
        const response = await fetch('/api/openai-commentary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_history: gameHistory.slice(-100), // Last 100 games
                scores: scores,
                hand_stats: handStats,
                current_difficulty: currentDifficulty
            })
        });
        
        console.log('Response received:', response.status);
        const data = await response.json();
        console.log('Data:', data);
        
        // Hide loading
        openaiLoading.style.display = 'none';
        openaiContent.style.display = 'block';
        
        if (data.error) {
            openaiContent.innerHTML = `<div class="openai-error"><p>${data.error}</p></div>`;
        } else {
            // Store the timestamp when commentary was received
            const commentaryTimestamp = Date.now();
            const totalGames = scores.player + scores.computer + scores.ties;
            
            // Format the commentary with game info, timer and refresh button
            const commentaryHTML = `
                <div class="commentary-controls">
                    <div class="commentary-game-info">
                        📊 Commentary refreshed on game ${totalGames}
                    </div>
                    <div class="commentary-timer" id="commentary-timer">
                        <span class="timer-icon">⏱️</span>
                        <span id="commentary-time-elapsed">0</span> seconds ago
                    </div>
                    <button class="refresh-commentary-btn" id="refresh-commentary-btn">
                        🔄 Refresh
                    </button>
                </div>
                <div class="openai-commentary">
                    ${data.commentary.split('\n').map(line => line.trim() ? `<p>${line}</p>` : '').join('')}
                </div>
            `;
            openaiContent.innerHTML = commentaryHTML;
            
            // Add event listener to refresh button
            const refreshBtn = document.getElementById('refresh-commentary-btn');
            if (refreshBtn) {
                refreshBtn.addEventListener('click', refreshOpenAICommentary);
            }
            
            // Start the timer
            startCommentaryTimer(commentaryTimestamp);
        }
    } catch (error) {
        console.error('Error fetching OpenAI commentary:', error);
        openaiLoading.style.display = 'none';
        openaiContent.style.display = 'block';
        openaiContent.innerHTML = `<div class="openai-error"><p>${t('openai.error')}</p><p>${error.message}</p></div>`;
    }
}

// Refresh OpenAI commentary with latest game data
async function refreshOpenAICommentary() {
    console.log('=== REFRESH OPENAI COMMENTARY CALLED ===');
    
    // Call the same function to fetch fresh commentary
    await fetchOpenAICommentary();
}

// Timer for commentary freshness
let commentaryTimerInterval = null;

function startCommentaryTimer(timestamp) {
    // Clear any existing timer
    if (commentaryTimerInterval) {
        clearInterval(commentaryTimerInterval);
    }
    
    // Update timer every second
    commentaryTimerInterval = setInterval(() => {
        const timeElapsedElement = document.getElementById('commentary-time-elapsed');
        if (timeElapsedElement) {
            const secondsElapsed = Math.floor((Date.now() - timestamp) / 1000);
            timeElapsedElement.textContent = secondsElapsed;
        } else {
            // Element not found, stop the timer
            clearInterval(commentaryTimerInterval);
        }
    }, 1000);
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
languageSelect.addEventListener('change', (e) => changeLanguage(e.target.value));
showAnalysisBtn.addEventListener('click', toggleAnalysis);
if (showOpenAIBtn) {
    console.log('Adding OpenAI button listener');
    console.log('OpenAI elements:', { openaiSidebar, openaiContent, openaiLoading });
    
    // Function to check and update button state
    function updateOpenAIButtonState() {
        const totalGames = scores.player + scores.computer + scores.ties;
        if (totalGames < 5) {
            showOpenAIBtn.disabled = true;
            showOpenAIBtn.style.opacity = '0.5';
            showOpenAIBtn.style.cursor = 'not-allowed';
        } else {
            showOpenAIBtn.disabled = false;
            showOpenAIBtn.style.opacity = '1';
            showOpenAIBtn.style.cursor = 'pointer';
        }
    }
    
    // Initial check
    updateOpenAIButtonState();
    
    // Add click listener
    showOpenAIBtn.addEventListener('click', () => {
        console.log('=== OPENAI BUTTON CLICKED ===');
        console.log('openaiSidebar classList before:', openaiSidebar.classList);
        console.log('gameHistory length:', gameHistory.length);
        
        const totalGames = scores.player + scores.computer + scores.ties;
        if (totalGames < 5) {
            alert('Play at least 5 games to get meaningful commentary.');
            return;
        }
        
        fetchOpenAICommentary();
    });
    
    // Store original updateScoreDisplay to add our check
    const originalUpdateScoreDisplay = updateScoreDisplay;
    updateScoreDisplay = function() {
        originalUpdateScoreDisplay();
        updateOpenAIButtonState();
    };
} else {
    console.error('showOpenAIBtn not found!');
}
if (closeOpenAIBtn) {
    closeOpenAIBtn.addEventListener('click', closeOpenAISidebar);
} else {
    console.error('closeOpenAIBtn not found!');
}

// Show stats button - toggle visibility like trend graph
showStatsBtn.addEventListener('click', () => {
    console.log('=== STATS BUTTON CLICKED ===');
    console.log('Stats panel:', statsPanel);
    console.log('Current classes:', statsPanel.classList);
    
    const isOpen = statsPanel.classList.contains('open');
    
    if (isOpen) {
        // Close it
        statsPanel.classList.remove('open');
        document.body.classList.remove('stats-open');
    } else {
        // Open it
        statsPanel.classList.add('open');
        document.body.classList.add('stats-open');
    }
});

showTrendsBtn.addEventListener('click', () => {
    console.log('=== TRENDS BUTTON CLICKED ===');
    console.log('Trend modal:', trendModal);
    console.log('Current classes:', trendModal.classList);
    showTrendGraph();
    console.log('After showTrendGraph');
    // Don't close menu - keep it open
});
menuResetBtn.addEventListener('click', () => {
    resetScores();
    // Don't close menu - keep it open
});
menuAutoPlayBtn.addEventListener('click', toggleAutoPlay);

// Remove duplicate listener check
if (showTrendsBtn) {
    console.log('Skipping duplicate showTrendsBtn listener - already added above');
}

// Stats panel close button (if it exists)
if (closeStatsBtn) {
    closeStatsBtn.addEventListener('click', () => {
        console.log('Close stats button clicked');
        statsPanel.classList.remove('open');
        document.body.classList.remove('stats-open');
    });
} else {
    console.log('Note: closeStatsBtn not found in HTML');
}

// Trend modal
closeTrendModalBtn.addEventListener('click', closeTrendGraphModal);
// Remove the click-outside-to-close functionality since it's now a bottom panel

// Difficulty button listeners
difficultyBtns.forEach(btn => {
    console.log('Adding listener to difficulty button:', btn, btn.dataset.difficulty);
    btn.addEventListener('click', () => {
        console.log('Difficulty button clicked:', btn.dataset.difficulty);
        const difficulty = btn.dataset.difficulty;
        setDifficulty(difficulty);
    });
});

// Load all saved data on page load
console.log('=== STARTING PAGE LOAD ===');
console.log('About to load scores...');
loadScores();
console.log('About to load hand stats...');
loadHandStats();
console.log('About to load difficulty...');
loadDifficulty();
console.log('About to load streaks...');
loadStreaks();
console.log('About to load trend...');
loadTrend();
console.log('About to load dark mode...');
loadDarkMode();
console.log('About to load theme...');
loadTheme();
console.log('About to load language...');
loadLanguage();
console.log('About to update win rates...');
updateWinRates();
console.log('=== PAGE LOAD COMPLETE ===');

