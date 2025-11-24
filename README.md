# Rock Paper Scissors Game 🎮

A modern, feature-rich Rock Paper Scissors game with Python Flask backend, advanced AI opponents, and a beautiful responsive web frontend.

## 🎯 Version History

### Version 2.0 - Advanced AI & Analytics Update (Current)

**Major Features Added:**

#### 🎨 **Enhanced UI/UX**
- ☰ **Consolidated Menu System** - All controls accessible from sleek left sidebar
- 🌙 **Dark Mode** - Beautiful dark theme with enhanced toggle switch (sun/moon indicators)
- 🎃 **Seasonal Themes** - 5 gorgeous themes to choose from:
  - Default (Purple gradient)
  - Halloween (Orange & spooky purple)
  - Christmas (Red & festive green)
  - Spring (Pink & mint fresh)
  - Ocean (Cyan & seafoam calm)
- **Responsive Layout** - Optimized for desktop, tablet, and mobile

#### 🧠 **AI Analysis & Strategy**
- **Pattern Detection** - AI analyzes your playing behavior:
  - Detects if you repeat moves after winning/losing
  - Identifies your favorite hands
  - Tracks behavioral patterns in real-time
- **Strategy Suggestions** - Smart tips based on:
  - Computer's recent play patterns
  - Your winning/losing streaks
  - Statistical analysis of your best-performing hands
- **Win Rate Percentages**:
  - Overall win rate tracking
  - Individual win rates for Rock, Paper, and Scissors
  - Real-time updates after each game

#### 📊 **Advanced Statistics**
- **Trend Graph** - Visual performance chart showing:
  - Player vs Computer score progression over time
  - Last 50 games tracked
  - Total games played
  - Current streak (wins/losses in a row)
  - Best streak ever achieved
- **Hand Statistics Dashboard**:
  - Detailed breakdown for each hand (Rock/Paper/Scissors)
  - Wins, Losses, and Ties tracked separately
  - Total plays per hand
  - Color-coded display (Green=Wins, Red=Losses, Orange=Ties)

#### 🤖 **Enhanced Auto-Play Mode**
- **Adjustable AI Difficulty**:
  - Easy: Pure random selection
  - Medium: Adaptive - counters your most common plays
  - Hard: Predictive - uses advanced pattern recognition
- **Variable Speed Control**:
  - Slow (2 seconds per round)
  - Normal (1.5 seconds per round)
  - Fast (0.8 seconds per round)
  - Turbo (0.3 seconds per round)
- **AI vs AI Battles** - Watch different AI difficulties compete!

#### 🎮 **Difficulty Levels**
- **Easy Mode** 😊 - Computer plays randomly (fair chance)
- **Medium Mode** 🤔 - Computer adapts to your patterns (70% counter rate)
- **Hard Mode** 😈 - Advanced AI that:
  - Predicts your next move based on psychology
  - Detects win/loss patterns
  - Weights recent plays more heavily
  - Exploits common human tendencies

#### 💾 **Data Persistence**
- All scores, statistics, and preferences saved in browser localStorage
- Game history (last 50 games) for AI analysis
- Streak tracking across sessions
- Theme and difficulty preferences remembered
- Trend data preserved

---

### Version 1.0 - Initial Release

**Core Features:**

#### ✨ **Beautiful Modern UI**
- Gradient purple design with smooth animations
- Emoji-based interface (✊ Rock, ✋ Paper, ✌️ Scissors)
- Responsive design (works on mobile and desktop)
- Card-based layout with hover effects

#### 🎯 **Core Game Features**
- Play against the computer
- Real-time score tracking (You vs Computer vs Ties)
- Visual feedback for wins, losses, and ties
- Winning hand indicator with circular badge
- Reset scores anytime

#### 🎲 **Game Mechanics**
- Standard Rock Paper Scissors rules:
  - Rock beats Scissors
  - Paper beats Rock
  - Scissors beats Paper
- Tie detection and tracking
- Prevention of rapid-clicking exploits

---

## 🚀 Tech Stack

**Backend:**
- Python 3.x
- Flask 3.0.0 (Web framework)
- Flask-CORS 4.0.0 (Cross-origin resource sharing)

**Frontend:**
- HTML5
- CSS3 (Custom variables for theming, animations, gradients)
- Vanilla JavaScript (No frameworks needed)
- Canvas API (For trend charts)

**AI/Logic:**
- Pattern recognition algorithms
- Statistical analysis
- Behavioral psychology models
- Weighted probability calculations

---

## 📦 Installation

1. **Clone or navigate to the project directory:**
```bash
cd /Users/alex.macdonald/cursor-11242025
```

2. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

---

## 🎮 Running the Application

1. **Start the Flask server:**
```bash
python3 app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

The server will run on `http://0.0.0.0:5000` by default.

---

## 📖 How to Play

### Basic Gameplay
1. **Choose your hand** by clicking Rock, Paper, or Scissors
2. The computer makes its choice based on selected difficulty
3. Winner is determined and scores update automatically
4. Winning hand is displayed in a circular badge

### Using the Menu (☰ Button)
1. **Click the ☰ button** (top-left) to open the menu
2. **Customize appearance:**
   - Toggle dark mode (moon/sun switch)
   - Choose from 5 seasonal themes
3. **Start Auto-Play:**
   - Click "Start Auto-Play"
   - Set AI difficulty (Easy/Medium/Hard)
   - Adjust speed (Slow to Turbo)
   - Watch AI battle itself!
4. **View AI Analysis:**
   - Click "View Pattern Analysis"
   - See detected patterns in your play style
   - Get strategic suggestions
   - Check win rates for each hand
