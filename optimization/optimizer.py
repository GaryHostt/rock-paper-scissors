"""
Optimization Framework for Hyperparameter Tuning

This module provides the optimization infrastructure to find optimal
hyperparameters for AI strategies through simulation-based evaluation.
"""

import random
import math
import copy
import json
from typing import List, Dict, Tuple, Callable, Any
from collections import defaultdict
import time

from optimization.hyperparameters import VeryHardHyperparameters
from optimization.opponent_agents import get_weighted_opponent_suite, OpponentAgent


class SimulationEngine:
    """
    Engine for running games between AI and opponent agents.
    """
    
    def __init__(self, ai_function: Callable):
        """
        Initialize simulation engine.
        
        Args:
            ai_function: AI strategy function that takes (history, params) and returns choice
        """
        self.ai_function = ai_function
        self.choices = ['rock', 'paper', 'scissors']
    
    def determine_winner(self, player_choice: str, computer_choice: str) -> str:
        """Determine winner of a round."""
        if player_choice == computer_choice:
            return 'tie'
        
        winning_combinations = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        
        if winning_combinations[player_choice] == computer_choice:
            return 'player'
        else:
            return 'computer'
    
    def run_game(self, opponent: OpponentAgent, params: VeryHardHyperparameters, 
                 num_rounds: int = 100) -> Dict[str, Any]:
        """
        Run a single game between AI and opponent.
        
        Args:
            opponent: Opponent agent
            params: Hyperparameters for AI
            num_rounds: Number of rounds to play
        
        Returns:
            Dict with game statistics
        """
        history = []
        opponent.reset()
        
        wins = 0
        losses = 0
        ties = 0
        
        for _ in range(num_rounds):
            # Opponent chooses
            player_choice = opponent.choose(history)
            
            # AI chooses using current hyperparameters
            computer_choice = self.ai_function(history, params)
            
            # Determine winner
            result = self.determine_winner(player_choice, computer_choice)
            
            # Update stats
            if result == 'computer':
                wins += 1
            elif result == 'player':
                losses += 1
            else:
                ties += 1
            
            # Update history
            history.append({
                'player': player_choice,
                'computer': computer_choice,
                'result': result
            })
        
        win_rate = wins / num_rounds if num_rounds > 0 else 0
        
        return {
            'wins': wins,
            'losses': losses,
            'ties': ties,
            'win_rate': win_rate,
            'opponent': opponent.name,
            'rounds': num_rounds
        }
    
    def run_tournament(self, params: VeryHardHyperparameters, 
                      rounds_per_opponent: int = 100,
                      verbose: bool = False) -> Dict[str, Any]:
        """
        Run a tournament against all opponents.
        
        Args:
            params: Hyperparameters for AI
            rounds_per_opponent: Rounds to play against each opponent
            verbose: Print progress
        
        Returns:
            Dict with tournament statistics
        """
        weighted_opponents = get_weighted_opponent_suite()
        results = []
        total_weight = sum(weight for _, weight in weighted_opponents)
        
        for opponent, weight in weighted_opponents:
            if verbose:
                print(f"  Playing vs {opponent.name}...", end='', flush=True)
            
            game_result = self.run_game(opponent, params, rounds_per_opponent)
            game_result['weight'] = weight
            results.append(game_result)
            
            if verbose:
                print(f" Win Rate: {game_result['win_rate']*100:.1f}%")
        
        # Calculate weighted average win rate
        weighted_win_rate = sum(
            r['win_rate'] * r['weight'] for r in results
        ) / total_weight
        
        # Calculate average against each category
        fixed_patterns = [r for r in results if 'Always' in r['opponent']]
        cycles = [r for r in results if 'Cycle' in r['opponent']]
        psychological = [r for r in results if 'Stay' in r['opponent']]
        frequency = [r for r in results if 'Frequency' in r['opponent']]
        complex_strategies = [r for r in results if r['opponent'] in ['Counter-AI', 'Mixed Strategy']]
        random_baseline = [r for r in results if r['opponent'] == 'Random']
        
        def avg_win_rate(results_list):
            return sum(r['win_rate'] for r in results_list) / len(results_list) if results_list else 0
        
        return {
            'weighted_win_rate': weighted_win_rate,
            'overall_win_rate': sum(r['win_rate'] for r in results) / len(results),
            'category_performance': {
                'fixed_patterns': avg_win_rate(fixed_patterns),
                'cycles': avg_win_rate(cycles),
                'psychological': avg_win_rate(psychological),
                'frequency_bias': avg_win_rate(frequency),
                'complex': avg_win_rate(complex_strategies),
                'random': avg_win_rate(random_baseline)
            },
            'detailed_results': results
        }


