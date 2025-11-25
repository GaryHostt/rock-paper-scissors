# Quick Start Guide - AI Evaluation

This guide will help you quickly get started with the AI evaluation framework.

## 🚀 Setup (One Time)

1. **Install testing dependencies:**
```bash
cd testing
pip3 install -r requirements.txt
```

2. **Make sure Flask server is running:**
```bash
# In another terminal
cd ..
python3 app.py
```

## 🧪 Run Your First Test

### Option 1: Quick Test (Recommended for first time)

Test Easy difficulty with 100 random games:

```bash
cd testing
python ai_evaluator.py --quick
```

**Expected output:**
```
🎯 QUICK TEST - Random Strategy vs All Difficulties
This should show ~33% AI win rate for all difficulties

Testing EASY difficulty
Strategy: random, Games: 100
  Game 100: Win Rate = 34.0% | Loss Rate = 33.0%

📊 Results:
  Agent Wins:    34 (34.0%)
  Agent Losses:  33 (33.0%)
  Ties:          33 (33.0%)

  AI Win Rate: 33.0%
```

✅ **PASS**: If AI win rate is between 28-38%

### Option 2: Pattern Test

Test if AIs can exploit patterns:

```bash
python ai_evaluator.py --pattern
```

This tests how well each difficulty exploits the "always_rock" strategy.

**Expected results:**
- Easy: ~33% (random)
- Medium: 55-65% (should counter)
- Hard: 65-75% (strong counter)
- Very Hard: 70-80% (very strong counter)

### Option 3: Full Test Suite

Run comprehensive tests (20 tests, ~10-15 minutes):

```bash
python ai_evaluator.py --full 1000
```

This runs 1000 games for each of 20 test combinations.

**What it tests:**
- 4 difficulty levels × 5 player strategies
- Generates detailed performance report
- Saves results to JSON file

## 📊 Understanding Results

### Test Output Format

```
Difficulty   Strategy              AI Win %   Expected   Diff      Status
----------------------------------------------------------------------------
easy         random                   33.2%      33%      +0.2%    ✅ PASS
medium       always_rock              61.4%      60%      +1.4%    ✅ PASS
hard         win_stay_lose_shift      68.1%      65%      +3.1%    ✅ PASS
veryhard     cycle                    72.3%      70%      +2.3%    ✅ PASS
```

### Status Indicators

- ✅ **PASS**: AI performance within 10% of expected (good!)
- ⚠️ **CHECK**: AI performance 10-15% off expected (needs review)
- ❌ **FAIL**: AI performance >15% off expected (needs fixing)

### Key Insights

1. **All AIs should win ~33% against random** (Nash equilibrium)
2. **Easy should always be ~33%** (it's truly random)
3. **Medium/Hard/Very Hard should exploit patterns** (higher win rates)

## 📈 Visualize Results

After running a full test, visualize the results:

```bash
# Find the most recent results file
ls -t ai_evaluation_*.json | head -1

# Generate charts
python visualization.py ai_evaluation_20250124_120000.json
```

This creates:
- `win_rate_comparison.png` - Bar chart of all results
- `performance_heatmap.png` - Heatmap showing performance
- `difficulty_progression.png` - Line chart of difficulty scaling

## 🔬 Statistical Tests

Test if Easy mode is truly random:

```python
from statistical_tests import chi_square_randomness_test

# After running a test with history tracking
chi_square_randomness_test(ai_choices)
```

Calculate confidence intervals:

```python
from statistical_tests import win_rate_confidence_interval

win_rate_confidence_interval(wins=65, total=100, confidence=0.95)
# Output: 95% CI: [55.2%, 73.8%]
```

## 🐛 Troubleshooting

### "Connection refused"
**Problem:** Flask server isn't running  
**Solution:** Start the server: `python3 app.py`

### "ModuleNotFoundError"
**Problem:** Missing dependencies  
**Solution:** Install them: `pip3 install -r requirements.txt`

### Tests taking too long
**Problem:** Full test suite is slow (1000 games × 20 tests)  
**Solution:** Use fewer games: `python ai_evaluator.py --full 100`

### Results seem off
**Problem:** Statistical variance with small samples  
**Solution:** Run more games (1000+) for more accurate results

## 💡 Tips

1. **Start small**: Use `--quick` first to verify everything works
2. **Check Easy mode**: Should always be ~33%, good sanity check
3. **Run overnight**: Full test suite with 1000+ games takes time
4. **Save results**: JSON files are automatically saved with timestamps
5. **Compare versions**: Use saved results to track improvements

## 📚 Next Steps

- Read `testing/README.md` for complete documentation
- Check `../STRATEGIES.md` for AI algorithm details
- Experiment with custom test scenarios
- Contribute improvements to the test framework!

## 🎯 Quick Reference

```bash
# Quick validation
python ai_evaluator.py --quick

# Pattern exploitation test
python ai_evaluator.py --pattern

# Full test suite
python ai_evaluator.py --full 1000

# Generate charts
python visualization.py results.json

# Statistical analysis (in Python)
from statistical_tests import *
```

Happy testing! 🎮

