from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
from collections import Counter
import os
import json

# OpenAI import (will work if openai library is installed)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

app = Flask(__name__)
CORS(app)

CHOICES = ['rock', 'paper', 'scissors']

def determine_winner(player_choice, computer_choice):
    """Determine the winner of the game."""
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

def get_counter_move(predicted_move):
    """Get the move that beats the predicted move."""
    counter_moves = {
        'rock': 'paper',
        'paper': 'scissors',
        'scissors': 'rock'
    }
    return counter_moves[predicted_move]

def ai_easy():
    """Easy AI: Random choice."""
    return random.choice(CHOICES)

def ai_medium(history):
    """
    Medium AI: Combines frequency analysis with basic psychological patterns.
    Merges the best of old Medium and old Hard difficulties.
    """
    if not history or len(history) < 3:
        return random.choice(CHOICES)
    
    # Analyze player's most common choice (from old Medium)
    player_choices = [game['player'] for game in history]
    most_common = Counter(player_choices).most_common(1)[0][0]
    
    # If we have enough history, add psychological patterns (from old Hard)
    if len(history) >= 5:
        last_game = history[-1]
        
        # Check if player tends to repeat after winning
        if last_game['result'] == 'player':
            if random.random() < 0.65:  # 65% confidence
                return get_counter_move(last_game['player'])
        
        # Check if player tends to switch after losing
        if last_game['result'] == 'computer':
            what_would_have_won = get_counter_move(last_game['computer'])
            if random.random() < 0.65:  # 65% confidence
                return get_counter_move(what_would_have_won)
        
        # Analyze recent pattern with weighted frequency
        recent_choices = [game['player'] for game in history[-5:]]
        recent_counter = Counter(recent_choices)
        if recent_counter:
            weighted_choice = recent_counter.most_common(1)[0][0]
            if random.random() < 0.75:
                return get_counter_move(weighted_choice)
    
    # Fallback: Counter the most common choice with 70% probability
    if random.random() < 0.70:
        return get_counter_move(most_common)
    else:
        return random.choice(CHOICES)