5. **Check Statistics:**
   - "View Hand Statistics" for detailed breakdown
   - "Show Trend Graph" for performance over time
6. **Reset Scores** to start fresh

### Difficulty Levels
- **Easy**: Computer plays randomly - 50/50 fair chance
- **Medium**: Computer learns your patterns and counters them
- **Hard**: Advanced AI predicts your moves using psychology

---

## 🎯 Advanced Features Explained

### Pattern Detection
The AI analyzes your last 10 games to detect:
- **Repeat-after-win**: Do you play the same hand after winning?
- **Repeat-after-loss**: Do you stick with losing hands?
- **Favorite hand bias**: Do you over-rely on one hand?

### Strategy Suggestions
Based on analysis, you'll receive tips like:
- "Computer recently favored rock. Try paper!"
- "You're in a losing streak. Try changing your strategy!"
- "Your best hand is scissors. But the AI may have noticed!"

### AI Difficulty Mechanics

**Medium AI:**
- Tracks your most common hand
- Counters it 70% of the time
- Requires 3+ games to activate

**Hard AI:**
- Detects psychological patterns:
  - Most people repeat after winning
  - Most people switch to "what would have won" after losing
- Weights recent games more heavily
- 75% accuracy in countering tendencies
- Requires 5+ games for full analysis

---

## 📊 Statistics Explained

### Win Rate Calculation
```
Win Rate = (Wins / Total Games) × 100%
```
Calculated separately for:
- Overall performance
- Each individual hand (Rock/Paper/Scissors)

### Streak Tracking
- **Current Streak**: Consecutive wins or losses
- **Best Streak**: Highest consecutive wins ever achieved
- Resets on outcome change (win → loss or loss → win)

### Trend Data
- Tracks last 50 games
- Plots player score vs computer score
- Visualized on canvas-based chart
- Updates in real-time

---

## 🗂️ Project Structure

```
cursor-11242025/
├── app.py                  # Flask backend with AI logic
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML page with menu & modals
└── static/
    ├── style.css          # Comprehensive styles with themes
    ├── script.js          # Game logic, AI analysis, UI controls
    └── chart.min.js       # Lightweight chart rendering
```

---

## 🌐 API Endpoints

### POST `/api/play`
Play a round of rock, paper, scissors.

**Request Body:**
```json
{
  "choice": "rock|paper|scissors",
  "difficulty": "easy|medium|hard",
  "history": [
    {
      "player": "rock",
      "computer": "paper",
      "result": "computer"
    }
  ]
}
```

**Response:**
```json
{
  "player_choice": "rock",
  "computer_choice": "scissors",
  "result": "player|computer|tie"
}
```

---

## 🎨 Theme Customization

Themes use CSS custom properties for easy customization:

```css
:root {
  --primary-gradient-start: #667eea;
  --primary-gradient-end: #764ba2;
  --background-gradient-start: #667eea;
  --background-gradient-end: #764ba2;
  --text-primary: #333;
  --text-secondary: #666;
}
```

Dark mode automatically adjusts all theme colors for optimal contrast.

---

## 🌍 Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (Recommended)
- Firefox
- Safari
- Opera

**Minimum Requirements:**
- ES6 JavaScript support
- LocalStorage API
- Canvas API
- CSS Grid & Flexbox

---

## 💾 Data Storage

All data is stored locally in your browser using localStorage:
- `rps-scores` - Current score totals
- `rps-hand-stats` - Win/loss/tie breakdown per hand
- `rps-difficulty` - Selected difficulty level
- `rps-dark-mode` - Dark mode preference
- `rps-theme` - Selected theme
- `rps-best-streak` - Best winning streak
- `rps-trend` - Last 50 games for trend chart

**Privacy Note:** No data is sent to external servers. Everything stays on your device!

---

## 🎓 Learning Features

This game demonstrates:
- **AI & Machine Learning**: Pattern recognition and prediction
- **Statistical Analysis**: Win rate calculation and trend analysis
- **Game Theory**: Optimal strategy selection
- **UX Design**: Progressive disclosure, feedback loops
- **Psychology**: Behavioral pattern exploitation
- **Data Visualization**: Real-time charting
- **Responsive Design**: Mobile-first approach

---

## 🐛 Known Limitations

- Pattern detection requires minimum 5 games for accuracy
- Medium/Hard AI needs 3-5 games to "learn" your patterns
- Trend chart displays maximum 50 most recent games
- Auto-play speed limited to 0.3s (turbo) to prevent browser lag

---

## 🚀 Future Enhancements (Potential v3.0)

- 🦎 Rock Paper Scissors Lizard Spock variant
- 🏆 Achievement system with unlockable badges
- 👥 Local multiplayer (Player vs Player)
- 🌐 Online leaderboards
- 🎵 Sound effects and music
- 📱 Progressive Web App (PWA) support
- 💾 Cloud save sync
- 🎨 Custom hand emoji selector
- 📈 Advanced analytics dashboard
- 🤖 Neural network AI opponent

---

## 📝 License

Free to use and modify as needed.

---

## 🎉 Enjoy the Game!

Have fun playing Rock Paper Scissors! Can you beat the Hard AI? Can you maintain a winning streak? Check your statistics and improve your strategy!

**Pro Tip:** The Hard AI exploits common human patterns. To beat it, try playing randomly or doing the opposite of what you'd normally do! 🧠

---

## 📞 Version Info

- **Current Version:** 2.0
- **Last Updated:** November 2025
- **Total Features:** 30+
- **Lines of Code:** ~2,500+
- **Development Time:** Iterative enhancement
