"""
AI vs AI Evaluation System for Rock Paper Scissors

This module tests different AI difficulties against each other to validate
proper difficulty scaling and comparative performance.

Directly imports and uses the AI functions from app.py for accurate testing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import ai_easy, ai_medium, ai_hard, ai_very_hard, determine_winner
import json
from datetime import datetime


class AIvsAIEvaluator:
    def __init__(self):
        self.results = {}
        self.ai_functions = {
            'easy': ai_easy,
            'medium': ai_medium,
            'hard': ai_hard,
            'veryhard': ai_very_hard
        }
    
    def get_ai_choice(self, difficulty, history):
        """
        Get AI's choice based on difficulty and history
        
        Args:
            difficulty: 'easy', 'medium', 'hard', or 'veryhard'
            history: List of previous games in format:
                     [{'player': choice, 'computer': choice, 'result': result}, ...]
        
        Returns:
            str: The AI's choice ('rock', 'paper', or 'scissors')
        """
        ai_func = self.ai_functions.get(difficulty)
        
        if difficulty == 'easy':
            return ai_func()
        else:
            return ai_func(history)
    
    def simulate_ai_vs_ai(self, player1_difficulty, player2_difficulty, num_games=1000, verbose=True):
        """
        Simulate games between two AI difficulties
        
        Player 1 (acts as 'player') vs Player 2 (acts as 'computer')
        
        Args:
            player1_difficulty: Difficulty for Player 1
            player2_difficulty: Difficulty for Player 2
            num_games: Number of games to play
            verbose: Print progress
        
        Returns:
            dict: Test results
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🤖 {player1_difficulty.upper()} vs {player2_difficulty.upper()}")
            print(f"{'='*70}")
        
        player1_wins = 0
        player2_wins = 0
        ties = 0
        
        # Separate history for each player (from their own perspective)
        player1_history = []  # P1 sees itself as 'player', P2 as 'computer'
        player2_history = []  # P2 sees itself as 'player', P1 as 'computer'
        
        for game_num in range(num_games):
            try:
                # Player 1 makes its choice
                p1_choice = self.get_ai_choice(player1_difficulty, player1_history)
                
                # Player 2 makes its choice
                p2_choice = self.get_ai_choice(player2_difficulty, player2_history)
                
                # Determine winner
                winner = determine_winner(p1_choice, p2_choice)
                
                # Update win counts
                if winner == 'player':  # Player 1 wins
                    player1_wins += 1
                    p1_result = 'player'
                    p2_result = 'computer'
                elif winner == 'computer':  # Player 2 wins
                    player2_wins += 1
                    p1_result = 'computer'
                    p2_result = 'player'
                else:  # Tie
                    ties += 1
                    p1_result = 'tie'
                    p2_result = 'tie'
                
                # Update histories from each player's perspective
                player1_history.append({
                    'player': p1_choice,
                    'computer': p2_choice,
                    'result': p1_result
                })
                
                player2_history.append({
                    'player': p2_choice,
                    'computer': p1_choice,
                    'result': p2_result
                })
                
                # Progress indicator
                if verbose and (game_num + 1) % 100 == 0:
                    p1_rate = player1_wins / (game_num + 1) * 100
                    p2_rate = player2_wins / (game_num + 1) * 100
                    print(f"  Game {game_num + 1}: {player1_difficulty.upper()} {p1_rate:.1f}% | {player2_difficulty.upper()} {p2_rate:.1f}%")
            
            except Exception as e:
                if verbose:
                    print(f"Error in game {game_num + 1}: {e}")
                continue
        
        total = player1_wins + player2_wins + ties
        
        result = {
            'player1': player1_difficulty,
            'player2': player2_difficulty,
            'player1_wins': player1_wins,
            'player2_wins': player2_wins,
            'ties': ties,
            'player1_win_rate': (player1_wins / total * 100) if total > 0 else 0,
            'player2_win_rate': (player2_wins / total * 100) if total > 0 else 0,
            'tie_rate': (ties / total * 100) if total > 0 else 0,
            'total_games': total
        }
        
        if verbose:
            print(f"\n📊 Results:")
            print(f"  {player1_difficulty.upper()} Wins:  {player1_wins:4d} ({result['player1_win_rate']:.1f}%)")
            print(f"  {player2_difficulty.upper()} Wins:  {player2_wins:4d} ({result['player2_win_rate']:.1f}%)")
            print(f"  Ties:          {ties:4d} ({result['tie_rate']:.1f}%)")
        
        return result
    
    def run_all_matchups(self, num_games=1000):
        """Run all possible AI vs AI matchups"""
        difficulties = ['easy', 'medium', 'hard', 'veryhard']
        
        print("\n" + "="*70)
        print("🤖 AI vs AI COMPREHENSIVE EVALUATION")
        print(f"Testing all AI difficulty matchups")
        print(f"Games per matchup: {num_games}")
        print("="*70)
        
        all_results = {}
        
        # Test each combination (including reverse matchups)
        for i, p1_diff in enumerate(difficulties):
            for j, p2_diff in enumerate(difficulties):
                if i == j:
                    # Skip same difficulty (or optionally test it)
                    continue
                
                key = f"{p1_diff}_vs_{p2_diff}"
                result = self.simulate_ai_vs_ai(p1_diff, p2_diff, num_games)
                all_results[key] = result
        
        # Generate report
        self.generate_report(all_results, difficulties)
        
        # Save results
        self.save_results(all_results)
        
        return all_results
    
    def generate_report(self, results, difficulties):
        """Generate comprehensive matchup report"""
        print("\n" + "="*70)
        print("📊 AI vs AI MATCHUP REPORT")
        print("="*70)
        
        print(f"\n{'Player 1':<12} {'vs':<4} {'Player 2':<12} {'P1 Win%':<10} {'P2 Win%':<10} {'Ties%':<10} {'Winner':<15}")
        print("-" * 70)
        
        for key, result in results.items():
            p1 = result['player1'].upper()
            p2 = result['player2'].upper()
            p1_rate = result['player1_win_rate']
            p2_rate = result['player2_win_rate']
            tie_rate = result['tie_rate']
            
            if p1_rate > p2_rate + 5:
                winner = f"✅ {p1}"
            elif p2_rate > p1_rate + 5:
                winner = f"✅ {p2}"
            else:
                winner = "⚖️ EVEN"
            
            print(f"{p1:<12} {'vs':<4} {p2:<12} {p1_rate:>7.1f}%  {p2_rate:>7.1f}%  {tie_rate:>7.1f}%  {winner:<15}")
        
        # Generate summary matrix
        print("\n" + "="*70)
        print("📈 WIN RATE MATRIX (Row vs Column)")
        print("="*70)
        
        # Create matrix
        print(f"\n{'':12}", end='')
        for diff in difficulties:
            print(f"{diff.upper():>12}", end='')
        print()
        print("-" * (12 + 12 * len(difficulties)))
        
        for p1 in difficulties:
            print(f"{p1.upper():<12}", end='')
            for p2 in difficulties:
                if p1 == p2:
                    print(f"{'---':>12}", end='')
                else:
                    key = f"{p1}_vs_{p2}"
                    if key in results:
                        rate = results[key]['player1_win_rate']
                        print(f"{rate:>11.1f}%", end='')
                    else:
                        print(f"{'N/A':>12}", end='')
            print()
        
        print("\n" + "="*70)
        print("📝 Expected Outcomes:")
        print("  - Higher difficulties should beat lower difficulties")
        print("  - Very Hard should beat all other difficulties (>50%)")
        print("  - Hard should beat Medium and Easy (>50%)")
        print("  - Medium should beat Easy (>50%)")
        print("  - Win rates should scale progressively with difficulty gap")
        print("="*70)
        
        # Validation checks
        print("\n" + "="*70)
        print("✅ VALIDATION CHECKS")
        print("="*70)
        
        checks_passed = 0
        checks_total = 0
        
        # Check: Very Hard should beat all others
        for lower in ['easy', 'medium', 'hard']:
            checks_total += 1
            key = f"veryhard_vs_{lower}"
            if key in results:
                rate = results[key]['player1_win_rate']
                if rate > 50:
                    print(f"✅ Very Hard beats {lower.upper()}: {rate:.1f}%")
                    checks_passed += 1
                else:
                    print(f"❌ Very Hard should beat {lower.upper()} but has {rate:.1f}% win rate")
        
        # Check: Hard should beat Medium and Easy
        for lower in ['easy', 'medium']:
            checks_total += 1
            key = f"hard_vs_{lower}"
            if key in results:
                rate = results[key]['player1_win_rate']
                if rate > 50:
                    print(f"✅ Hard beats {lower.upper()}: {rate:.1f}%")
                    checks_passed += 1
                else:
                    print(f"❌ Hard should beat {lower.upper()} but has {rate:.1f}% win rate")
        
        # Check: Medium should beat Easy
        checks_total += 1
        key = "medium_vs_easy"
        if key in results:
            rate = results[key]['player1_win_rate']
            if rate > 50:
                print(f"✅ Medium beats EASY: {rate:.1f}%")
                checks_passed += 1
            else:
                print(f"❌ Medium should beat EASY but has {rate:.1f}% win rate")
        
        print(f"\n{'='*70}")
        print(f"Validation: {checks_passed}/{checks_total} checks passed")
        if checks_passed == checks_total:
            print("✅ ALL CHECKS PASSED - Difficulty scaling is working correctly!")
        else:
            print(f"⚠️ {checks_total - checks_passed} checks failed - Review difficulty balance")
        print("="*70)
    
    def save_results(self, results):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_vs_ai_evaluation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'results': results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")


if __name__ == "__main__":
    import sys
    
    evaluator = AIvsAIEvaluator()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        evaluator.run_all_matchups(num_games=num_games)
    else:
        print("AI vs AI Performance Evaluation System")
        print("="*70)
        print("\nUsage:")
        print("  python ai_vs_ai_evaluator.py --full [N]    # Run all matchups (default 1000 games)")
        print("\nExamples:")
        print("  python ai_vs_ai_evaluator.py --full")
        print("  python ai_vs_ai_evaluator.py --full 2000")
        print("\nThis will test all AI difficulties against each other:")
        print("  - Easy vs Medium, Easy vs Hard, Easy vs Very Hard")
        print("  - Medium vs Easy, Medium vs Hard, Medium vs Very Hard")
        print("  - Hard vs Easy, Hard vs Medium, Hard vs Very Hard")
        print("  - Very Hard vs Easy, Very Hard vs Medium, Very Hard vs Hard")
        print("\nTotal: 12 matchups")