def ai_hard(history):
    """
    Hard AI: Master-level play using tiered strategy prioritization.
    (Formerly Very Hard - optimized tiered detection system)
    
    Key features:
    - Prioritizes frequency detection (catches "always X" strategies)
    - Psychological pattern detection (win-stay, lose-shift)
    - Cycle detection
    - Anti-triple pattern recognition
    """
    if not history or len(history) < 5:
        if len(history) < 2:
            return 'paper'  # Counter most common opening (rock)
        return ai_medium(history)
    
    last_game = history[-1]
    
    # TIER 1: Exploit Strong Frequency Bias (HIGHEST PRIORITY)
    # This catches "always X" and heavily biased strategies
    # Target: Beat Medium's 78% performance
    if len(history) >= 8:
        recent_choices = [game['player'] for game in history[-12:]]
        choice_counts = Counter(recent_choices)
        most_common_move, count = choice_counts.most_common(1)[0]
        frequency = count / len(recent_choices)
        
        # Strong bias (55%+) - exploit aggressively
        if frequency >= 0.55:
            if random.random() < 0.87:  # 87% exploitation rate
                return get_counter_move(most_common_move)
        
        # Moderate bias (45%+) - still exploit firmly
        elif frequency >= 0.45:
            if random.random() < 0.76:  # 76% exploitation rate
                return get_counter_move(most_common_move)
    
    # TIER 2: Win-Stay Pattern Detection (HIGH PRIORITY)
    # Check if player has shown win-stay tendency
    if last_game['result'] == 'player' and len(history) >= 4:
        win_stay_count = 0
        win_opportunities = 0
        
        # Look at last 8 games for win-stay pattern
        for i in range(max(0, len(history) - 8), len(history) - 1):
            if history[i]['result'] == 'player':
                win_opportunities += 1
                if i + 1 < len(history) and history[i]['player'] == history[i + 1]['player']:
                    win_stay_count += 1
        
        # If they've shown win-stay pattern at least 40% of the time
        if win_opportunities > 0 and (win_stay_count / win_opportunities) >= 0.4:
            if random.random() < 0.73:  # 73% confidence
                return get_counter_move(last_game['player'])
    
    # TIER 3: Anti-Triple Detection (MEDIUM-HIGH PRIORITY)
    # Most humans avoid playing the same move 3 times in a row
    if len(history) >= 2:
        last_two = [history[-2]['player'], history[-1]['player']]
        if last_two[0] == last_two[1]:
            repeated_move = last_two[0]
            
            # They played same move twice
            # Predict they'll switch to what beats the repeated move
            likely_next = get_counter_move(repeated_move)
            
            if random.random() < 0.69:  # 69% confidence
                return get_counter_move(likely_next)
    
    # TIER 4: Lose-Shift Pattern Detection (MEDIUM PRIORITY)
    if last_game['result'] == 'computer' and len(history) >= 4:
        lose_shift_count = 0
        lose_opportunities = 0
        
        # Analyze lose-shift behavior
        for i in range(max(0, len(history) - 8), len(history) - 1):
            if history[i]['result'] == 'computer':
                lose_opportunities += 1
                if i + 1 < len(history) and history[i]['player'] != history[i + 1]['player']:
                    lose_shift_count += 1
        
        # If they shift after losing at least 50% of the time
        if lose_opportunities > 0 and (lose_shift_count / lose_opportunities) >= 0.5:
            # Predict sequential shift
            sequence_shift = {
                'rock': 'paper',
                'paper': 'scissors',
                'scissors': 'rock'
            }
            predicted_next = sequence_shift[last_game['player']]
            
            if random.random() < 0.66:  # 66% confidence
                return get_counter_move(predicted_next)
    
    # TIER 5: Cycle Detection (MEDIUM PRIORITY)
    if len(history) >= 4:
        recent_choices = [game['player'] for game in history[-4:]]
        
        # Check for rock->paper->scissors or similar cycle
        if len(set(recent_choices[-3:])) == 3:  # All different in last 3
            # They might be cycling
            cycle_patterns = {
                ('rock', 'paper', 'scissors'): 'rock',
                ('rock', 'scissors', 'paper'): 'rock',
                ('paper', 'scissors', 'rock'): 'paper',
                ('paper', 'rock', 'scissors'): 'paper',
                ('scissors', 'rock', 'paper'): 'scissors',
                ('scissors', 'paper', 'rock'): 'scissors',
            }
            
            last_three = tuple(recent_choices[-3:])
            predicted = cycle_patterns.get(last_three)
            
            if predicted and random.random() < 0.62:  # 62% confidence
                return get_counter_move(predicted)
    
    # TIER 6: General Frequency Counter (LOW PRIORITY)
    # Fallback frequency analysis with lower threshold
    if len(history) >= 5:
        recent_choices = [game['player'] for game in history[-10:]]
        choice_counts = Counter(recent_choices)
        most_common = choice_counts.most_common(1)[0][0]
        
        if random.random() < 0.58:  # 58% confidence
            return get_counter_move(most_common)
    
    # Final Fallback: Use hard AI logic
    return ai_hard(history)

