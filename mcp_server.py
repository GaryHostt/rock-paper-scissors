#!/usr/bin/env python3
"""
MCP Server for Rock Paper Scissors Game
Implements the Model Context Protocol for Claude Desktop integration
"""

import asyncio
import json
import sys
from typing import Any
import random
from collections import Counter

# MCP protocol messages
class MCPServer:
    def __init__(self):
        self.tools = {
            "play_rps": {
                "name": "play_rps",
                "description": "Play a game of Rock Paper Scissors against an AI opponent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "choice": {
                            "type": "string",
                            "enum": ["rock", "paper", "scissors"],
                            "description": "Your choice: rock, paper, or scissors"
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "medium", "hard"],
                            "default": "medium",
                            "description": "AI difficulty level"
                        }
                    },
                    "required": ["choice"]
                }
            },
            "get_stats": {
                "name": "get_stats",
                "description": "Get current game statistics",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
        
        self.game_history = []
        self.stats = {
            "wins": 0,
            "losses": 0,
            "ties": 0
        }
    
    def determine_winner(self, player_choice, computer_choice):
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
    
    def get_counter_move(self, predicted_move):
        """Get the move that beats the predicted move."""
        counter_moves = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        return counter_moves[predicted_move]
    
    def ai_easy(self):
        """Easy AI: Random choice."""
        return random.choice(['rock', 'paper', 'scissors'])
    
    def ai_medium(self):
        """Medium AI: Counters the player's most frequently played hand."""
        if len(self.game_history) < 3:
            return self.ai_easy()
        
        recent_player_moves = [game['player'] for game in self.game_history[-10:]]
        most_common = Counter(recent_player_moves).most_common(1)[0][0]
        
        if random.random() < 0.7:
            return self.get_counter_move(most_common)
        return self.ai_easy()
    
    def ai_hard(self):
        """Hard AI: Predicts player's next move based on patterns."""
        if len(self.game_history) < 5:
            return self.ai_medium()
        
        recent_games = self.game_history[-10:]
        
        # Pattern 1: Win-Stay, Lose-Shift
        last_game = recent_games[-1]
        if last_game['result'] == 'player':
            predicted = last_game['player']
        else:
            losing_move = last_game['player']
            what_would_have_won = self.get_counter_move(last_game['computer'])
            predicted = what_would_have_won
        
        # Pattern 2: Recent frequency
        recent_moves = [g['player'] for g in recent_games]
        most_common = Counter(recent_moves).most_common(1)[0][0]
        
        # Combine predictions
        predictions = [predicted, most_common]
        final_prediction = random.choice(predictions)
        
        if random.random() < 0.75:
            return self.get_counter_move(final_prediction)
        
        return self.ai_easy()
    
    def play_game(self, choice: str, difficulty: str = "medium"):
        """Play a game and return the result."""
        choice = choice.lower()
        difficulty = difficulty.lower()
        
        if choice not in ['rock', 'paper', 'scissors']:
            return {"error": "Invalid choice. Must be rock, paper, or scissors."}
        
        # AI makes its choice
        if difficulty == 'easy':
            computer_choice = self.ai_easy()
        elif difficulty == 'hard':
            computer_choice = self.ai_hard()
        else:
            computer_choice = self.ai_medium()
        
        # Determine winner
        result = self.determine_winner(choice, computer_choice)
        
        # Update stats
        if result == 'player':
            self.stats['wins'] += 1
        elif result == 'computer':
            self.stats['losses'] += 1
        else:
            self.stats['ties'] += 1
        
        # Record game
        self.game_history.append({
            'player': choice,
            'computer': computer_choice,
            'result': result
        })
        
        return {
            "player_choice": choice,
            "computer_choice": computer_choice,
            "result": result,
            "message": self._get_result_message(choice, computer_choice, result),
            "stats": self.stats.copy(),
            "total_games": len(self.game_history)
        }
    
    def _get_result_message(self, player, computer, result):
        """Generate a friendly result message."""
        if result == 'tie':
            return f"It's a tie! Both chose {player}."
        elif result == 'player':
            return f"You win! {player.capitalize()} beats {computer}."
        else:
            return f"You lose! {computer.capitalize()} beats {player}."
    
    def get_statistics(self):
        """Get current game statistics."""
        total = len(self.game_history)
        win_rate = (self.stats['wins'] / total * 100) if total > 0 else 0
        
        return {
            "stats": self.stats.copy(),
            "total_games": total,
            "win_rate": round(win_rate, 1),
            "recent_games": self.game_history[-5:] if self.game_history else []
        }
    
    async def handle_request(self, request: dict) -> dict:
        """Handle incoming MCP requests."""
        method = request.get("method")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "rock-paper-scissors",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "tools": list(self.tools.values())
                }
            }
        
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "play_rps":
                result = self.play_game(
                    arguments.get("choice"),
                    arguments.get("difficulty", "medium")
                )
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            elif tool_name == "get_stats":
                result = self.get_statistics()
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }
    
    async def run(self):
        """Run the MCP server using stdio."""
        while True:
            try:
                # Read from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                # Parse JSON-RPC request
                request = json.loads(line.strip())
                
                # Handle request
                response = await self.handle_request(request)
                
                # Write response to stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

async def main():
    server = MCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

