#!/usr/bin/env python3
"""
Hyperparameter Optimization Runner

This script runs hyperparameter optimization for the ai_very_hard strategy.
It evaluates different hyperparameter configurations against a suite of
simulated opponents to find the optimal settings.

Usage:
    python run_optimization.py [--method METHOD] [--iterations N] [--rounds N]

Methods:
    random      - Random search (faster, good results)
    annealing   - Simulated annealing (slower, better results)
    both        - Run both methods and compare

Example:
    python run_optimization.py --method annealing --iterations 100 --rounds 100
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.hyperparameters import VeryHardHyperparameters, DEFAULT_VERY_HARD_PARAMS
from optimization.ai_strategies import ai_very_hard_parameterized
from optimization.optimizer import (
    FitnessEvaluator,
    RandomSearchOptimizer,
    SimulatedAnnealingOptimizer,
    save_optimization_results
)


def run_baseline_evaluation():
    """Evaluate baseline (current default parameters)."""
    print("\n" + "=" * 70)
    print("BASELINE EVALUATION - Current Default Parameters")
    print("=" * 70)
    
    evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=100)
    baseline_params = DEFAULT_VERY_HARD_PARAMS
    baseline_fitness = evaluator.evaluate(baseline_params, verbose=True)
    
    print(f"\nBaseline Fitness: {baseline_fitness:.2f}")
    return baseline_fitness


def run_random_search(iterations=50, rounds_per_opponent=100):
    """Run random search optimization."""
    print("\n" + "=" * 70)
    print("RANDOM SEARCH OPTIMIZATION")
    print("=" * 70)
    
    evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=rounds_per_opponent)
    optimizer = RandomSearchOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
    
    best_params, best_fitness = optimizer.optimize(iterations=iterations, verbose=True)
    
    # Save results
    save_optimization_results(
        best_params, 
        best_fitness, 
        'random_search',
        'optimization/results/random_search_best.json'
    )
    
    return best_params, best_fitness


def run_simulated_annealing(iterations=100, rounds_per_opponent=100):
    """Run simulated annealing optimization."""
    print("\n" + "=" * 70)
    print("SIMULATED ANNEALING OPTIMIZATION")
    print("=" * 70)
    
    evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=rounds_per_opponent)
    optimizer = SimulatedAnnealingOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
    
    best_params, best_fitness = optimizer.optimize(
        iterations=iterations,
        initial_temp=10.0,
        cooling_rate=0.95,
        verbose=True
    )
    
    # Save results
    save_optimization_results(
        best_params,
        best_fitness,
        'simulated_annealing',
        'optimization/results/simulated_annealing_best.json'
    )
    
    return best_params, best_fitness


def main():
    parser = argparse.ArgumentParser(
        description='Run hyperparameter optimization for RPS AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test with random search
  python run_optimization.py --method random --iterations 20 --rounds 50
  
  # Full optimization with simulated annealing
  python run_optimization.py --method annealing --iterations 200 --rounds 100
  
  # Compare both methods
  python run_optimization.py --method both --iterations 50 --rounds 100
        """
    )
    
    parser.add_argument('--method', 
                       choices=['random', 'annealing', 'both'], 
                       default='random',
                       help='Optimization method to use (default: random)')
    
    parser.add_argument('--iterations', 
                       type=int, 
                       default=50,
                       help='Number of optimization iterations (default: 50)')
    
    parser.add_argument('--rounds', 
                       type=int, 
                       default=100,
                       help='Rounds per opponent in fitness evaluation (default: 100)')
    
    parser.add_argument('--skip-baseline',
                       action='store_true',
                       help='Skip baseline evaluation')
    
    args = parser.parse_args()
    
    # Create results directory
    os.makedirs('optimization/results', exist_ok=True)
    
    print("\n" + "=" * 70)
    print("RPS AI HYPERPARAMETER OPTIMIZATION")
    print("=" * 70)
    print(f"Method: {args.method}")
    print(f"Iterations: {args.iterations}")
    print(f"Rounds per opponent: {args.rounds}")
    print("=" * 70)
    
    # Evaluate baseline
    baseline_fitness = None
    if not args.skip_baseline:
        baseline_fitness = run_baseline_evaluation()
    
    results = {}
    
    # Run optimization
    if args.method == 'random' or args.method == 'both':
        params, fitness = run_random_search(args.iterations, args.rounds)
        results['random_search'] = (params, fitness)
        
        if baseline_fitness:
            improvement = fitness - baseline_fitness
            print(f"\n✓ Random Search Improvement: {improvement:+.2f} ({improvement/baseline_fitness*100:+.1f}%)")
    
    if args.method == 'annealing' or args.method == 'both':
        params, fitness = run_simulated_annealing(args.iterations, args.rounds)
        results['simulated_annealing'] = (params, fitness)
        
        if baseline_fitness:
            improvement = fitness - baseline_fitness
            print(f"\n✓ Simulated Annealing Improvement: {improvement:+.2f} ({improvement/baseline_fitness*100:+.1f}%)")
    
    # Summary
    print("\n" + "=" * 70)
    print("OPTIMIZATION COMPLETE")
    print("=" * 70)
    
    if baseline_fitness:
        print(f"Baseline Fitness: {baseline_fitness:.2f}")
    
    for method_name, (params, fitness) in results.items():
        print(f"\n{method_name.upper()}:")
        print(f"  Best Fitness: {fitness:.2f}")
        if baseline_fitness:
            improvement = fitness - baseline_fitness
            print(f"  Improvement: {improvement:+.2f} ({improvement/baseline_fitness*100:+.1f}%)")
    
    if len(results) > 1:
        best_method = max(results.items(), key=lambda x: x[1][1])
        print(f"\n✓ Best Method: {best_method[0]} (fitness: {best_method[1][1]:.2f})")
        print(f"\nOptimized parameters saved to optimization/results/")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()

