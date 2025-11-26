"""
Parameterized AI Strategy Functions for Optimization

This module contains AI strategy functions that accept hyperparameters,
allowing for optimization through simulation.
"""

import random
from collections import Counter
from typing import List, Dict
from optimization.hyperparameters import VeryHardHyperparameters


def get_counter_move(predicted_move: str) -> str:
    """Get the move that beats the predicted move."""
    counter_moves = {
        'rock': 'paper',
        'paper': 'scissors',
        'scissors': 'rock'
    }
    return counter_moves[predicted_move]


def ai_very_hard_parameterized(history: List[Dict], params: VeryHardHyperparameters) -> str:
    """
    Very Hard AI with parameterized hyperparameters for optimization.
    
    This version is identical to ai_very_hard but accepts a params object
    instead of using hardcoded values.
    
    Args:
        history: List of game dictionaries
        params: Hyperparameters object
    
    Returns:
        Move choice: 'rock', 'paper', or 'scissors'
    """
    if not history or len(history) < 5:
        if len(history) < 2:
            return 'paper'  # Counter most common opening (rock)
        # For early game, use simple random
        return random.choice(['rock', 'paper', 'scissors'])
    
    # Initialize prediction ensemble
    predictions = []  # List of (move, confidence, source) tuples
    
    last_game = history[-1]
    player_choices = [game['player'] for game in history]
    
    # ============================================================
    # FEATURE 1: MARKOV CHAIN PREDICTION (2nd Order)
    # ============================================================
    if len(history) >= 10:
        transitions = {}
        for i in range(len(history) - 1):
            current = history[i]['player']
            next_move = history[i + 1]['player']
            
            if current not in transitions:
                transitions[current] = []
            transitions[current].append(next_move)
        
        if last_game['player'] in transitions:
            transition_counts = Counter(transitions[last_game['player']])
            total = len(transitions[last_game['player']])
            
            most_likely, count = transition_counts.most_common(1)[0]
            probability = count / total
            
            if probability >= params.markov_strong_threshold:
                confidence = params.markov_strong_base_confidence + \
                           (probability - params.markov_strong_threshold) * params.markov_strong_scaling
                predictions.append((get_counter_move(most_likely), confidence, 'markov'))
            elif probability >= params.markov_moderate_threshold:
                confidence = params.markov_moderate_base_confidence + \
                           (probability - params.markov_moderate_threshold) * params.markov_moderate_scaling
                predictions.append((get_counter_move(most_likely), confidence, 'markov'))
    
    # ============================================================
    # FEATURE 2: OPPONENT MODELING
    # ============================================================
    if len(history) >= 15:
        choice_counts = Counter(player_choices[-20:])
        total_recent = len(player_choices[-20:])
        
        if len(choice_counts) == 1:
            randomness_score = 0.0
        elif len(choice_counts) == 2:
            counts = sorted(choice_counts.values(), reverse=True)
            randomness_score = counts[1] / counts[0]
        else:
            expected = total_recent / 3
            variance = sum((count - expected) ** 2 for count in choice_counts.values()) / 3
            max_variance = (total_recent ** 2) / 3
            randomness_score = 1.0 - (variance / max_variance) if max_variance > 0 else 0.5
        
        if randomness_score < params.predictable_threshold:
            most_common = Counter(player_choices[-15:]).most_common(1)[0][0]
            predictions.append((get_counter_move(most_common), params.predictable_confidence, 'exploit_predictable'))
        elif randomness_score > params.random_threshold:
            predictions.append((random.choice(['rock', 'paper', 'scissors']), params.random_confidence, 'nash_equilibrium'))
    
    # ============================================================
    # FEATURE 3: COUNTER-COUNTER PREDICTION (Level-K Reasoning)
    # ============================================================
    if len(history) >= 12:
        recent_choices = player_choices[-12:]
        choice_counts = Counter(recent_choices)
        most_common_move, _ = choice_counts.most_common(1)[0]
        
        ai_would_counter = get_counter_move(most_common_move)
        counter_ai_counter = get_counter_move(ai_would_counter)
        
        counter_counter_count = recent_choices.count(counter_ai_counter)
        counter_counter_freq = counter_counter_count / len(recent_choices)
        
        if counter_counter_freq >= params.level_k_threshold:
            predictions.append((get_counter_move(counter_ai_counter), params.level_k_confidence, 'level_3_reasoning'))
        
        last_6 = recent_choices[-6:]
        if len(set(last_6)) == 3 and max(Counter(last_6).values()) == 2:
            predictions.append((random.choice(['rock', 'paper', 'scissors']), params.sophistication_confidence, 'counter_sophistication'))
    
    # ============================================================
    # FEATURE 4: ENHANCED PATTERN DETECTION
    # ============================================================
    
    # Strong Frequency Bias
    if len(history) >= 8:
        recent_choices = player_choices[-15:]
        choice_counts = Counter(recent_choices)
        most_common_move, count = choice_counts.most_common(1)[0]
        frequency = count / len(recent_choices)
        
        if frequency >= params.strong_frequency_threshold:
            predictions.append((get_counter_move(most_common_move), params.strong_frequency_confidence, 'strong_frequency'))
        elif frequency >= params.moderate_frequency_threshold:
            predictions.append((get_counter_move(most_common_move), params.moderate_frequency_confidence, 'moderate_frequency'))
        elif frequency >= params.weak_frequency_threshold:
            predictions.append((get_counter_move(most_common_move), params.weak_frequency_confidence, 'weak_frequency'))
    
    # Win-Stay Detection
    if last_game['result'] == 'player' and len(history) >= 6:
        win_stay_count = 0
        win_opportunities = 0
        
        for i in range(max(0, len(history) - 12), len(history) - 1):
            if history[i]['result'] == 'player':
                win_opportunities += 1
                if i + 1 < len(history) and history[i]['player'] == history[i + 1]['player']:
                    win_stay_count += 1
        
        if win_opportunities > 0:
            win_stay_rate = win_stay_count / win_opportunities
            if win_stay_rate >= params.win_stay_threshold:
                confidence = params.win_stay_base_confidence + \
                           (win_stay_rate - params.win_stay_threshold) * params.win_stay_confidence_scaling
                predictions.append((get_counter_move(last_game['player']), confidence, 'win_stay'))
    
    # Lose-Shift Detection
    if last_game['result'] == 'computer' and len(history) >= 6:
        lose_shift_count = 0
        lose_opportunities = 0
        
        for i in range(max(0, len(history) - 12), len(history) - 1):
            if history[i]['result'] == 'computer':
                lose_opportunities += 1
                if i + 1 < len(history) and history[i]['player'] != history[i + 1]['player']:
                    lose_shift_count += 1
        
        if lose_opportunities > 0:
            lose_shift_rate = lose_shift_count / lose_opportunities
            if lose_shift_rate >= params.lose_shift_threshold:
                sequence_shift = {
                    'rock': 'paper',
                    'paper': 'scissors',
                    'scissors': 'rock'
                }
                predicted_next = sequence_shift[last_game['player']]
                confidence = params.lose_shift_base_confidence + \
                           (lose_shift_rate - params.lose_shift_threshold) * params.lose_shift_confidence_scaling
                predictions.append((get_counter_move(predicted_next), confidence, 'lose_shift'))
    
    # Advanced Cycle Detection
    if len(history) >= 6:
        recent = player_choices[-9:]
        
        # Check for length-3 cycles
        if len(recent) >= 6:
            if recent[-6:-3] == recent[-3:]:
                next_in_cycle = recent[-2]
                predictions.append((get_counter_move(next_in_cycle), params.cycle_3_confidence, 'cycle_3'))
        
        # Check for length-2 cycles (alternating)
        if len(recent) >= 4:
            if recent[-4] == recent[-2] and recent[-3] == recent[-1]:
                next_in_pattern = recent[-2]
                predictions.append((get_counter_move(next_in_pattern), params.cycle_2_confidence, 'cycle_2'))
    
    # Anti-Triple Pattern
    if len(history) >= 2:
        if history[-2]['player'] == history[-1]['player']:
            repeated_move = history[-1]['player']
            likely_next = get_counter_move(repeated_move)
            predictions.append((get_counter_move(likely_next), params.anti_triple_confidence, 'anti_triple'))
    
    # ============================================================
    # ENSEMBLE VOTING SYSTEM
    # ============================================================
    if predictions:
        # Group predictions by move
        move_votes = {}
        for move, confidence, source in predictions:
            if move not in move_votes:
                move_votes[move] = []
            move_votes[move].append((confidence, source))
        
        # Calculate weighted scores
        move_scores = {}
        for move, votes in move_votes.items():
            total_confidence = sum(conf for conf, _ in votes)
            vote_count_bonus = len(votes) * params.vote_bonus_per_predictor
            move_scores[move] = total_confidence + vote_count_bonus
        
        # Select move with highest score
        best_move = max(move_scores, key=move_scores.get)
        best_score = move_scores[best_move]
        
        # Apply stochastic exploitation based on confidence
        if best_score >= params.exploitation_very_high_threshold:
            if random.random() < params.exploitation_very_high_rate:
                return best_move
        elif best_score >= params.exploitation_high_threshold:
            if random.random() < params.exploitation_high_rate:
                return best_move
        elif best_score >= params.exploitation_moderate_threshold:
            if random.random() < params.exploitation_moderate_rate:
                return best_move
        elif best_score >= params.exploitation_low_threshold:
            if random.random() < params.exploitation_low_rate:
                return best_move
    
    # Fallback: Random choice (Nash equilibrium)
    return random.choice(['rock', 'paper', 'scissors'])