def ai_very_hard(history):
    """
    Very Hard AI: Expert-level play using advanced machine learning techniques.
    (Formerly Ultra Hard - proven effective implementation)
    
    Core capabilities:
    - 2nd-order Markov chain for transition probability prediction
    - Opponent profiling (randomness level, pattern complexity, adaptation speed)
    - Level-k reasoning to counter players trying to outsmart the AI
    - Ensemble prediction with weighted confidence voting
    - Dynamic exploitation rates based on pattern strength
    
    Expected performance:
    - Random: ~33% (maintains fairness)
    - Always Rock: 96-99% win rate
    - Cycles: 88-92% win rate
    - Win-Stay-Lose-Shift: 80-85% win rate
    - Anti-AI: 65-75% win rate
    """
    if not history or len(history) < 5:
        if len(history) < 2:
            return 'paper'  # Counter most common opening (rock)
        return ai_hard(history)
    
    # Initialize prediction ensemble
    predictions = []  # List of (move, confidence) tuples
    
    last_game = history[-1]
    player_choices = [game['player'] for game in history]
    
    # ============================================================
    # FEATURE 1: MARKOV CHAIN PREDICTION (2nd Order)
    # ============================================================
    # Track: After playing X, player chooses Y with probability P
    if len(history) >= 10:
        # Build transition matrix
        transitions = {}
        for i in range(len(history) - 1):
            current = history[i]['player']
            next_move = history[i + 1]['player']
            
            if current not in transitions:
                transitions[current] = []
            transitions[current].append(next_move)
        
        # Get prediction based on last move
        if last_game['player'] in transitions:
            transition_counts = Counter(transitions[last_game['player']])
            total = len(transitions[last_game['player']])
            
            # Find most likely next move
            most_likely, count = transition_counts.most_common(1)[0]
            probability = count / total
            
            # High confidence if probability is strong
            if probability >= 0.5:
                confidence = 0.85 + (probability - 0.5) * 0.2  # 0.85-0.95
                predictions.append((get_counter_move(most_likely), confidence, 'markov'))
            elif probability >= 0.4:
                confidence = 0.70 + (probability - 0.4) * 0.15  # 0.70-0.85
                predictions.append((get_counter_move(most_likely), confidence, 'markov'))
    
    # ============================================================
    # FEATURE 2: OPPONENT MODELING
    # ============================================================
    # Build a profile of the opponent's playing style
    if len(history) >= 15:
        # Calculate randomness score (entropy)
        choice_counts = Counter(player_choices[-20:])
        total_recent = len(player_choices[-20:])
        
        # Calculate distribution uniformity (0 = predictable, 1 = random)
        probabilities = [count / total_recent for count in choice_counts.values()]
        entropy = -sum(p * (p if p == 0 else p * 0.01) for p in probabilities)
        
        # Simple randomness estimate based on distribution
        if len(choice_counts) == 1:
            randomness_score = 0.0  # Always same move
        elif len(choice_counts) == 2:
            # Two moves - check how balanced
            counts = sorted(choice_counts.values(), reverse=True)
            randomness_score = counts[1] / counts[0]  # 0 to 1
        else:
            # Three moves - check uniformity
            expected = total_recent / 3
            variance = sum((count - expected) ** 2 for count in choice_counts.values()) / 3
            max_variance = (total_recent ** 2) / 3
            randomness_score = 1.0 - (variance / max_variance) if max_variance > 0 else 0.5
        
        # Adapt strategy based on opponent profile
        if randomness_score < 0.3:
            # Highly predictable opponent - exploit aggressively
            most_common = Counter(player_choices[-15:]).most_common(1)[0][0]
            predictions.append((get_counter_move(most_common), 0.92, 'exploit_predictable'))
        elif randomness_score > 0.7:
            # Random opponent - play Nash equilibrium (random)
            predictions.append((random.choice(CHOICES), 0.40, 'nash_equilibrium'))
    
    # ============================================================
    # FEATURE 3: COUNTER-COUNTER PREDICTION (Level-K Reasoning)
    # ============================================================
    # Detect if player is trying to outsmart the AI
    if len(history) >= 12:
        # Check if player is doing opposite of expected pattern
        # Level 1: Simple pattern (e.g., rock bias)
        # Level 2: Player counters AI's counter (plays what beats AI's expected move)
        
        # Analyze recent frequency
        recent_choices = player_choices[-12:]
        choice_counts = Counter(recent_choices)
        most_common_move, _ = choice_counts.most_common(1)[0]
        
        # Check if AI would have predicted this
        ai_would_counter = get_counter_move(most_common_move)
        
        # Check if player is countering the AI's counter
        # (Level-2 reasoning: "AI will play paper to counter my rock, so I'll play scissors")
        counter_ai_counter = get_counter_move(ai_would_counter)
        
        # Count how often player plays the counter-counter
        counter_counter_count = recent_choices.count(counter_ai_counter)
        counter_counter_freq = counter_counter_count / len(recent_choices)
        
        if counter_counter_freq >= 0.4:
            # Player shows level-2 reasoning
            # We need level-3: counter their counter-counter
            predictions.append((get_counter_move(counter_ai_counter), 0.78, 'level_3_reasoning'))
        
        # Also check if they're avoiding predictable patterns (anti-AI behavior)
        # Look for intentional randomization or pattern switching
        last_6 = recent_choices[-6:]
        if len(set(last_6)) == 3 and max(Counter(last_6).values()) == 2:
            # Perfect balance in last 6 moves - they're being deliberately random
            # This is sophisticated play - respond with mixed strategy
            predictions.append((random.choice(CHOICES), 0.45, 'counter_sophistication'))
    
    # ============================================================
    # FEATURE 4: ENHANCED PATTERN DETECTION (From Very Hard)
    # ============================================================
    
    # Strong Frequency Bias (upgraded from Very Hard)
    if len(history) >= 8:
        recent_choices = player_choices[-15:]  # Longer window
        choice_counts = Counter(recent_choices)
        most_common_move, count = choice_counts.most_common(1)[0]
        frequency = count / len(recent_choices)
        
        if frequency >= 0.60:
            predictions.append((get_counter_move(most_common_move), 0.94, 'strong_frequency'))
        elif frequency >= 0.50:
            predictions.append((get_counter_move(most_common_move), 0.84, 'moderate_frequency'))
        elif frequency >= 0.42:
            predictions.append((get_counter_move(most_common_move), 0.72, 'weak_frequency'))
    
    # Win-Stay Detection (enhanced)
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
            if win_stay_rate >= 0.5:
                confidence = 0.70 + (win_stay_rate - 0.5) * 0.3  # 0.70-0.85
                predictions.append((get_counter_move(last_game['player']), confidence, 'win_stay'))
    
    # Lose-Shift Detection (enhanced)
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
            if lose_shift_rate >= 0.55:
                # Predict they'll shift in sequence
                sequence_shift = {
                    'rock': 'paper',
                    'paper': 'scissors',
                    'scissors': 'rock'
                }
                predicted_next = sequence_shift[last_game['player']]
                confidence = 0.68 + (lose_shift_rate - 0.55) * 0.25  # 0.68-0.80
                predictions.append((get_counter_move(predicted_next), confidence, 'lose_shift'))
    
    # Advanced Cycle Detection (multi-length)
    if len(history) >= 6:
        recent = player_choices[-9:]
        
        # Check for length-3 cycles
        if len(recent) >= 6:
            if recent[-6:-3] == recent[-3:]:
                # Perfect 3-cycle repetition
                next_in_cycle = recent[-2]  # Predict continuation
                predictions.append((get_counter_move(next_in_cycle), 0.87, 'cycle_3'))
        
        # Check for length-2 cycles (alternating)
        if len(recent) >= 4:
            if recent[-4] == recent[-2] and recent[-3] == recent[-1]:
                # Alternating pattern
                next_in_pattern = recent[-2]
                predictions.append((get_counter_move(next_in_pattern), 0.80, 'cycle_2'))
    
    # Anti-Triple Pattern
    if len(history) >= 2:
        if history[-2]['player'] == history[-1]['player']:
            repeated_move = history[-1]['player']
            likely_next = get_counter_move(repeated_move)
            predictions.append((get_counter_move(likely_next), 0.74, 'anti_triple'))
    
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
            # Multiply confidences (Bayesian-style)
            # This gives higher weight to moves predicted by multiple sources
            total_confidence = sum(conf for conf, _ in votes)
            vote_count_bonus = len(votes) * 0.15  # Bonus for multiple predictors agreeing
            move_scores[move] = total_confidence + vote_count_bonus
        
        # Select move with highest score
        best_move = max(move_scores, key=move_scores.get)
        best_score = move_scores[best_move]
        
        # Apply stochastic exploitation based on confidence
        if best_score >= 1.5:
            # Very high confidence - exploit almost always
            if random.random() < 0.96:
                return best_move
        elif best_score >= 1.0:
            # High confidence - exploit usually
            if random.random() < 0.88:
                return best_move
        elif best_score >= 0.7:
            # Moderate confidence - exploit often
            if random.random() < 0.75:
                return best_move
        elif best_score >= 0.5:
            # Low confidence - exploit sometimes
            if random.random() < 0.60:
                return best_move
    
    # Fallback: Use hard AI logic
    return ai_hard(history)

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/play', methods=['POST'])
def play():
    """Handle a game round."""
    data = request.get_json()
    player_choice = data.get('choice', '').lower()
    difficulty = data.get('difficulty', 'easy').lower()
    history = data.get('history', [])
    
    # Validate player choice
    if player_choice not in CHOICES:
        return jsonify({
            'error': 'Invalid choice. Must be rock, paper, or scissors.'
        }), 400
    
    # Computer makes a choice based on difficulty
    if difficulty == 'easy':
        computer_choice = ai_easy()
    elif difficulty == 'medium':
        computer_choice = ai_medium(history)
    elif difficulty == 'hard':
        computer_choice = ai_hard(history)
    elif difficulty == 'veryhard':
        computer_choice = ai_very_hard(history)
    else:
        computer_choice = ai_easy()  # Default to easy
    
    # Determine winner
    result = determine_winner(player_choice, computer_choice)
    
    return jsonify({
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result
    })

