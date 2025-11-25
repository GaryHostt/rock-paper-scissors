#!/usr/bin/env python3
"""
Test all 4 difficulty levels against various strategies
Tests: Easy, Medium, Hard, Very Hard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import Counter
import random

# Import AI functions directly from app.py
from app import ai_easy, ai_medium, ai_hard, ai_very_hard, determine_winner, CHOICES

def simulate_player(strategy, history):
    """Simulate different player strategies"""
    
    if strategy == 'random':
        return random.choice(CHOICES)
    
    elif strategy == 'always_rock':
        return 'rock'
    
    elif strategy == 'cycle':
        # Rock -> Paper -> Scissors -> repeat
        if not history:
            return 'rock'
        return CHOICES[len(history) % 3]
    
    elif strategy == 'win_stay_lose_shift':
        if not history:
            return random.choice(CHOICES)
        last = history[-1]
        if last['result'] == 'player':
            return last['player']  # Stay
        else:
            # Shift to next
            shifts = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            return shifts[last['player']]
    
    elif strategy == 'anti_ai':
        # Try to counter AI patterns
        if len(history) < 3:
            return random.choice(CHOICES)
        # Find AI's most common choice
        ai_choices = [g['computer'] for g in history[-10:]]
        most_common = Counter(ai_choices).most_common(1)[0][0]
        counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
        return counters[most_common]
    
    return random.choice(CHOICES)

def run_test(ai_func, ai_name, strategy, num_games=1000):
    """Run test for a specific AI difficulty against a specific strategy"""
    history = []
    results = {'player': 0, 'computer': 0, 'tie': 0}
    
    print(f"\n{'='*60}")
    print(f"Testing {ai_name} vs {strategy.upper().replace('_', ' ')}")
    print(f"Running {num_games} games...")
    print(f"{'='*60}\n")
    
    for game_num in range(num_games):
        # Player makes choice
        player_choice = simulate_player(strategy, history)
        
        # AI makes choice
        if ai_name == 'Easy':
            computer_choice = ai_func()
        else:
            computer_choice = ai_func(history)
        
        # Determine winner
        result = determine_winner(player_choice, computer_choice)
        
        # Update results
        results[result] += 1
        
        # Add to history
        history.append({
            'player': player_choice,
            'computer': computer_choice,
            'result': result
        })
        
        # Progress indicator
        if (game_num + 1) % 200 == 0:
            current_ai_win_rate = (results['computer'] / (game_num + 1)) * 100
            print(f"Progress: {game_num + 1}/{num_games} games | AI Win Rate: {current_ai_win_rate:.1f}%")
    
    # Calculate final statistics
    total = sum(results.values())
    player_wins = results['player']
    ai_wins = results['computer']
    ties = results['tie']
    
    player_pct = (player_wins / total) * 100
    ai_pct = (ai_wins / total) * 100
    tie_pct = (ties / total) * 100
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {ai_name} vs {strategy.upper().replace('_', ' ')}")
    print(f"{'='*60}")
    print(f"Total Games:    {total}")
    print(f"Player Wins:    {player_wins:4d} ({player_pct:5.1f}%)")
    print(f"AI Wins:        {ai_wins:4d} ({ai_pct:5.1f}%)")
    print(f"Ties:           {ties:4d} ({tie_pct:5.1f}%)")
    print(f"{'='*60}\n")
    
    return {
        'difficulty': ai_name,
        'strategy': strategy,
        'total': total,
        'player_wins': player_wins,
        'ai_wins': ai_wins,
        'ties': ties,
        'ai_win_rate': ai_pct
    }

def main():
    """Run all tests"""
    difficulties = [
        (ai_easy, 'Easy'),
        (ai_medium, 'Medium'),
        (ai_hard, 'Hard'),
        (ai_very_hard, 'Very Hard')
    ]
    strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
    num_games = 1000
    
    print("\n" + "="*60)
    print("COMPREHENSIVE AI DIFFICULTY EVALUATION")
    print("="*60)
    print(f"Testing {len(difficulties)} difficulties × {len(strategies)} strategies")
    print(f"Games per test: {num_games}")
    print(f"Total games: {len(difficulties) * len(strategies) * num_games}")
    print("="*60)
    
    all_results = []
    
    for ai_func, ai_name in difficulties:
        print(f"\n\n{'#'*60}")
        print(f"{'#'*60}")
        print(f"  TESTING {ai_name.upper()} DIFFICULTY")
        print(f"{'#'*60}")
        print(f"{'#'*60}")
        
        difficulty_results = []
        for strategy in strategies:
            result = run_test(ai_func, ai_name, strategy, num_games)
            difficulty_results.append(result)
            all_results.append(result)
        
        # Print summary for this difficulty
        print(f"\n{'='*60}")
        print(f"{ai_name.upper()} DIFFICULTY - SUMMARY")
        print(f"{'='*60}")
        print(f"{'Strategy':<25} {'AI Wins':<10} {'Player Wins':<12} {'Ties':<8} {'AI Win %':<10}")
        print("-"*60)
        
        for result in difficulty_results:
            strategy_name = result['strategy'].replace('_', ' ').title()
            print(f"{strategy_name:<25} {result['ai_wins']:<10} {result['player_wins']:<12} {result['ties']:<8} {result['ai_win_rate']:>6.1f}%")
        
        print("="*60)
    
    # Print final comprehensive summary
    print(f"\n\n{'#'*60}")
    print(f"{'#'*60}")
    print(f"  FINAL COMPREHENSIVE SUMMARY")
    print(f"{'#'*60}")
    print(f"{'#'*60}\n")
    
    # Organize by strategy
    for strategy in strategies:
        print(f"\n{'='*60}")
        print(f"STRATEGY: {strategy.upper().replace('_', ' ')}")
        print(f"{'='*60}")
        print(f"{'Difficulty':<15} {'AI Wins':<10} {'Player Wins':<12} {'Ties':<8} {'AI Win %':<10}")
        print("-"*60)
        
        strategy_results = [r for r in all_results if r['strategy'] == strategy]
        for result in strategy_results:
            print(f"{result['difficulty']:<15} {result['ai_wins']:<10} {result['player_wins']:<12} {result['ties']:<8} {result['ai_win_rate']:>6.1f}%")
        
        print("="*60)
    
    print(f"\n{'='*60}")
    print("TEST COMPLETE!")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()

