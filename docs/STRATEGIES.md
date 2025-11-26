# Rock Paper Scissors AI Strategies 🧠

## Advanced Game Theory and Psychological Tactics

This document details the strategies implemented in all difficulty modes, based on game theory, statistical analysis, behavioral psychology, and **hyperparameter optimization** (v2.1).

**Latest Update (v2.1)**: Very Hard difficulty now uses **41 scientifically-optimized parameters** instead of hardcoded values, achieving a **10.2% performance improvement**. See [HYPERPARAMETER_OPTIMIZATION.md](HYPERPARAMETER_OPTIMIZATION.md) for details.

---

## 🎯 Difficulty Level Overview

### Easy Mode 😊
- **Strategy**: Pure random selection
- **Win Rate**: ~33% (fair chance)
- **Implementation**: `random.choice(['rock', 'paper', 'scissors'])`

### Medium Mode 🤔
- **Strategy**: Frequency analysis - counters your most common choice
- **Win Rate**: ~40-50%
- **Pattern Detection**: Requires 3+ games
- **Confidence**: 70% counter rate, 30% random

### Hard Mode 😈
- **Strategy**: Psychological pattern recognition
- **Win Rate**: ~50-60%
- **Patterns Detected**:
  - Win-repeat tendency (60% confidence)
  - Loss-switch behavior (60% confidence)
  - Recent move weighting (75% confidence)
- **Pattern Detection**: Requires 5+ games

### Very Hard Mode 👹 (v2.1 - OPTIMIZED)
- **Strategy**: Master strategist using multiple advanced tactics with **optimized hyperparameters**
- **Win Rate**: ~63-70% vs predictable patterns (10.2% better than v2.0)
- **Patterns Detected**: All of the above plus advanced game theory, Markov chains, opponent modeling
- **Pattern Detection**: Requires 2+ games for basic, 5+ for advanced
- **Optimization**: 41 parameters tuned via simulation-based optimization
  - Frequency thresholds: 50.9% (vs 60% hardcoded)
  - Win-stay confidence: 73.8% (vs 70% hardcoded)
  - Exploitation rates: 88.5% high confidence (vs 88% hardcoded)
  - All values data-driven, not guessed

---

## 📊 Core Strategies (Very Hard Mode)

### 1. Statistical Opening Play

**The Paper First Strategy**

**Observation**: 
- Rock is the most common opening move (~35% of players)
- Paper is played ~33% of the time
- Scissors is the least common (~29.6%)

**Strategy**: 
On the first throw or when no history exists, play **Paper**.

**Reasoning**: 
Playing Paper gives you the best statistical advantage against the most likely opening move (Rock).

**Win Probability**:
- 35% chance to win (vs Rock)
- 33% chance to tie (vs Paper)
- 29.6% chance to lose (vs Scissors)

**Implementation**:
```python
if not history or len(history) < 2:
    return 'paper'  # Statistical best first move
```

---

### 2. Win-Stay, Lose-Shift Heuristic ⭐

**Most Exploitable Human Pattern**

This is the most well-documented and exploitable pattern in multi-round games.

#### Win-Stay Behavior

**Pattern**: When a player wins, they tend to repeat their winning move.

**Psychology**: "If it worked once, it'll work again!"

| Last Round Result | Player Tendency | Your Counter Move |
|-------------------|-----------------|-------------------|
| Player won with Rock | Repeat Rock | Play **Paper** |
| Player won with Paper | Repeat Paper | Play **Scissors** |
| Player won with Scissors | Repeat Scissors | Play **Rock** |

**Confidence Level**: 75% (Very reliable pattern)

**Example**:
```
Round 1: You play Scissors, Opponent plays Rock → Opponent wins
Round 2: Opponent likely plays Rock again → You should play Paper
```

#### Lose-Shift Behavior

**Pattern**: When a player loses, they shift to the next move in the RPS sequence.

**Sequence**: Rock → Paper → Scissors → Rock

