# Testing Directory

This directory contains all testing tools, scripts, and results for the Rock Paper Scissors AI system.

---

## 🧪 Testing Tools

### Main Evaluators
- **[ai_evaluator.py](ai_evaluator.py)** - Tests AI performance vs various human strategies
  - Random play
  - Always Rock/Paper/Scissors
  - Cycle patterns
  - Win-Stay-Lose-Shift
  - Anti-AI strategies

- **[ai_vs_ai_evaluator.py](ai_vs_ai_evaluator.py)** - Tests AI difficulties against each other
  - All 12 matchup combinations
  - Nash equilibrium validation
  - Difficulty scaling verification

### Statistical Analysis
- **[statistical_tests.py](statistical_tests.py)** - Statistical analysis tools
  - Chi-square randomness tests
  - Pattern detection validation
  - Performance metrics

- **[visualization.py](visualization.py)** - Data visualization tools
  - Win rate charts
  - Pattern heatmaps
  - Performance graphs

### Interactive Tools
- **[demo.py](demo.py)** - Interactive testing demo
- **[run_tests.sh](run_tests.sh)** - Convenient test runner script

---

## 📊 Test Results

Located in: `results/`

### Latest Results
- **ai_evaluation_20251125_102036.json** - AI vs Human strategies (20,000 games)
- **ai_vs_ai_evaluation_20251125_102804.json** - AI vs AI matchups (12,000 games)

### Comprehensive Analysis
See: **[../docs/testing-results/TEST_RESULTS.md](../docs/testing-results/TEST_RESULTS.md)**

---

## 📦 Archive

Located in: `archive/`

Old test scripts and deprecated tools:
- **test_mcp.py** - Old MCP testing script
- **test_mcp_protocol.py** - Old protocol testing script

---

## 🚀 Quick Start

### Run Quick Test (100 games)
```bash
./run_tests.sh quick
```

### Run Pattern Exploitation Test
```bash
./run_tests.sh pattern
```

### Run Full Test Suite (1000+ games)
```bash
./run_tests.sh full 1000
```

### Run AI vs AI Tests
```bash
python3 ai_vs_ai_evaluator.py --full 1000
```

### View Latest Results
```bash
./run_tests.sh visualize
```

---

## 📚 Documentation

- **[README.md](README.md)** - Complete testing documentation (this file)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[requirements.txt](requirements.txt)** - Testing dependencies

---

## 📁 Directory Structure

```
testing/
├── README.md (detailed docs)
├── QUICKSTART.md
├── requirements.txt
├── ai_evaluator.py
├── ai_vs_ai_evaluator.py
├── statistical_tests.py
├── visualization.py
├── demo.py
├── run_tests.sh
├── results/
│   ├── ai_evaluation_20251125_102036.json
│   └── ai_vs_ai_evaluation_20251125_102804.json
└── archive/
    ├── test_mcp.py
    └── test_mcp_protocol.py
```

---

## 🎯 Test Results Summary

### AI vs Human Strategies (20,000 games)
- Easy: 33% avg (perfect random)
- Medium: 57.7% avg (pattern detection)
- Hard: 47.0% avg (psychological patterns)
- **Very Hard: 82.6% avg** (dominant!) ⭐

### AI vs AI (12,000 games)
- All difficulties: ~33% avg
- Validates Nash equilibrium
- Proves AIs are optimized for humans, not each other

**Overall Grade**: A (Production Ready)

---

**Last Updated**: November 25, 2025
