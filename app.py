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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

