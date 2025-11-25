#!/usr/bin/env python3
"""
MCP Endpoint Test Script for Rock Paper Scissors
Demonstrates how AI agents can interact with the game programmatically
"""

import requests
import json
import random

# Configuration
BASE_URL = "http://localhost:5000"
AGENT_ID = "test_agent_001"

def play_mcp_game(choice, difficulty='easy', history=None):
    """
    Play a game via the MCP endpoint
    
    Args:
        choice: 'rock', 'paper', or 'scissors'
        difficulty: 'easy', 'medium', or 'hard'
        history: Previous game history (optional)
    
    Returns:
        Response JSON from the server
    """
    endpoint = f"{BASE_URL}/mcp/play"
    
    payload = {
        'agent_id': AGENT_ID,
        'choice': choice,
        'opponent_difficulty': difficulty,
        'session_history': history or []
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def run_test_session(num_games=10, difficulty='medium'):
    """Run a test session with multiple games"""
    print(f"🤖 Starting MCP Test Session")
    print(f"Agent ID: {AGENT_ID}")
    print(f"Difficulty: {difficulty}")
    print(f"Games to play: {num_games}")
    print("=" * 60)
    
    choices = ['rock', 'paper', 'scissors']
    session_history = []
    
    for i in range(num_games):
        # Agent makes a random choice
        agent_choice = random.choice(choices)
        
        print(f"\n🎮 Game {i + 1}:")
        print(f"   Agent choice: {agent_choice}")
        
        # Play the game
        result = play_mcp_game(agent_choice, difficulty, session_history)
        
        if result:
            print(f"   Opponent choice: {result['opponent_choice']}")
            print(f"   Result: {result['result']}")
            print(f"   📊 Session Stats: {result['session_stats']}")
            
            # Add to history
            session_history.append({
                'agent_choice': result['agent_choice'],
                'opponent_choice': result['opponent_choice'],
                'result': result['result']
            })
        else:
            print("   ❌ Game failed!")
    
    print("\n" + "=" * 60)
    print("🏁 Session Complete!")
    
    if session_history:
        final_stats = session_history[-1] if play_mcp_game('rock', difficulty, session_history) else None
        if final_stats:
            stats = final_stats.get('session_stats', {})
            total = sum(stats.values()) if stats else 0
            if total > 0:
                win_rate = (stats.get('agent_wins', 0) / total) * 100
                print(f"   Agent Win Rate: {win_rate:.1f}%")

def test_all_difficulties():
    """Test agent against all difficulty levels"""
    difficulties = ['easy', 'medium', 'hard']
    
    for difficulty in difficulties:
        print(f"\n{'='*60}")
        print(f"Testing {difficulty.upper()} difficulty")
        print(f"{'='*60}")
        run_test_session(num_games=5, difficulty=difficulty)
        print("\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            test_all_difficulties()
        else:
            difficulty = sys.argv[1] if sys.argv[1] in ['easy', 'medium', 'hard'] else 'medium'
            num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            run_test_session(num_games=num_games, difficulty=difficulty)
    else:
        print("Usage:")
        print("  python test_mcp.py [difficulty] [num_games]")
        print("  python test_mcp.py --all")
        print("\nExamples:")
        print("  python test_mcp.py medium 10")
        print("  python test_mcp.py hard 20")
        print("  python test_mcp.py --all")
        print("\nRunning default test (10 games, medium difficulty)...\n")
        run_test_session()