class FitnessEvaluator:
    """
    Evaluates fitness of hyperparameter configurations.
    """
    
    def __init__(self, ai_function: Callable, rounds_per_opponent: int = 100):
        """
        Initialize fitness evaluator.
        
        Args:
            ai_function: AI strategy function
            rounds_per_opponent: Number of rounds per opponent in tournaments
        """
        self.engine = SimulationEngine(ai_function)
        self.rounds_per_opponent = rounds_per_opponent
        self.evaluation_count = 0
    
    def evaluate(self, params: VeryHardHyperparameters, verbose: bool = False) -> float:
        """
        Evaluate fitness of hyperparameters.
        
        Higher fitness = better performance.
        
        Args:
            params: Hyperparameters to evaluate
            verbose: Print progress
        
        Returns:
            Fitness score (0-100, higher is better)
        """
        self.evaluation_count += 1
        
        if verbose:
            print(f"\nEvaluation #{self.evaluation_count}")
        
        results = self.engine.run_tournament(params, self.rounds_per_opponent, verbose)
        
        # Fitness is weighted win rate * 100
        # We want to maximize this
        fitness = results['weighted_win_rate'] * 100
        
        # Bonus for good performance against complex opponents
        complex_performance = results['category_performance']['complex']
        if complex_performance > 0.55:  # Above 55% against complex
            fitness += (complex_performance - 0.55) * 20  # Up to +9 bonus
        
        # Penalty if we're too weak against random (should be around 33%)
        random_performance = results['category_performance']['random']
        if random_performance < 0.28 or random_performance > 0.38:
            # We want to be ~33% (fair) against random
            fitness -= abs(random_performance - 0.33) * 30
        
        if verbose:
            print(f"  Weighted Win Rate: {results['weighted_win_rate']*100:.2f}%")
            print(f"  Fitness Score: {fitness:.2f}")
        
        return fitness


class RandomSearchOptimizer:
    """
    Random search optimization - samples random configurations.
    Fast and effective for finding good solutions.
    """
    
    def __init__(self, evaluator: FitnessEvaluator, params_template: VeryHardHyperparameters):
        """
        Initialize optimizer.
        
        Args:
            evaluator: Fitness evaluator
            params_template: Template with default values and bounds
        """
        self.evaluator = evaluator
        self.params_template = params_template
        self.bounds = params_template.get_optimization_bounds()
        self.best_params = None
        self.best_fitness = float('-inf')
        self.history = []
    
    def random_params(self) -> VeryHardHyperparameters:
        """Generate random hyperparameters within bounds."""
        params_dict = {}
        for param_name, (min_val, max_val) in self.bounds.items():
            # Random value in range
            params_dict[param_name] = random.uniform(min_val, max_val)
        
        return VeryHardHyperparameters.from_dict(params_dict)
    
    def optimize(self, iterations: int = 100, verbose: bool = True) -> Tuple[VeryHardHyperparameters, float]:
        """
        Run random search optimization.
        
        Args:
            iterations: Number of random samples to evaluate
            verbose: Print progress
        
        Returns:
            (best_params, best_fitness)
        """
        if verbose:
            print(f"Starting Random Search with {iterations} iterations...")
            print("=" * 70)
        
        start_time = time.time()
        
        for i in range(iterations):
            if verbose and i % 10 == 0:
                print(f"\nIteration {i+1}/{iterations}")
            
            # Generate random parameters
            params = self.random_params()
            
            # Evaluate fitness
            fitness = self.evaluator.evaluate(params, verbose=False)
            
            # Track history
            self.history.append((params, fitness))
            
            # Update best
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_params = params
                if verbose:
                    print(f"  ✓ New best fitness: {fitness:.2f}")
        
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"\n" + "=" * 70)
            print(f"Random Search Complete!")
            print(f"Time elapsed: {elapsed/60:.1f} minutes")
            print(f"Best fitness: {self.best_fitness:.2f}")
            print(f"Evaluations: {self.evaluator.evaluation_count}")
        
        return self.best_params, self.best_fitness


