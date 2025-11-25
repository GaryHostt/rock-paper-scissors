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
    """Medium AI: Counters the player's most frequently played hand."""
    if not history or len(history) < 3:
        return random.choice(CHOICES)
    
    # Analyze player's most common choice
    player_choices = [game['player'] for game in history]
    most_common = Counter(player_choices).most_common(1)[0][0]
    
    # Counter the most common choice with 70% probability
    if random.random() < 0.7:
        return get_counter_move(most_common)
    else:
        return random.choice(CHOICES)

def ai_hard(history):
    """Hard AI: Advanced pattern recognition."""
    if not history or len(history) < 5:
        return random.choice(CHOICES)
    
    # Look at recent trends (last 5 games)
    recent_choices = [game['player'] for game in history[-5:]]
    
    # Check if player tends to repeat after winning
    if len(history) >= 2:
        last_game = history[-1]
        if last_game['result'] == 'player':
            # Player won last game, likely to repeat (common psychology)
            if random.random() < 0.6:
                return get_counter_move(last_game['player'])
    
    # Check if player tends to switch after losing
    if len(history) >= 2:
        last_game = history[-1]
        if last_game['result'] == 'computer':
            # Player lost, likely to switch to what would have won
            what_would_have_won = get_counter_move(last_game['computer'])
            if random.random() < 0.6:
                return get_counter_move(what_would_have_won)
    
    # Analyze recent pattern with weighted frequency
    recent_counter = Counter(recent_choices)
    if recent_counter:
        # Weight recent choices more heavily
        weighted_choice = recent_counter.most_common(1)[0][0]
        if random.random() < 0.75:
            return get_counter_move(weighted_choice)
    
    # Fallback to countering most common overall
    all_choices = [game['player'] for game in history]
    most_common = Counter(all_choices).most_common(1)[0][0]
    return get_counter_move(most_common)

def ai_very_hard(history):
    """
    Very Hard AI: Master strategist using advanced game theory and psychology.
    
    Implements multiple advanced strategies:
    1. Win-Stay, Lose-Shift Detection
    2. Double-Throw Pattern (avoid repetition)
    3. Opening move counter (Paper first defense)
    4. Pattern frequency analysis
    5. Sequence prediction
    """
    if not history or len(history) < 2:
        # First move: Statistically, Rock is most common (35%), so play Paper
        return 'paper'
    
    last_game = history[-1]
    
    # Strategy 1: Win-Stay, Lose-Shift Heuristic (Most exploitable pattern)
    if len(history) >= 2:
        prev_game = history[-2]
        
        # If player won last round, they likely repeat (Win-Stay)
        if last_game['result'] == 'player':
            if random.random() < 0.75:  # 75% confidence
                # Counter the repeated move
                return get_counter_move(last_game['player'])
        
        # If player lost last round, they likely shift to next in sequence (Lose-Shift)
        if last_game['result'] == 'computer':
            if random.random() < 0.70:  # 70% confidence
                # Predict the shift: Rock -> Paper -> Scissors -> Rock
                sequence_shift = {
                    'rock': 'paper',
                    'paper': 'scissors', 
                    'scissors': 'rock'
                }
                predicted_next = sequence_shift[last_game['player']]
                return get_counter_move(predicted_next)
    
    # Strategy 2: Double-Throw Detection (Humans avoid 3x repetition)
    if len(history) >= 2:
        last_two = [history[-2]['player'], history[-1]['player']]
        if last_two[0] == last_two[1]:
            # Player played same move twice, they will NOT play it again
            repeated_move = last_two[0]
            # They will play one of the other two moves
            other_moves = [m for m in CHOICES if m != repeated_move]
            
            # Play the move that beats one and ties the other
            # If they played Rock-Rock, they'll play Paper or Scissors
            # We play Scissors (beats Paper, loses to Rock, ties Scissors)
            # But Rock is unlikely, so this is optimal
            if random.random() < 0.65:  # 65% confidence
                # Choose the move that counters what beats the repeated move
                what_beats_repeated = get_counter_move(repeated_move)
                # Counter that
                return get_counter_move(what_beats_repeated)
    
    # Strategy 3: Advanced Pattern Recognition (last 7 games)
    if len(history) >= 7:
        recent = history[-7:]
        
        # Check for alternating pattern
        player_choices = [g['player'] for g in recent]
        
        # Check if player is cycling through moves
        if len(set(player_choices[-3:])) == 3:
            # Player is cycling, predict next in their cycle
            last_three = player_choices[-3:]
            # Find the pattern
            cycle_map = {
                ('rock', 'paper', 'scissors'): 'rock',
                ('rock', 'scissors', 'paper'): 'rock',
                ('paper', 'rock', 'scissors'): 'paper',
                ('paper', 'scissors', 'rock'): 'paper',
                ('scissors', 'rock', 'paper'): 'scissors',
                ('scissors', 'paper', 'rock'): 'scissors',
            }
            predicted = cycle_map.get(tuple(last_three[-3:]))
            if predicted and random.random() < 0.60:
                return get_counter_move(predicted)
    
    # Strategy 4: Frequency Analysis with Recency Bias
    if len(history) >= 5:
        recent_choices = [game['player'] for game in history[-10:]]
        choice_counts = Counter(recent_choices)
        
        # Heavily weight the most common choice
        most_common = choice_counts.most_common(1)[0][0]
        
        if random.random() < 0.80:  # 80% confidence in frequency
            return get_counter_move(most_common)
    
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

