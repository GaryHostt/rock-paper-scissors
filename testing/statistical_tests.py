"""
Statistical Analysis Tools for AI Evaluation

Provides statistical tests and confidence intervals for evaluating AI performance.
"""

import scipy.stats as stats
import numpy as np
from collections import Counter


def chi_square_randomness_test(choices, alpha=0.05):
    """
    Test if AI choices are truly random using Chi-Square test
    
    Args:
        choices: List of AI choices ('rock', 'paper', 'scissors')
        alpha: Significance level (default 0.05)
    
    Returns:
        dict: Test results including chi2, p_value, and conclusion
    """
    counts = Counter(choices)
    observed = [counts['rock'], counts['paper'], counts['scissors']]
    expected = [len(choices) / 3] * 3
    
    chi2, p_value = stats.chisquare(observed, expected)
    
    result = {
        'chi2': chi2,
        'p_value': p_value,
        'is_random': p_value > alpha,
        'observed': dict(counts),
        'expected_each': len(choices) / 3
    }
    
    print(f"\n🔬 Chi-Square Randomness Test")
    print(f"{'='*50}")
    print(f"Observed: Rock={counts['rock']}, Paper={counts['paper']}, Scissors={counts['scissors']}")
    print(f"Expected each: {len(choices)/3:.1f}")
    print(f"Chi-Square Statistic: χ² = {chi2:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Significance level: α = {alpha}")
    
    if p_value > alpha:
        print(f"✅ RANDOM: Cannot reject null hypothesis (p > α)")
        print(f"   The AI appears to be playing randomly")
    else:
        print(f"❌ NOT RANDOM: Reject null hypothesis (p ≤ α)")
        print(f"   The AI shows non-random patterns")
    
    return result


def win_rate_confidence_interval(wins, total, confidence=0.95):
    """
    Calculate confidence interval for win rate using Wilson score interval
    
    Args:
        wins: Number of wins
        total: Total games
        confidence: Confidence level (default 0.95)
    
    Returns:
        dict: Lower and upper bounds of confidence interval
    """
    if total == 0:
        return {'lower': 0, 'upper': 0, 'point_estimate': 0}
    
    p_hat = wins / total
    z = stats.norm.ppf((1 + confidence) / 2)
    
    # Wilson score interval (more accurate for proportions)
    denominator = 1 + z**2 / total
    center = (p_hat + z**2 / (2 * total)) / denominator
    margin = z * np.sqrt(p_hat * (1 - p_hat) / total + z**2 / (4 * total**2)) / denominator
    
    lower = max(0, (center - margin) * 100)
    upper = min(100, (center + margin) * 100)
    point = p_hat * 100
    
    print(f"\n📊 Win Rate Confidence Interval")
    print(f"{'='*50}")
    print(f"Wins: {wins}/{total}")
    print(f"Point Estimate: {point:.2f}%")
    print(f"{confidence*100:.0f}% Confidence Interval: [{lower:.2f}%, {upper:.2f}%]")
    print(f"Margin of Error: ±{(upper-lower)/2:.2f}%")
    
    return {
        'lower': lower,
        'upper': upper,
        'point_estimate': point,
        'margin_of_error': (upper - lower) / 2
    }


def pattern_exploitation_rate(history):
    """
    Calculate how often AI successfully exploits Win-Stay, Lose-Shift pattern
    
    Args:
        history: List of game dictionaries with 'agent_choice', 'opponent_choice', 'result'
    
    Returns:
        dict: Exploitation statistics
    """
    if len(history) < 2:
        return None
    
    win_stay_attempts = 0
    win_stay_exploits = 0
    lose_shift_attempts = 0
    lose_shift_exploits = 0
    
    counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
    shifts = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
    
    for i in range(1, len(history)):
        prev_game = history[i-1]
        current_game = history[i]
        
        # Win-Stay: Did agent win, then repeat?
        if prev_game['result'] == 'agent_win':
            win_stay_attempts += 1
            if current_game['agent_choice'] == prev_game['agent_choice']:
                # Agent repeated - did AI counter it?
                if current_game['opponent_choice'] == counters[prev_game['agent_choice']]:
                    win_stay_exploits += 1
        
        # Lose-Shift: Did agent lose, then shift?
        if prev_game['result'] == 'opponent_win':
            lose_shift_attempts += 1
            expected_shift = shifts[prev_game['agent_choice']]
            if current_game['agent_choice'] == expected_shift:
                # Agent shifted - did AI counter it?
                if current_game['opponent_choice'] == counters[expected_shift]:
                    lose_shift_exploits += 1
    
    win_stay_rate = (win_stay_exploits / win_stay_attempts * 100) if win_stay_attempts > 0 else 0
    lose_shift_rate = (lose_shift_exploits / lose_shift_attempts * 100) if lose_shift_attempts > 0 else 0
    
    print(f"\n🎯 Pattern Exploitation Analysis")
    print(f"{'='*50}")
    print(f"Win-Stay Pattern:")
    print(f"  Opportunities: {win_stay_attempts}")
    print(f"  Exploited: {win_stay_exploits}")
    print(f"  Rate: {win_stay_rate:.1f}%")
    print(f"\nLose-Shift Pattern:")
    print(f"  Opportunities: {lose_shift_attempts}")
    print(f"  Exploited: {lose_shift_exploits}")
    print(f"  Rate: {lose_shift_rate:.1f}%")
    
    return {
        'win_stay': {
            'attempts': win_stay_attempts,
            'exploits': win_stay_exploits,
            'rate': win_stay_rate
        },
        'lose_shift': {
            'attempts': lose_shift_attempts,
            'exploits': lose_shift_exploits,
            'rate': lose_shift_rate
        }
    }


