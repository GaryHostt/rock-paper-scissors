#!/usr/bin/env python3
"""
Demo script for the AI evaluation framework
Run this to see a quick demonstration of the testing system
"""

import sys
import os

# Add parent directory to path to import the evaluator
sys.path.insert(0, os.path.dirname(__file__))

from ai_evaluator import AIEvaluator
from statistical_tests import chi_square_randomness_test, win_rate_confidence_interval

def demo():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         AI Performance Evaluation - Demo                     ║")
    print("║         Rock Paper Scissors AI Testing Framework             ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    evaluator = AIEvaluator()
    
    # Test 1: Easy mode should be random
    print("\n" + "="*65)
    print("TEST 1: Verifying Easy Mode Randomness")
    print("="*65)
    print("Hypothesis: Easy AI should win ~33% against all strategies\n")
    
    result_easy_random = evaluator.run_test_suite(
        difficulty='easy',
        num_games=100,
        strategy='random',
        verbose=True
    )
    
    # Test 2: Hard mode should exploit patterns
    print("\n" + "="*65)
    print("TEST 2: Verifying Hard Mode Pattern Exploitation")
    print("="*65)
    print("Hypothesis: Hard AI should exploit 'always_rock' strategy\n")
    
    result_hard_rock = evaluator.run_test_suite(
        difficulty='hard',
        num_games=100,
        strategy='always_rock',
        verbose=True
    )
    
    # Test 3: Very Hard should dominate
    print("\n" + "="*65)
    print("TEST 3: Verifying Very Hard Mode Superiority")
    print("="*65)
    print("Hypothesis: Very Hard should win 70%+ against predictable play\n")
    
    result_veryhard_wsls = evaluator.run_test_suite(
        difficulty='veryhard',
        num_games=100,
        strategy='win_stay_lose_shift',
        verbose=True
    )
    
    # Statistical Analysis
    print("\n" + "="*65)
    print("STATISTICAL ANALYSIS")
    print("="*65)
    
    # Confidence interval for Easy mode
    win_rate_confidence_interval(
        wins=result_easy_random['wins'],
        total=result_easy_random['total_games'],
        confidence=0.95
    )
    
    # Summary
    print("\n" + "="*65)
    print("DEMO SUMMARY")
    print("="*65)
    print(f"\nTest 1 - Easy Random:       AI won {result_easy_random['loss_rate']:.1f}%")
    print(f"  Expected: 28-38%          Status: {'✅ PASS' if 28 <= result_easy_random['loss_rate'] <= 38 else '❌ FAIL'}")
    
    print(f"\nTest 2 - Hard vs Always Rock: AI won {result_hard_rock['loss_rate']:.1f}%")
    print(f"  Expected: 65-75%          Status: {'✅ PASS' if 65 <= result_hard_rock['loss_rate'] <= 75 else '❌ FAIL'}")
    
    print(f"\nTest 3 - Very Hard vs WSLS:  AI won {result_veryhard_wsls['loss_rate']:.1f}%")
    print(f"  Expected: 70-80%          Status: {'✅ PASS' if 70 <= result_veryhard_wsls['loss_rate'] <= 80 else '❌ FAIL'}")
    
    print("\n" + "="*65)
    print("Demo complete! Run with more games for accurate results:")
    print("  python ai_evaluator.py --full 1000")
    print("="*65)

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError running demo: {e}")
        print("\nMake sure:")
        print("  1. Flask server is running (python3 app.py)")
        print("  2. Dependencies are installed (pip3 install -r requirements.txt)")
        sys.exit(1)

