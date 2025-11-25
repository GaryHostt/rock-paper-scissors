"""
Visualization Tools for AI Performance Analysis

Generates charts and graphs for AI evaluation results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
import numpy as np
from pathlib import Path


def load_results(filename):
    """Load results from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['results']


def plot_win_rate_comparison(results, output_file='win_rate_comparison.png'):
    """
    Plot win rates across all difficulties and strategies
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    difficulties = ['easy', 'medium', 'hard', 'veryhard']
    strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
    
    # Prepare data
    data = []
    labels = []
    colors = []
    
    color_map = {
        'easy': '#10b981',
        'medium': '#f59e0b',
        'hard': '#ef4444',
        'veryhard': '#8b5cf6'
    }
    
    for difficulty in difficulties:
        for strategy in strategies:
            key = f"{difficulty}_{strategy}"
            if key in results:
                ai_win_rate = results[key]['loss_rate']
                data.append(ai_win_rate)
                labels.append(f"{difficulty}\n{strategy}")
                colors.append(color_map[difficulty])
    
    # Create bar chart
    x = np.arange(len(data))
    bars = ax.bar(x, data, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add Nash equilibrium line
    ax.axhline(y=33.3, color='blue', linestyle='--', linewidth=2, label='Nash Equilibrium (33.3%)')
    
    # Formatting
    ax.set_ylabel('AI Win Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('AI Performance Across Difficulties and Strategies', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📊 Chart saved to: {output_file}")


def plot_heatmap(results, output_file='performance_heatmap.png'):
    """
    Create heatmap of AI performance
    """
    difficulties = ['easy', 'medium', 'hard', 'veryhard']
    strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
    
    # Create matrix
    matrix = np.zeros((len(difficulties), len(strategies)))
    
    for i, difficulty in enumerate(difficulties):
        for j, strategy in enumerate(strategies):
            key = f"{difficulty}_{strategy}"
            if key in results:
                matrix[i, j] = results[key]['loss_rate']
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matrix, annot=True, fmt='.1f', cmap='RdYlGn', 
                xticklabels=strategies, yticklabels=difficulties,
                vmin=0, vmax=100, cbar_kws={'label': 'AI Win Rate (%)'})
    
    ax.set_title('AI Win Rate Heatmap', fontsize=14, fontweight='bold')
    ax.set_xlabel('Player Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('AI Difficulty', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📊 Heatmap saved to: {output_file}")


def plot_difficulty_progression(results, output_file='difficulty_progression.png'):
    """
    Show how AI win rate progresses with difficulty for each strategy
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    difficulties = ['easy', 'medium', 'hard', 'veryhard']
    strategies = ['random', 'always_rock', 'cycle', 'win_stay_lose_shift', 'anti_ai']
    
    markers = ['o', 's', '^', 'D', 'v']
    
    for idx, strategy in enumerate(strategies):
        win_rates = []
        for difficulty in difficulties:
            key = f"{difficulty}_{strategy}"
            if key in results:
                win_rates.append(results[key]['loss_rate'])
            else:
                win_rates.append(None)
        
        ax.plot(difficulties, win_rates, marker=markers[idx], linewidth=2,
                markersize=8, label=strategy, alpha=0.8)
    
    ax.axhline(y=33.3, color='gray', linestyle='--', alpha=0.5, label='Nash Equilibrium')
    ax.set_ylabel('AI Win Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Difficulty Level', fontsize=12, fontweight='bold')
    ax.set_title('AI Performance Progression by Difficulty', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📊 Progression chart saved to: {output_file}")


def generate_report(results_file):
    """Generate all visualizations from results file"""
    results = load_results(results_file)
    
    print(f"\n📊 Generating visualizations from {results_file}\n")
    
    plot_win_rate_comparison(results)
    plot_heatmap(results)
    plot_difficulty_progression(results)
    
    print("\n✅ All visualizations generated successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
        if Path(results_file).exists():
            generate_report(results_file)
        else:
            print(f"Error: File '{results_file}' not found")
            sys.exit(1)
    else:
        print("Visualization Tools for AI Evaluation")
        print("="*60)
        print("\nUsage:")
        print("  python visualization.py <results_file.json>")
        print("\nExample:")
        print("  python visualization.py ai_evaluation_20250124_120000.json")
        print("\nThis will generate:")
        print("  • win_rate_comparison.png - Bar chart of all results")
        print("  • performance_heatmap.png - Heatmap of win rates")
        print("  • difficulty_progression.png - Line chart of progression")

