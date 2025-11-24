from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
from collections import Counter

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

