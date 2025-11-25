"""
AI Performance Evaluation System for Rock Paper Scissors

This module provides comprehensive testing and evaluation of AI difficulty levels.
Tests AI performance against various player strategies to ensure proper difficulty scaling.
"""

import requests
import random
from collections import defaultdict, Counter
import statistics
import json
from datetime import datetime


class AIEvaluator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = defaultdict(lambda: {
            'wins': 0, 'losses': 0, 'ties': 0,
            'games': []
        })
        self.current_history = []
    
    def simulate_player(self, strategy='random'):
        """
        Simulate different player strategies
        
        Args:
            strategy: One of 'random', 'always_rock', 'cycle', 'win_stay_lose_shift',
                     'double_throw', 'anti_ai'
        
        Returns:
            Choice: 'rock', 'paper', or 'scissors'
        """
        choices = ['rock', 'paper', 'scissors']
        
        if strategy == 'random':
            return random.choice(choices)
        
        elif strategy == 'always_rock':
            return 'rock'
        
        elif strategy == 'always_paper':
            return 'paper'
        
        elif strategy == 'always_scissors':
            return 'scissors'
        
        elif strategy == 'cycle':
            # Rock -> Paper -> Scissors -> repeat
            if not self.current_history:
                return 'rock'
            return choices[len(self.current_history) % 3]
        
        elif strategy == 'win_stay_lose_shift':
            if not self.current_history:
                return random.choice(choices)
            last = self.current_history[-1]
            if last['result'] == 'agent_win':
                return last['agent_choice']  # Stay
            else:
                # Shift to next
                shifts = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                return shifts[last['agent_choice']]
        
        elif strategy == 'double_throw':
            # Play same move twice, then switch
            if len(self.current_history) < 2:
                return 'rock'
            last_two = [g['agent_choice'] for g in self.current_history[-2:]]
            if last_two[0] == last_two[1]:
                # Switch to next
                shifts = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                return shifts[last_two[1]]
            else:
                return last_two[-1]
        
        elif strategy == 'anti_ai':
            # Try to counter AI patterns
            if len(self.current_history) < 3:
                return random.choice(choices)
            # Find AI's most common choice
            ai_choices = [g['opponent_choice'] for g in self.current_history[-10:]]
            most_common = Counter(ai_choices).most_common(1)[0][0]
            counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            return counters[most_common]
        
        return random.choice(choices)
    
    def run_test_suite(self, difficulty, num_games=1000, strategy='random', verbose=True):
        """
        Run a test suite against a specific difficulty
        
        Args:
            difficulty: 'easy', 'medium', 'hard', or 'veryhard'
            num_games: Number of games to play
            strategy: Player strategy to simulate
            verbose: Print progress and results
        
        Returns:
            dict: Test results including wins, losses, ties, win_rate
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Testing {difficulty.upper()} difficulty")
            print(f"Strategy: {strategy}, Games: {num_games}")
            print(f"{'='*60}")
        
        self.current_history = []
        wins = 0
        losses = 0
        ties = 0
        
        for game_num in range(num_games):
            # Agent chooses based on strategy
            agent_choice = self.simulate_player(strategy)
            
            # Play against AI
            try:
                response = requests.post(
                    f"{self.base_url}/mcp/play",
                    json={
                        'agent_id': f'evaluator_{strategy}',
                        'choice': agent_choice,
                        'opponent_difficulty': difficulty,
                        'session_history': self.current_history
                    },
                    timeout=5
                )
                
                if response.status_code != 200:
                    print(f"Error: HTTP {response.status_code}")
                    continue
                
                result = response.json()
                
                # Track results
                if result['result'] == 'agent_win':
                    wins += 1
                elif result['result'] == 'opponent_win':
                    losses += 1
                else:
                    ties += 1
                
                # Add to history
                self.current_history.append({
                    'agent_choice': result['agent_choice'],
                    'opponent_choice': result['opponent_choice'],
                    'result': result['result']
                })
                
                # Progress indicator
                if verbose and (game_num + 1) % 100 == 0:
                    current_win_rate = wins / (game_num + 1) * 100
                    current_loss_rate = losses / (game_num + 1) * 100
                    print(f"  Game {game_num + 1}: Win Rate = {current_win_rate:.1f}% | Loss Rate = {current_loss_rate:.1f}%")
            
            except Exception as e:
                print(f"Error in game {game_num + 1}: {e}")
                continue
        
        # Calculate statistics
        total = wins + losses + ties
        if total == 0:
            print("Error: No games completed")
            return None
        
        win_rate = (wins / total * 100)
        loss_rate = (losses / total * 100)
        tie_rate = (ties / total * 100)
        
        # Store results
        test_result = {
            'wins': wins,
            'losses': losses,
            'ties': ties,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'tie_rate': tie_rate,
            'total_games': total
        }
        
        # Print results
        if verbose:
            print(f"\n📊 Results:")
            print(f"  Agent Wins:    {wins:4d} ({win_rate:.1f}%)")
            print(f"  Agent Losses:  {losses:4d} ({loss_rate:.1f}%)")
            print(f"  Ties:          {ties:4d} ({tie_rate:.1f}%)")
            print(f"\n  AI Win Rate: {loss_rate:.1f}%")
        
        return test_result
    
    def run_comprehensive_test(self, num_games=1000):
        """
        Run all tests across all difficulties and strategies
        
        Args:
            num_games: Number of games per test
        
        Returns:
            dict: All test results
        """
        difficulties = ['easy', 'medium', 'hard', 'veryhard']
        strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
        
        all_results = {}
        
        print("\n" + "="*80)
        print("🧪 COMPREHENSIVE AI EVALUATION")
        print(f"Running {len(difficulties) * len(strategies)} tests with {num_games} games each")
        print("="*80)
        
        for difficulty in difficulties:
            for strategy in strategies:
                key = f"{difficulty}_{strategy}"
                result = self.run_test_suite(
                    difficulty, 
                    num_games=num_games, 
                    strategy=strategy,
                    verbose=True
                )
                if result:
                    all_results[key] = result
        
        # Generate report
        self.generate_report(all_results)
        
        # Save results to file
        self.save_results(all_results)
        
        return all_results
    
    def generate_report(self, results):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("📈 COMPREHENSIVE AI EVALUATION REPORT")
        print("="*80)
        
        difficulties = ['easy', 'medium', 'hard', 'veryhard']
        strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
        
        # Expected AI win rates against different strategies
        expected_rates = {
            'easy': {'random': 33, 'always_rock': 33, 'cycle': 33, 'win_stay_lose_shift': 33, 'anti_ai': 33},
            'medium': {'random': 33, 'always_rock': 60, 'cycle': 50, 'win_stay_lose_shift': 50, 'anti_ai': 40},
            'hard': {'random': 33, 'always_rock': 70, 'cycle': 60, 'win_stay_lose_shift': 65, 'anti_ai': 50},
            'veryhard': {'random': 33, 'always_rock': 75, 'cycle': 70, 'win_stay_lose_shift': 75, 'anti_ai': 60}
        }
        
        # Table header
        print(f"\n{'Difficulty':<12} {'Strategy':<22} {'AI Win %':<10} {'Expected':<10} {'Diff':<8} {'Status':<10}")
        print("-" * 80)
        
        for difficulty in difficulties:
            for strategy in strategies:
                key = f"{difficulty}_{strategy}"
                if key in results:
                    ai_win_rate = results[key].get('loss_rate', 0)
                    expected = expected_rates[difficulty][strategy]
                    diff = ai_win_rate - expected
                    
                    # Status: within 10% of expected is PASS
                    if abs(diff) <= 10:
                        status = "✅ PASS"
                    elif abs(diff) <= 15:
                        status = "⚠️ CHECK"
                    else:
                        status = "❌ FAIL"
                    
                    print(f"{difficulty:<12} {strategy:<22} {ai_win_rate:>6.1f}%   {expected:>5}%    {diff:>+6.1f}%  {status}")
        
        print("\n" + "="*80)
        print("📝 Analysis Guidelines:")
        print("  ✅ PASS:  AI performance within 10% of expected")
        print("  ⚠️  CHECK: AI performance 10-15% off expected (needs review)")
        print("  ❌ FAIL:  AI performance >15% off expected (needs fixing)")
        print("\n  - Easy should win ~33% against all strategies (pure random)")
        print("  - Medium should exploit predictable patterns (40-60%)")
        print("  - Hard should strongly exploit patterns (50-70%)")
        print("  - Very Hard should dominate predictable play (60-75%)")
        print("  - All AIs should win ~33% against true random (Nash equilibrium)")
        print("="*80)
    
    def save_results(self, results):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_evaluation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'results': results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")


def quick_test():
    """Quick test against all difficulties with random strategy"""
    evaluator = AIEvaluator()
    
    print("🎯 QUICK TEST - Random Strategy vs All Difficulties")
    print("This should show ~33% AI win rate for all difficulties\n")
    
    for difficulty in ['easy', 'medium', 'hard', 'veryhard']:
        evaluator.run_test_suite(difficulty, num_games=100, strategy='random')


def pattern_test():
    """Test AI ability to exploit patterns"""
    evaluator = AIEvaluator()
    
    print("🎯 PATTERN EXPLOITATION TEST")
    print("Testing if AIs can exploit predictable player strategies\n")
    
    # Test against always_rock (should be easy to exploit)
    evaluator.run_test_suite('easy', num_games=100, strategy='always_rock')
    evaluator.run_test_suite('medium', num_games=100, strategy='always_rock')
    evaluator.run_test_suite('hard', num_games=100, strategy='always_rock')
    evaluator.run_test_suite('veryhard', num_games=100, strategy='always_rock')


if __name__ == "__main__":
    import sys
    
    evaluator = AIEvaluator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--quick':
            quick_test()
        elif command == '--pattern':
            pattern_test()
        elif command == '--full':
            num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
            evaluator.run_comprehensive_test(num_games=num_games)
        else:
            print("Usage:")
            print("  python ai_evaluator.py --quick       # Quick test (100 games per difficulty)")
            print("  python ai_evaluator.py --pattern     # Pattern exploitation test")
            print("  python ai_evaluator.py --full [N]    # Full test suite (N games per test)")
    else:
        print("AI Performance Evaluation System")
        print("="*60)
        print("\nUsage:")
        print("  python ai_evaluator.py --quick       # Quick test (100 games)")
        print("  python ai_evaluator.py --pattern     # Test pattern exploitation")
        print("  python ai_evaluator.py --full [N]    # Full test (default 1000 games)")
        print("\nExamples:")
        print("  python ai_evaluator.py --quick")
        print("  python ai_evaluator.py --full 500")
        print("\nRunning quick test...\n")
        quick_test()