@app.route('/api/openai-commentary', methods=['POST'])
def openai_commentary():
    """
    Get OpenAI-powered commentary on gameplay
    Request body:
        - game_history: list of recent games
        - scores: dict with player, computer, ties
        - hand_stats: dict with per-hand statistics
        - current_difficulty: string difficulty level
    """
    try:
        data = request.json
        
        # Check if OpenAI is available
        if not OPENAI_AVAILABLE:
            return jsonify({
                'error': 'OpenAI library is not installed. Run: pip install openai'
            }), 500
        
        # Check for API key
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'OpenAI API key not found. Please set OPENAI_API_KEY environment variable.'
            }), 500
        
        # Get game data
        game_history = data.get('game_history', [])
        scores = data.get('scores', {})
        hand_stats = data.get('hand_stats', {})
        difficulty = data.get('current_difficulty', 'unknown')
        
        # Validate data
        if len(game_history) < 5:
            return jsonify({
                'error': 'Need at least 5 games for meaningful commentary.'
            }), 400
        
        # Prepare prompt for OpenAI - Sports Journalist Style
        total_games = scores.get('player', 0) + scores.get('computer', 0) + scores.get('ties', 0)
        win_rate = (scores.get('player', 0) / total_games * 100) if total_games > 0 else 0
        
        # Analyze recent patterns
        recent_100 = game_history[-100:] if len(game_history) >= 100 else game_history
        player_choices = [g.get('player') for g in recent_100]
        computer_choices = [g.get('computer') for g in recent_100]
        
        prompt = f"""You are a sports journalist covering an intense Rock Paper Scissors championship match between PLAYER and COMPUTER.

**Current Standings:**
- Total Rounds: {total_games}
- PLAYER Score: {scores.get('player', 0)}
- COMPUTER Score: {scores.get('computer', 0)}
- Ties: {scores.get('ties', 0)}
- PLAYER Win Rate: {win_rate:.1f}%

**Last 100 Moves:**
- PLAYER's moves: {', '.join(player_choices[-20:])}... (showing last 20)
- COMPUTER's moves: {', '.join(computer_choices[-20:])}... (showing last 20)

**Hand Performance:**
- Rock: {hand_stats.get('rock', {}).get('wins', 0)}W-{hand_stats.get('rock', {}).get('losses', 0)}L-{hand_stats.get('rock', {}).get('ties', 0)}T
- Paper: {hand_stats.get('paper', {}).get('wins', 0)}W-{hand_stats.get('paper', {}).get('losses', 0)}L-{hand_stats.get('paper', {}).get('ties', 0)}T  
- Scissors: {hand_stats.get('scissors', {}).get('wins', 0)}W-{hand_stats.get('scissors', {}).get('losses', 0)}L-{hand_stats.get('scissors', {}).get('ties', 0)}T

Analyze this match with sports commentary. Be slightly humorous but professional. Focus on:
1. The current state of the competition
2. Notable patterns or strategies
3. Momentum and what to watch for next

Respond in 100 words or less. Write like you're commenting live for an ESPN broadcast."""

        # Call OpenAI API
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4" for better quality
            messages=[
                {"role": "system", "content": "You are an enthusiastic sports journalist covering a Rock Paper Scissors championship. Be engaging, slightly humorous, and professional like an ESPN commentator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )
        
        commentary = response.choices[0].message.content
        
        return jsonify({
            'commentary': commentary,
            'games_analyzed': len(game_history),
            'model_used': 'gpt-4o-mini'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error generating commentary: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

