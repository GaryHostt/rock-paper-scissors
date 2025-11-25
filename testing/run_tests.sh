#!/bin/bash
# AI Evaluation Test Runner
# Convenient wrapper for running AI tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to testing directory
cd "$(dirname "$0")"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Rock Paper Scissors AI Testing Framework     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"

# Check if Flask server is running
if ! curl -s http://localhost:5000/api/play > /dev/null 2>&1; then
    echo -e "${RED}Error: Flask server is not running!${NC}"
    echo -e "${YELLOW}Please start the server first:${NC}"
    echo -e "  cd .."
    echo -e "  python3 app.py"
    exit 1
fi

echo -e "${GREEN}✓ Flask server is running${NC}\n"

# Parse command
case "${1:-help}" in
    quick)
        echo -e "${YELLOW}Running quick test (100 games per difficulty)...${NC}\n"
        python3 ai_evaluator.py --quick
        ;;
    
    pattern)
        echo -e "${YELLOW}Running pattern exploitation test...${NC}\n"
        python3 ai_evaluator.py --pattern
        ;;
    
    full)
        GAMES=${2:-1000}
        echo -e "${YELLOW}Running full test suite (${GAMES} games per test)...${NC}"
        echo -e "${YELLOW}This will take ~10-15 minutes...${NC}\n"
        python3 ai_evaluator.py --full ${GAMES}
        ;;
    
    demo)
        echo -e "${YELLOW}Running interactive demo...${NC}\n"
        python3 demo.py
        ;;
    
    visualize)
        if [ -z "$2" ]; then
            # Find most recent results file
            LATEST=$(ls -t ai_evaluation_*.json 2>/dev/null | head -1)
            if [ -z "$LATEST" ]; then
                echo -e "${RED}No results files found!${NC}"
                echo -e "${YELLOW}Run a test first:${NC} ./run_tests.sh quick"
                exit 1
            fi
            echo -e "${YELLOW}Visualizing latest results: ${LATEST}${NC}\n"
            python3 visualization.py "$LATEST"
        else
            echo -e "${YELLOW}Visualizing: $2${NC}\n"
            python3 visualization.py "$2"
        fi
        ;;
    
    clean)
        echo -e "${YELLOW}Cleaning up test results and charts...${NC}"
        rm -f ai_evaluation_*.json
        rm -f *.png
        echo -e "${GREEN}✓ Cleanup complete${NC}"
        ;;
    
    install)
        echo -e "${YELLOW}Installing testing dependencies...${NC}\n"
        pip3 install -r requirements.txt
        echo -e "\n${GREEN}✓ Dependencies installed${NC}"
        ;;
    
    help|*)
        echo -e "\n${BLUE}Available Commands:${NC}\n"
        echo -e "  ${GREEN}quick${NC}              Quick test (100 games)"
        echo -e "  ${GREEN}pattern${NC}            Test pattern exploitation"
        echo -e "  ${GREEN}full [N]${NC}           Full test suite (N games, default 1000)"
        echo -e "  ${GREEN}demo${NC}               Run interactive demo"
        echo -e "  ${GREEN}visualize [file]${NC}   Generate charts (latest or specified file)"
        echo -e "  ${GREEN}clean${NC}              Remove all test results and charts"
        echo -e "  ${GREEN}install${NC}            Install testing dependencies"
        echo -e "  ${GREEN}help${NC}               Show this message"
        echo -e "\n${BLUE}Examples:${NC}\n"
        echo -e "  ./run_tests.sh quick"
        echo -e "  ./run_tests.sh full 500"
        echo -e "  ./run_tests.sh visualize"
        echo -e "  ./run_tests.sh visualize ai_evaluation_20250124.json"
        echo -e "\n${BLUE}Documentation:${NC}"
        echo -e "  README.md        - Complete testing documentation"
        echo -e "  QUICKSTART.md    - Quick start guide"
        echo ""
        ;;
esac

