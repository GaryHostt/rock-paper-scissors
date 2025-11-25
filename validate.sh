#!/bin/bash
# Quick validation script to check if all components are working

echo "🔍 Validating Rock Paper Scissors v2.1 Implementation"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to project root
cd "$(dirname "$0")"

checks_passed=0
checks_failed=0

# Check 1: Flask server files
echo -n "✓ Checking Flask backend... "
if [ -f "app.py" ] && grep -q "ai_very_hard" app.py; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 2: HTML streak visualization
echo -n "✓ Checking streak visualization HTML... "
if [ -f "templates/index.html" ] && grep -q "streak-display" templates/index.html; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 3: CSS animations
echo -n "✓ Checking streak animations CSS... "
if [ -f "static/style.css" ] && grep -q "streakPulse" static/style.css; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 4: JavaScript streak logic
echo -n "✓ Checking streak update function... "
if [ -f "static/script.js" ] && grep -q "updateStreakDisplay" static/script.js; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 5: Translations (English)
echo -n "✓ Checking English translations... "
if grep -q "streak.winning" static/script.js && grep -q "streak.losing" static/script.js; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 6: Translations (French)
echo -n "✓ Checking French translations... "
if grep -q "Série de Victoires" static/script.js && grep -q "Série de Défaites" static/script.js; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 7: Translations (Spanish)
echo -n "✓ Checking Spanish translations... "
if grep -q "Racha de Victorias" static/script.js && grep -q "Racha de Derrotas" static/script.js; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 8: Testing directory
echo -n "✓ Checking testing directory... "
if [ -d "testing" ] && [ -f "testing/ai_evaluator.py" ]; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 9: Test runner script
echo -n "✓ Checking test runner script... "
if [ -f "testing/run_tests.sh" ] && [ -x "testing/run_tests.sh" ]; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 10: Statistical tests
echo -n "✓ Checking statistical tests... "
if [ -f "testing/statistical_tests.py" ] && grep -q "chi_square_randomness_test" testing/statistical_tests.py; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 11: Visualization tools
echo -n "✓ Checking visualization tools... "
if [ -f "testing/visualization.py" ] && grep -q "plot_heatmap" testing/visualization.py; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 12: Testing documentation
echo -n "✓ Checking testing documentation... "
if [ -f "testing/README.md" ] && [ -f "testing/QUICKSTART.md" ]; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 13: Main README updated
echo -n "✓ Checking main README updates... "
if grep -q "Version 2.1" README.md && grep -q "Streak Visualization" README.md; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Check 14: Demo script
echo -n "✓ Checking demo script... "
if [ -f "testing/demo.py" ] && [ -x "testing/demo.py" ]; then
    echo -e "${GREEN}OK${NC}"
    ((checks_passed++))
else
    echo -e "${RED}FAILED${NC}"
    ((checks_failed++))
fi

# Summary
echo ""
echo "=================================================="
echo "Validation Summary:"
echo "  Passed: $checks_passed"
echo "  Failed: $checks_failed"
echo "=================================================="
echo ""

if [ $checks_failed -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Implementation is complete.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Start the server: python3 app.py"
    echo "  2. Open http://localhost:5000 in browser"
    echo "  3. Test streak visualization by playing games"
    echo "  4. Run AI tests: cd testing && ./run_tests.sh demo"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review the implementation.${NC}"
    exit 1
fi