def entropy_analysis(choices):
    """
    Calculate Shannon entropy of AI choices
    
    Args:
        choices: List of choices
    
    Returns:
        dict: Entropy and interpretation
    """
    if not choices:
        return None
    
    counts = Counter(choices)
    total = len(choices)
    probs = [count / total for count in counts.values()]
    
    # Shannon entropy
    entropy = -sum(p * np.log2(p) for p in probs if p > 0)
    max_entropy = np.log2(3)  # Maximum entropy for 3 choices
    normalized_entropy = entropy / max_entropy
    
    print(f"\n🔢 Entropy Analysis")
    print(f"{'='*50}")
    print(f"Shannon Entropy: {entropy:.4f} bits")
    print(f"Maximum Entropy: {max_entropy:.4f} bits")
    print(f"Normalized: {normalized_entropy:.2%}")
    
    if normalized_entropy > 0.95:
        interpretation = "Very random (near-perfect entropy)"
    elif normalized_entropy > 0.85:
        interpretation = "Mostly random (good entropy)"
    elif normalized_entropy > 0.70:
        interpretation = "Somewhat predictable (moderate entropy)"
    else:
        interpretation = "Highly predictable (low entropy)"
    
    print(f"Interpretation: {interpretation}")
    
    return {
        'entropy': entropy,
        'max_entropy': max_entropy,
        'normalized': normalized_entropy,
        'interpretation': interpretation
    }


def compare_two_ais(results_a, results_b, name_a='AI A', name_b='AI B'):
    """
    Compare two AI implementations statistically
    
    Args:
        results_a: Results dict from AI A
        results_b: Results dict from AI B
        name_a: Name of AI A
        name_b: Name of AI B
    
    Returns:
        dict: Comparison results
    """
    win_rate_a = results_a['loss_rate']  # AI's win rate
    win_rate_b = results_b['loss_rate']
    
    total_a = results_a['total_games']
    total_b = results_b['total_games']
    
    wins_a = int(win_rate_a * total_a / 100)
    wins_b = int(win_rate_b * total_b / 100)
    
    # Two-sample proportion z-test
    p1 = wins_a / total_a
    p2 = wins_b / total_b
    
    p_pooled = (wins_a + wins_b) / (total_a + total_b)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/total_a + 1/total_b))
    
    z_stat = (p1 - p2) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    print(f"\n⚖️  AI Comparison: {name_a} vs {name_b}")
    print(f"{'='*50}")
    print(f"{name_a}: {win_rate_a:.2f}% win rate ({total_a} games)")
    print(f"{name_b}: {win_rate_b:.2f}% win rate ({total_b} games)")
    print(f"Difference: {abs(win_rate_a - win_rate_b):.2f}%")
    print(f"Z-statistic: {z_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        better = name_a if win_rate_a > win_rate_b else name_b
        print(f"✅ SIGNIFICANT: {better} performs significantly better (p < 0.05)")
    else:
        print(f"❌ NOT SIGNIFICANT: No significant difference (p ≥ 0.05)")
    
    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'better_ai': name_a if win_rate_a > win_rate_b else name_b if win_rate_a < win_rate_b else 'tie'
    }


if __name__ == "__main__":
    # Example usage
    print("Statistical Analysis Tools for AI Evaluation")
    print("="*60)
    print("\nThis module provides statistical tests for:")
    print("  • Chi-square randomness test")
    print("  • Confidence intervals for win rates")
    print("  • Pattern exploitation rate analysis")
    print("  • Entropy analysis")
    print("  • AI comparison tests")
    print("\nImport this module in ai_evaluator.py or use standalone.")