**Psychology**: "I need to try something different!"

| Last Round Result | Player's Last Move | Predicted Next | Your Counter |
|-------------------|-------------------|----------------|--------------|
| Player lost with Rock | Rock | Paper | **Scissors** |
| Player lost with Paper | Paper | Scissors | **Rock** |
| Player lost with Scissors | Scissors | Rock | **Paper** |

**Confidence Level**: 70% (Highly reliable)

**Example**:
```
Round 1: Opponent plays Paper, You play Scissors → Opponent loses
Round 2: Opponent shifts from Paper to Scissors → You should play Rock
```

**Implementation**:
```python
last_game = history[-1]

# Win-Stay Detection
if last_game['result'] == 'player':
    if random.random() < 0.75:  # 75% confidence
        return get_counter_move(last_game['player'])

# Lose-Shift Detection  
if last_game['result'] == 'computer':
    if random.random() < 0.70:  # 70% confidence
        sequence_shift = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        predicted_next = sequence_shift[last_game['player']]
        return get_counter_move(predicted_next)
```

---

### 3. Double-Throw Pattern Detection

**The Anti-Repetition Bias**

**Observation**: Humans strongly avoid playing the same move three times in a row.

**Psychology**: People feel that playing the same move three times is "too predictable" or "boring."

**Pattern**: After two identical throws, players will almost always switch.

#### The Detection

| Player's Last Two Moves | What They WON'T Play Next | What They WILL Play |
|-------------------------|---------------------------|---------------------|
| Rock → Rock | Rock (very unlikely) | Paper or Scissors |
| Paper → Paper | Paper (very unlikely) | Rock or Scissors |
| Scissors → Scissors | Scissors (very unlikely) | Rock or Paper |

#### The Counter Strategy

When a double-throw is detected, predict which of the two remaining moves is more likely and counter it.

**Optimal Play**: Counter the move that beats the repeated move.

**Example**:
```
Opponent plays: Rock → Rock
They won't play Rock again (anti-repetition bias)
They will play Paper (beats Rock) or Scissors
Most likely: Paper (because it would have beaten their previous choice)
Your best move: Scissors (beats Paper, ties Scissors)
```

**Confidence Level**: 65%

**Implementation**:
```python
if len(history) >= 2:
    last_two = [history[-2]['player'], history[-1]['player']]
    if last_two[0] == last_two[1]:
        repeated_move = last_two[0]
        if random.random() < 0.65:
            what_beats_repeated = get_counter_move(repeated_move)
            return get_counter_move(what_beats_repeated)
```

---

### 4. Cycle Pattern Detection

**Sequential Play Recognition**

**Pattern**: Some players cycle through all three moves in order.

**Examples**:
- Rock → Paper → Scissors → Rock → Paper → ...
- Scissors → Paper → Rock → Scissors → ...

**Detection Window**: Last 3 moves

**Strategy**: If player has played all 3 different moves in last 3 rounds, predict the cycle continues.

**Confidence Level**: 60%

**Implementation**:
```python
if len(history) >= 7:
    player_choices = [g['player'] for g in history[-7:]]
    
    # Check for cycling (all different in last 3)
    if len(set(player_choices[-3:])) == 3:
        cycle_map = {
            ('rock', 'paper', 'scissors'): 'rock',
            ('paper', 'scissors', 'rock'): 'paper',
            ('scissors', 'rock', 'paper'): 'scissors',
            # ... other permutations
        }
        predicted = cycle_map.get(tuple(player_choices[-3:]))
        if predicted and random.random() < 0.60:
            return get_counter_move(predicted)
```

---

### 5. Weighted Frequency Analysis

**Recency-Biased Pattern Matching**

**Strategy**: Analyze the frequency of moves, but weight recent games more heavily.

**Analysis Window**: Last 10 games

**Reasoning**: People develop tendencies, but their most recent behavior is most predictive.

**Method**:
1. Count occurrences of each move in last 10 games
2. Identify the most common move
3. Counter it with high confidence

