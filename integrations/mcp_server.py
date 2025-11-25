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
import math
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
                            "enum": ["easy", "medium", "hard", "veryhard"],
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
        """Medium AI: Combines frequency analysis with basic psychological patterns."""
        if len(self.game_history) < 3:
            return self.ai_easy()
        
        recent_player_moves = [game['player'] for game in self.game_history[-10:]]
        most_common = Counter(recent_player_moves).most_common(1)[0][0]
        
        # Add psychological patterns if enough history
        if len(self.game_history) >= 5:
            last_game = self.game_history[-1]
            
            if last_game['result'] == 'player' and random.random() < 0.65:
                return self.get_counter_move(last_game['player'])
            
            if last_game['result'] == 'computer':
                what_would_have_won = self.get_counter_move(last_game['computer'])
                if random.random() < 0.65:
                    return self.get_counter_move(what_would_have_won)
        
        if random.random() < 0.70:
            return self.get_counter_move(most_common)
        return self.ai_easy()
    
    def ai_hard(self):
        """
        Hard AI: Master-level play using tiered strategy prioritization.
        (Formerly Very Hard)
        """
        if len(self.game_history) < 5:
            if len(self.game_history) < 2:
                return 'paper'  # Counter most common opening (rock)
            return self.ai_hard()
        
        last_game = self.game_history[-1]
        
        # TIER 1: Exploit Strong Frequency Bias (HIGHEST PRIORITY)
        if len(self.game_history) >= 8:
            recent_choices = [game['player'] for game in self.game_history[-12:]]
            choice_counts = Counter(recent_choices)
            most_common_move, count = choice_counts.most_common(1)[0]
            frequency = count / len(recent_choices)
            
            # Strong bias (55%+) - exploit aggressively
            if frequency >= 0.55:
                if random.random() < 0.87:  # 87% exploitation rate
                    return self.get_counter_move(most_common_move)
            
            # Moderate bias (45%+) - still exploit firmly
            elif frequency >= 0.45:
                if random.random() < 0.76:  # 76% exploitation rate
                    return self.get_counter_move(most_common_move)
        
        # TIER 2: Win-Stay Pattern Detection (HIGH PRIORITY)
        if last_game['result'] == 'player' and len(self.game_history) >= 4:
            win_stay_count = 0
            win_opportunities = 0
            
            # Look at last 8 games for win-stay pattern
            for i in range(max(0, len(self.game_history) - 8), len(self.game_history) - 1):
                if self.game_history[i]['result'] == 'player':
                    win_opportunities += 1
                    if i + 1 < len(self.game_history) and self.game_history[i]['player'] == self.game_history[i + 1]['player']:
                        win_stay_count += 1
            
            # If they've shown win-stay pattern at least 40% of the time
            if win_opportunities > 0 and (win_stay_count / win_opportunities) >= 0.4:
                if random.random() < 0.73:  # 73% confidence
                    return self.get_counter_move(last_game['player'])
        
        # TIER 3: Anti-Triple Detection (MEDIUM-HIGH PRIORITY)
        if len(self.game_history) >= 2:
            last_two = [self.game_history[-2]['player'], self.game_history[-1]['player']]
            if last_two[0] == last_two[1]:
                repeated_move = last_two[0]
                # Predict they'll switch to what beats the repeated move
                likely_next = self.get_counter_move(repeated_move)
                
                if random.random() < 0.69:  # 69% confidence
                    return self.get_counter_move(likely_next)
        
        # TIER 4: Lose-Shift Pattern Detection (MEDIUM PRIORITY)
        if last_game['result'] == 'computer' and len(self.game_history) >= 4:
            lose_shift_count = 0
            lose_opportunities = 0
            
            # Analyze lose-shift behavior
            for i in range(max(0, len(self.game_history) - 8), len(self.game_history) - 1):
                if self.game_history[i]['result'] == 'computer':
                    lose_opportunities += 1
                    if i + 1 < len(self.game_history) and self.game_history[i]['player'] != self.game_history[i + 1]['player']:
                        lose_shift_count += 1
            
            # If they shift after losing at least 50% of the time
            if lose_opportunities > 0 and (lose_shift_count / lose_opportunities) >= 0.5:
                sequence_shift = {
                    'rock': 'paper',
                    'paper': 'scissors',
                    'scissors': 'rock'
                }
                predicted_next = sequence_shift[last_game['player']]
                
                if random.random() < 0.66:  # 66% confidence
                    return self.get_counter_move(predicted_next)
        
        # TIER 5: Cycle Detection (MEDIUM PRIORITY)
        if len(self.game_history) >= 4:
            recent_choices = [game['player'] for game in self.game_history[-4:]]
            
            # Check for rock->paper->scissors or similar cycle
            if len(set(recent_choices[-3:])) == 3:  # All different in last 3
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
                    return self.get_counter_move(predicted)
        
        # TIER 6: General Frequency Counter (LOW PRIORITY)
        if len(self.game_history) >= 5:
            recent_choices = [game['player'] for game in self.game_history[-10:]]
            choice_counts = Counter(recent_choices)
            most_common = choice_counts.most_common(1)[0][0]
            
            if random.random() < 0.58:  # 58% confidence
                return self.get_counter_move(most_common)
        
        # Final Fallback: Use hard AI logic
        return self.ai_hard()
    
    def ai_very_hard(self):
        """
        Very Hard AI: Ultimate expert-level play with cutting-edge techniques.
        (Formerly Ultra Hard + Advanced features)
        """
        if len(self.game_history) < 5:
            if len(self.game_history) < 2:
                return 'paper'
            return self.ai_hard()
        
        predictions = []
        last_game = self.game_history[-1]
        player_choices = [game['player'] for game in self.game_history]
        
        # Markov Chain Prediction
        if len(self.game_history) >= 10:
            transitions = {}
            for i in range(len(self.game_history) - 1):
                current = self.game_history[i]['player']
                next_move = self.game_history[i + 1]['player']
                if current not in transitions:
                    transitions[current] = []
                transitions[current].append(next_move)
            
            if last_game['player'] in transitions:
                transition_counts = Counter(transitions[last_game['player']])
                total = len(transitions[last_game['player']])
                most_likely, count = transition_counts.most_common(1)[0]
                probability = count / total
                
                if probability >= 0.5:
                    confidence = 0.85 + (probability - 0.5) * 0.2
                    predictions.append((self.get_counter_move(most_likely), confidence, 'markov'))
                elif probability >= 0.4:
                    confidence = 0.70 + (probability - 0.4) * 0.15
                    predictions.append((self.get_counter_move(most_likely), confidence, 'markov'))
        
        # Opponent Modeling
        if len(self.game_history) >= 15:
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
            
            if randomness_score < 0.3:
                most_common = Counter(player_choices[-15:]).most_common(1)[0][0]
                predictions.append((self.get_counter_move(most_common), 0.92, 'exploit_predictable'))
            elif randomness_score > 0.7:
                predictions.append((random.choice(['rock', 'paper', 'scissors']), 0.40, 'nash_equilibrium'))
        
        # Counter-Counter Prediction
        if len(self.game_history) >= 12:
            recent_choices = player_choices[-12:]
            choice_counts = Counter(recent_choices)
            most_common_move, _ = choice_counts.most_common(1)[0]
            ai_would_counter = self.get_counter_move(most_common_move)
            counter_ai_counter = self.get_counter_move(ai_would_counter)
            counter_counter_count = recent_choices.count(counter_ai_counter)
            counter_counter_freq = counter_counter_count / len(recent_choices)
            
            if counter_counter_freq >= 0.4:
                predictions.append((self.get_counter_move(counter_ai_counter), 0.78, 'level_3_reasoning'))
            
            last_6 = recent_choices[-6:]
            if len(set(last_6)) == 3 and max(Counter(last_6).values()) == 2:
                predictions.append((random.choice(['rock', 'paper', 'scissors']), 0.45, 'counter_sophistication'))
        
        # Enhanced Pattern Detection
        if len(self.game_history) >= 8:
            recent_choices = player_choices[-15:]
            choice_counts = Counter(recent_choices)
            most_common_move, count = choice_counts.most_common(1)[0]
            frequency = count / len(recent_choices)
            
            if frequency >= 0.60:
                predictions.append((self.get_counter_move(most_common_move), 0.94, 'strong_frequency'))
            elif frequency >= 0.50:
                predictions.append((self.get_counter_move(most_common_move), 0.84, 'moderate_frequency'))
            elif frequency >= 0.42:
                predictions.append((self.get_counter_move(most_common_move), 0.72, 'weak_frequency'))
        
        # Win-Stay Detection
        if last_game['result'] == 'player' and len(self.game_history) >= 6:
            win_stay_count = 0
            win_opportunities = 0
            for i in range(max(0, len(self.game_history) - 12), len(self.game_history) - 1):
                if self.game_history[i]['result'] == 'player':
                    win_opportunities += 1
                    if i + 1 < len(self.game_history) and self.game_history[i]['player'] == self.game_history[i + 1]['player']:
                        win_stay_count += 1
            
            if win_opportunities > 0:
                win_stay_rate = win_stay_count / win_opportunities
                if win_stay_rate >= 0.5:
                    confidence = 0.70 + (win_stay_rate - 0.5) * 0.3
                    predictions.append((self.get_counter_move(last_game['player']), confidence, 'win_stay'))
        
        # Lose-Shift Detection
        if last_game['result'] == 'computer' and len(self.game_history) >= 6:
            lose_shift_count = 0
            lose_opportunities = 0
            for i in range(max(0, len(self.game_history) - 12), len(self.game_history) - 1):
                if self.game_history[i]['result'] == 'computer':
                    lose_opportunities += 1
                    if i + 1 < len(self.game_history) and self.game_history[i]['player'] != self.game_history[i + 1]['player']:
                        lose_shift_count += 1
            
            if lose_opportunities > 0:
                lose_shift_rate = lose_shift_count / lose_opportunities
                if lose_shift_rate >= 0.55:
                    sequence_shift = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                    predicted_next = sequence_shift[last_game['player']]
                    confidence = 0.68 + (lose_shift_rate - 0.55) * 0.25
                    predictions.append((self.get_counter_move(predicted_next), confidence, 'lose_shift'))
        
        # Cycle Detection
        if len(self.game_history) >= 6:
            recent = player_choices[-9:]
            if len(recent) >= 6:
                if recent[-6:-3] == recent[-3:]:
                    next_in_cycle = recent[-2]
                    predictions.append((self.get_counter_move(next_in_cycle), 0.87, 'cycle_3'))
            if len(recent) >= 4:
                if recent[-4] == recent[-2] and recent[-3] == recent[-1]:
                    next_in_pattern = recent[-2]
                    predictions.append((self.get_counter_move(next_in_pattern), 0.80, 'cycle_2'))
        
        # Anti-Triple Pattern
        if len(self.game_history) >= 2:
            if self.game_history[-2]['player'] == self.game_history[-1]['player']:
                repeated_move = self.game_history[-1]['player']
                likely_next = self.get_counter_move(repeated_move)
                predictions.append((self.get_counter_move(likely_next), 0.74, 'anti_triple'))
        
        # Ensemble Voting
        if predictions:
            move_votes = {}
            for move, confidence, source in predictions:
                if move not in move_votes:
                    move_votes[move] = []
                move_votes[move].append((confidence, source))
            
            move_scores = {}
            for move, votes in move_votes.items():
                total_confidence = sum(conf for conf, _ in votes)
                vote_count_bonus = len(votes) * 0.15
                move_scores[move] = total_confidence + vote_count_bonus
            
            best_move = max(move_scores, key=move_scores.get)
            best_score = move_scores[best_move]
            
            if best_score >= 1.5 and random.random() < 0.96:
                return best_move
            elif best_score >= 1.0 and random.random() < 0.88:
                return best_move
            elif best_score >= 0.7 and random.random() < 0.75:
                return best_move
            elif best_score >= 0.5 and random.random() < 0.60:
                return best_move
        
        return self.ai_hard()
    
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
        elif difficulty == 'veryhard':
            computer_choice = self.ai_very_hard()
        else:  # medium is default
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

