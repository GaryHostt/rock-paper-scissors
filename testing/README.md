# AI Performance Evaluation System

This directory contains tools for comprehensively testing and evaluating the Rock Paper Scissors AI difficulty levels.

## 📁 Files

### `ai_evaluator.py`
Main evaluation framework that tests AI performance against various player strategies.

**Features:**
- Simulate different player strategies (random, always_rock, cycle, win-stay-lose-shift, anti-ai)
- Test all difficulty levels (easy, medium, hard, veryhard)
- Generate comprehensive reports
- Save results to JSON

**Usage:**
```bash
# Quick test (100 games per difficulty with random strategy)
python ai_evaluator.py --quick

# Test pattern exploitation
python ai_evaluator.py --pattern

# Full comprehensive test (1000 games per test)
python ai_evaluator.py --full

# Custom number of games
python ai_evaluator.py --full 500
```

### `statistical_tests.py`
Statistical analysis tools for evaluating AI performance.

**Features:**
- Chi-square test for randomness
- Confidence intervals for win rates
- Pattern exploitation rate analysis
- Entropy analysis
- AI comparison tests

**Usage:**
```python
from statistical_tests import chi_square_randomness_test, win_rate_confidence_interval

# Test if AI is truly random
chi_square_randomness_test(['rock', 'paper', 'scissors', ...])

# Calculate confidence interval
win_rate_confidence_interval(wins=45, total=100, confidence=0.95)
```

### `visualization.py`
Visualization tools for AI performance analysis.

**Features:**
- Win rate comparison charts
- Performance trends over time
- Strategy effectiveness heatmaps
- Confidence interval plots

**Usage:**
```bash
python visualization.py results.json
```

### `requirements.txt`
Required Python packages for testing framework.

## 🧪 Testing Strategy

### 1. Randomness Test (Easy AI)
Tests if Easy AI truly plays randomly (~33% win rate against all strategies).

**Expected:**
- Chi-square test should NOT reject null hypothesis
- Win rate ≈ 33% ± 5% against all strategies

### 2. Pattern Exploitation Test (Medium/Hard/Very Hard)
Tests if AI can detect and exploit player patterns.

**Expected Win Rates (AI's perspective):**

| Strategy | Easy | Medium | Hard | Very Hard |
|----------|------|--------|------|-----------|
| Random | 33% | 33% | 33% | 33% |
| Always Rock | 33% | 60% | 70% | 75% |
| Cycle | 33% | 50% | 60% | 70% |
| Win-Stay-Lose-Shift | 33% | 50% | 65% | 75% |
| Anti-AI | 33% | 40% | 50% | 60% |

### 3. Confidence Intervals
All results should include 95% confidence intervals to ensure statistical significance.

### 4. Pattern Recognition Rate
Measure how often AI successfully exploits specific patterns:
- Win-Stay detection rate
- Lose-Shift detection rate
- Double-throw detection rate

## 📊 Running Tests

### Prerequisites
```bash
# Make sure Flask server is running
cd ..
python3 app.py

# In another terminal, install requirements
pip3 install -r testing/requirements.txt
```

### Quick Validation
```bash
cd testing
python ai_evaluator.py --quick
```

Expected output:
```
Testing EASY difficulty
Strategy: random, Games: 100
  Game 100: Win Rate = 34.0% | Loss Rate = 33.0%

📊 Results:
  Agent Wins:    34 (34.0%)
  Agent Losses:  33 (33.0%)
  Ties:          33 (33.0%)

  AI Win Rate: 33.0%
```

### Full Test Suite
```bash
python ai_evaluator.py --full 1000
```

This runs 20 tests (4 difficulties × 5 strategies) with 1000 games each.
Total games: 20,000
Estimated time: 10-15 minutes

### Interpreting Results

✅ **PASS** - AI performance within 10% of expected
- Easy: Should always be ~33%
- Medium/Hard/Very Hard: Should exploit patterns as expected

⚠️ **CHECK** - AI performance 10-15% off expected  
- May need tuning of confidence parameters
- Check if sample size is sufficient

❌ **FAIL** - AI performance >15% off expected
- Algorithm may have bugs
- Pattern detection not working correctly

## 🔬 Statistical Validation

### Chi-Square Test
For Easy mode, run chi-square test to verify randomness:

```python
from statistical_tests import chi_square_randomness_test

# Get AI choices from test run
ai_choices = [game['opponent_choice'] for game in history]
chi_square_randomness_test(ai_choices)
```

Expected: p-value > 0.05 (cannot reject randomness)

### Confidence Intervals
Check if results are statistically significant:

```python
from statistical_tests import win_rate_confidence_interval

win_rate_confidence_interval(wins=70, total=100, confidence=0.95)
# Should output: [60.5%, 78.2%] or similar
```

### Pattern Exploitation
Measure how well AI exploits patterns:

```python
from statistical_tests import pattern_exploitation_rate

pattern_exploitation_rate(game_history)
# Expected for Very Hard: 70-80% exploitation rate
```

## 📈 Continuous Monitoring

### A/B Testing
When improving AI algorithms:

```python
# Test old version
results_v1 = evaluator.run_test_suite('veryhard', num_games=1000, strategy='win_stay_lose_shift')

# Test new version (after changes)
results_v2 = evaluator.run_test_suite('veryhard', num_games=1000, strategy='win_stay_lose_shift')

# Compare
from statistical_tests import compare_two_ais
compare_two_ais(results_v1, results_v2, 'Old AI', 'New AI')
```

### Regression Testing
Before deploying changes, run full test suite:

```bash
# Run all tests
python ai_evaluator.py --full 1000 > test_results_$(date +%Y%m%d).log

# Check for any FAIL status
grep "FAIL" test_results_*.log
```

## 🎯 Performance Benchmarks

### Minimum Acceptable Performance

| Difficulty | Min Win Rate vs Random | Min Win Rate vs Always_Rock | Min Win Rate vs WSLS |
|------------|------------------------|----------------------------|----------------------|
| Easy | 28-38% | 28-38% | 28-38% |
| Medium | 28-38% | 55-65% | 45-55% |
| Hard | 28-38% | 65-75% | 60-70% |
| Very Hard | 28-38% | 70-80% | 70-80% |

If AI performs below minimum against predictable strategies, it needs improvement.
If AI performs above 38% against true random, it's not following Nash equilibrium.

## 🐛 Debugging Failed Tests

If tests fail:

1. **Check server is running**: `curl http://localhost:5000/api/play -X POST -H "Content-Type: application/json" -d '{"choice":"rock","difficulty":"easy","history":[]}'`

2. **Verify MCP endpoint**: `curl http://localhost:5000/mcp/play -X POST -H "Content-Type: application/json" -d '{"agent_id":"test","choice":"rock","opponent_difficulty":"easy"}'`

3. **Check logs**: Look at Flask server output for errors

4. **Reduce sample size**: Try with 100 games first to debug faster

5. **Test individual strategies**: Run pattern test to isolate issues

## 📚 Further Reading

- `../STRATEGIES.md` - Detailed AI strategy documentation
- `../README.md` - Project overview
- `results/*.json` - Historical test results

## 🤝 Contributing

When adding new AI strategies:

1. Update expected win rates in this file
2. Run full test suite
3. Document any changes to algorithms
4. Commit test results to version control