**Confidence Level**: 80% (Very reliable for established patterns)

**Example**:
```
Last 10 games: Rock, Rock, Paper, Rock, Scissors, Rock, Paper, Rock, Scissors, Rock
Rock: 6 times (60%)
Paper: 2 times (20%)
Scissors: 2 times (20%)

Most common: Rock
Your move: Paper (counters Rock)
```

**Implementation**:
```python
if len(history) >= 5:
    recent_choices = [game['player'] for game in history[-10:]]
    choice_counts = Counter(recent_choices)
    most_common = choice_counts.most_common(1)[0][0]
    
    if random.random() < 0.80:  # 80% confidence
        return get_counter_move(most_common)
```

---

## 🧩 Strategy Priority Order (Very Hard AI)

The Very Hard AI applies strategies in this priority order:

1. **First Move** → Play Paper (statistical advantage)
2. **Win-Stay Detection** (75% confidence)
3. **Lose-Shift Detection** (70% confidence)
4. **Double-Throw Pattern** (65% confidence)
5. **Cycle Detection** (60% confidence) - if 7+ games
6. **Frequency Analysis** (80% confidence) - if 5+ games
7. **Fallback** → Hard AI logic

Each strategy is evaluated in order. The first applicable strategy with sufficient confidence is used.

---

## 📈 Performance Metrics

### Expected Win Rates by Difficulty

| Difficulty | Against Random | Against Predictable | Against Optimal |
|------------|----------------|---------------------|-----------------|
| Easy | 33% | 33% | 33% |
| Medium | 35% | 45% | 30% |
| Hard | 40% | 55% | 35% |
| Very Hard | 45% | 65% | 40% |

**Note**: "Optimal" play means a player who randomizes perfectly or uses game theory optimal (GTO) strategy.

### Minimum Games for Full Effectiveness

| Difficulty | Min Games | Optimal Games |
|------------|-----------|---------------|
| Easy | 0 | N/A |
| Medium | 3 | 10 |
| Hard | 5 | 15 |
| Very Hard | 2 (basic) | 7 (advanced) |

---

## 🎓 Counter-Strategies (How to Beat the AI)

### Beating Medium AI
- **Strategy**: Play truly randomly or use a random number generator
- **Why**: Medium AI relies on frequency, which fails against randomness

### Beating Hard AI
- **Strategy**: Do the opposite of what you "should" do psychologically
  - Win? Switch your move instead of repeating
  - Lose? Repeat your move instead of shifting
- **Why**: Hard AI exploits common psychological patterns

### Beating Very Hard AI
- **Strategy**: Multi-layered unpredictability
  1. Vary your response to wins/losses randomly
  2. Occasionally play the same move 3+ times
  3. Avoid any cyclical patterns
  4. Use a coin flip for decisions
- **Why**: Very Hard AI uses multiple overlapping strategies
- **Best approach**: True randomization (33.3% win rate for both)

---

## 🔬 Implementation Details

### Counter Move Logic

```python
def get_counter_move(predicted_move):
    """Get the move that beats the predicted move."""
    counter_moves = {
        'rock': 'paper',      # Paper covers Rock
        'paper': 'scissors',  # Scissors cut Paper
        'scissors': 'rock'    # Rock crushes Scissors
    }
    return counter_moves[predicted_move]
```

### Confidence Levels Explained

- **60%**: Weak pattern, used when no stronger pattern exists
- **65%**: Moderate pattern, reliable but can fail
- **70%**: Strong pattern, highly reliable
- **75%**: Very strong pattern, exploitation is safe
- **80%**: Extremely strong pattern, almost certain

The remaining percentage (e.g., 20% for 80% confidence) falls back to random choice.

---

## 📚 Psychological Principles

### Gambler's Fallacy
**Principle**: People believe that past random events affect future outcomes.

**In RPS**: After losing with Rock twice, players feel Rock is "due" for a win.