@app.route('/mcp/play', methods=['POST'])
def mcp_play():
    """
    MCP (Model Context Protocol) endpoint for AI agents to play Rock Paper Scissors.
    
    This endpoint allows AI agents, bots, or other automated systems to play the game.
    Designed for integration with AI assistants, automation tools, and testing frameworks.
    
    Request Body:
        {
            "agent_id": "unique_agent_identifier",
            "choice": "rock|paper|scissors",
            "opponent_difficulty": "easy|medium|hard",
            "session_history": [...]  // Optional: previous games for context
        }
    
    Response:
        {
            "agent_choice": "rock",
            "opponent_choice": "scissors",
            "result": "agent_win|opponent_win|tie",
            "agent_id": "unique_agent_identifier",
            "game_number": 1,
            "session_stats": {
                "agent_wins": 1,
                "opponent_wins": 0,
                "ties": 0
            }
        }
    """
    data = request.get_json()
    
    # Extract agent information
    agent_id = data.get('agent_id', 'anonymous_agent')
    agent_choice = data.get('choice', '').lower()
    opponent_difficulty = data.get('opponent_difficulty', 'easy').lower()
    session_history = data.get('session_history', [])
    
    # Validate agent choice
    if agent_choice not in CHOICES:
        return jsonify({
            'error': 'Invalid choice. Must be rock, paper, or scissors.',
            'agent_id': agent_id,
            'valid_choices': CHOICES
        }), 400
    
    # Opponent makes a choice based on difficulty
    if opponent_difficulty == 'easy':
        opponent_choice = ai_easy()
    elif opponent_difficulty == 'medium':
        # Convert session history to format AI expects
        ai_history = [{'player': h.get('agent_choice'), 
                      'computer': h.get('opponent_choice'),
                      'result': 'player' if h.get('result') == 'agent_win' else ('computer' if h.get('result') == 'opponent_win' else 'tie')}
                     for h in session_history if 'agent_choice' in h]
        opponent_choice = ai_medium(ai_history)
    elif opponent_difficulty == 'hard':
        ai_history = [{'player': h.get('agent_choice'), 
                      'computer': h.get('opponent_choice'),
                      'result': 'player' if h.get('result') == 'agent_win' else ('computer' if h.get('result') == 'opponent_win' else 'tie')}
                     for h in session_history if 'agent_choice' in h]
        opponent_choice = ai_hard(ai_history)
    elif opponent_difficulty == 'veryhard':
        ai_history = [{'player': h.get('agent_choice'), 
                      'computer': h.get('opponent_choice'),
                      'result': 'player' if h.get('result') == 'agent_win' else ('computer' if h.get('result') == 'opponent_win' else 'tie')}
                     for h in session_history if 'agent_choice' in h]
        opponent_choice = ai_very_hard(ai_history)
    else:
        opponent_choice = ai_easy()
    
    # Determine winner
    game_result = determine_winner(agent_choice, opponent_choice)
    
    # Map result to agent-friendly format
    if game_result == 'player':
        mcp_result = 'agent_win'
    elif game_result == 'computer':
        mcp_result = 'opponent_win'
    else:
        mcp_result = 'tie'
    
    # Calculate session statistics
    session_stats = {
        'agent_wins': sum(1 for h in session_history if h.get('result') == 'agent_win'),
        'opponent_wins': sum(1 for h in session_history if h.get('result') == 'opponent_win'),
        'ties': sum(1 for h in session_history if h.get('result') == 'tie')
    }
    
    # Update stats with current game
    if mcp_result == 'agent_win':
        session_stats['agent_wins'] += 1
    elif mcp_result == 'opponent_win':
        session_stats['opponent_wins'] += 1
    else:
        session_stats['ties'] += 1
    
    return jsonify({
        'agent_choice': agent_choice,
        'opponent_choice': opponent_choice,
        'result': mcp_result,
        'agent_id': agent_id,
        'game_number': len(session_history) + 1,
        'session_stats': session_stats,
        'message': f"Agent chose {agent_choice}, opponent chose {opponent_choice}. Result: {mcp_result}!"
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