class SimulatedAnnealingOptimizer:
    """
    Simulated Annealing optimization - more efficient than random search.
    """
    
    def __init__(self, evaluator: FitnessEvaluator, params_template: VeryHardHyperparameters):
        """
        Initialize optimizer.
        
        Args:
            evaluator: Fitness evaluator
            params_template: Template with default values and bounds
        """
        self.evaluator = evaluator
        self.params_template = params_template
        self.bounds = params_template.get_optimization_bounds()
        self.best_params = None
        self.best_fitness = float('-inf')
        self.history = []
    
    def perturb_params(self, params: VeryHardHyperparameters, temperature: float) -> VeryHardHyperparameters:
        """
        Perturb hyperparameters (make small random changes).
        
        Args:
            params: Current parameters
            temperature: Controls perturbation size (0-1)
        
        Returns:
            Perturbed parameters
        """
        params_dict = params.to_dict()
        new_params_dict = {}
        
        for param_name, value in params_dict.items():
            if param_name in self.bounds:
                min_val, max_val = self.bounds[param_name]
                range_size = max_val - min_val
                
                # Perturbation size depends on temperature
                max_perturbation = range_size * 0.1 * temperature
                perturbation = random.uniform(-max_perturbation, max_perturbation)
                
                # Apply perturbation and clip to bounds
                new_value = value + perturbation
                new_value = max(min_val, min(max_val, new_value))
                new_params_dict[param_name] = new_value
            else:
                new_params_dict[param_name] = value
        
        return VeryHardHyperparameters.from_dict(new_params_dict)
    
    def acceptance_probability(self, current_fitness: float, new_fitness: float, temperature: float) -> float:
        """
        Calculate probability of accepting worse solution.
        
        Simulated annealing allows occasional acceptance of worse solutions
        to escape local optima.
        """
        if new_fitness > current_fitness:
            return 1.0  # Always accept better solutions
        
        # Accept worse solutions with probability that decreases with temperature
        return math.exp((new_fitness - current_fitness) / temperature)
    
    def optimize(self, iterations: int = 200, initial_temp: float = 10.0, 
                 cooling_rate: float = 0.95, verbose: bool = True) -> Tuple[VeryHardHyperparameters, float]:
        """
        Run simulated annealing optimization.
        
        Args:
            iterations: Number of iterations
            initial_temp: Starting temperature
            cooling_rate: Temperature reduction per iteration (0-1)
            verbose: Print progress
        
        Returns:
            (best_params, best_fitness)
        """
        if verbose:
            print(f"Starting Simulated Annealing with {iterations} iterations...")
            print(f"Initial temp: {initial_temp}, Cooling rate: {cooling_rate}")
            print("=" * 70)
        
        start_time = time.time()
        
        # Start with default parameters
        current_params = self.params_template
        current_fitness = self.evaluator.evaluate(current_params, verbose=False)
        
        self.best_params = current_params
        self.best_fitness = current_fitness
        
        temperature = initial_temp
        
        for i in range(iterations):
            if verbose and i % 20 == 0:
                print(f"\nIteration {i+1}/{iterations} (T={temperature:.2f})")
            
            # Generate neighbor solution
            new_params = self.perturb_params(current_params, temperature / initial_temp)
            
            # Evaluate new solution
            new_fitness = self.evaluator.evaluate(new_params, verbose=False)
            
            # Track history
            self.history.append((new_params, new_fitness))
            
            # Decide whether to accept new solution
            if random.random() < self.acceptance_probability(current_fitness, new_fitness, temperature):
                current_params = new_params
                current_fitness = new_fitness
                
                # Update best if necessary
                if new_fitness > self.best_fitness:
                    self.best_fitness = new_fitness
                    self.best_params = new_params
                    if verbose:
                        print(f"  ✓ New best fitness: {new_fitness:.2f}")
            
            # Cool down
            temperature *= cooling_rate
        
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"\n" + "=" * 70)
            print(f"Simulated Annealing Complete!")
            print(f"Time elapsed: {elapsed/60:.1f} minutes")
            print(f"Best fitness: {self.best_fitness:.2f}")
            print(f"Evaluations: {self.evaluator.evaluation_count}")
        
        return self.best_params, self.best_fitness


def save_optimization_results(params: VeryHardHyperparameters, fitness: float, 
                              method: str, filepath: str):
    """Save optimization results to file."""
    results = {
        'method': method,
        'fitness': fitness,
        'parameters': params.to_dict(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {filepath}")