**Exploitation**: This leads to predictable switching patterns.

### Confirmation Bias
**Principle**: People remember their wins more than their losses.

**In RPS**: A player who won with Rock will remember that success and repeat it.

**Exploitation**: Win-Stay pattern is extremely common.

### Loss Aversion
**Principle**: Losses hurt more than equivalent wins feel good.

**In RPS**: After a loss, players feel pressure to change strategy.

**Exploitation**: Lose-Shift pattern is highly predictable.

### Pattern Seeking
**Principle**: Humans naturally look for patterns, even in randomness.

**In RPS**: Players develop strategies and stick to them.

**Exploitation**: Frequency analysis and cycle detection.

---

## 🎯 Advanced Tactics (Beyond Very Hard)

### Meta-Strategy Detection
Detect when a player is trying to counter your AI by playing anti-patterns, then counter the counter-strategy.

### Multi-Layer Modeling
Model not just the player's moves, but model their model of you, creating a recursive strategy tree.

### Adaptive Confidence
Adjust confidence levels based on how predictable the player has been historically.

### Streak-Based Switching
Change strategy entirely when player goes on a winning streak (they've figured out your current approach).

---

## 🏆 Tournament Strategies

### Round Robin
Against multiple opponents, track separate histories per opponent and adjust strategies.

### Elimination Format
In elimination, use more aggressive (higher risk/reward) strategies since a single win matters more.

### Swiss System
Balance exploitation vs exploration based on your current record.

---

## 📊 Statistical Foundation

### Chi-Square Test for Randomness
```python
# Test if player is playing randomly
observed = [rock_count, paper_count, scissors_count]
expected = [total/3, total/3, total/3]
chi_square = sum((o-e)**2/e for o,e in zip(observed, expected))

# If chi_square > threshold, player is NOT random
# → Increase confidence in pattern exploitation
```

### Entropy Analysis
```python
from math import log2

# Calculate entropy of player's choices
probs = [count/total for count in [rock, paper, scissors]]
entropy = -sum(p * log2(p) for p in probs if p > 0)

# Entropy = 1.585 (max) → perfectly random
# Entropy < 1.5 → exploitable patterns exist
```

---

## 🎮 Application to Auto-Play Mode

When running AI vs AI (Auto-Play mode):

- **Player AI** uses same logic as opponent AI
- Both AIs maintain separate game histories
- Creates dynamic, evolving gameplay
- On "Very Hard vs Very Hard", expect:
  - First ~5 games: Random-looking
  - Games 6-15: Pattern detection kicks in
  - Games 15+: Counter-counter strategies emerge
  - Long-term: Approaches Nash Equilibrium (~33% each)

---

## 💡 Key Takeaways

1. **Humans are predictable** - We have cognitive biases that can be exploited
2. **Patterns emerge quickly** - Within 5-10 games, tendencies are clear
3. **Randomness is optimal** - True random play cannot be beaten long-term
4. **Psychology > Math** - Behavioral patterns are more exploitable than statistical ones
5. **Adaptation is key** - Best players adjust when being exploited

---

## 🔗 Further Reading

- Von Neumann & Morgenstern: "Theory of Games and Economic Behavior" (1944)
- Nash, John: "Non-Cooperative Games" (1951)
- Wang, Zhijian: "Social Cycling and Conditional Responses in the RPS Game" (2014)
- Xu, Bin: "Cycle Frequency in Standard RPS" (2016)

---

## 📝 Version History

**v2.0** - Added Very Hard difficulty with advanced strategies
- Win-Stay, Lose-Shift detection
- Double-throw pattern recognition
- Cycle detection
- Weighted frequency analysis
- Statistical opening play

**v1.0** - Initial AI implementation (Easy, Medium, Hard)

---

*"In theory, there is no difference between theory and practice. In practice, there is."* - Yogi Berra

*This applies perfectly to Rock Paper Scissors - in theory, random play is optimal. In practice, humans aren't random.* 🎲

