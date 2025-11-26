"""
Simulated Opponent Agents for Hyperparameter Optimization

This module defines various opponent strategies to test AI performance against.
Each agent represents a different human playing pattern.
"""

import random
from typing import List, Dict


class OpponentAgent:
    """Base class for opponent agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.history = []
    
    def choose(self, history: List[Dict]) -> str:
        """
        Choose next move based on game history.
        
        Args:
            history: List of game dictionaries with 'player', 'computer', 'result'
        
        Returns:
            Choice: 'rock', 'paper', or 'scissors'
        """
        raise NotImplementedError
    
    def reset(self):
        """Reset agent state."""
        self.history = []


class RandomAgent(OpponentAgent):
    """Plays completely randomly (Nash equilibrium)."""
    
    def __init__(self):
        super().__init__("Random")
    
    def choose(self, history: List[Dict]) -> str:
        return random.choice(['rock', 'paper', 'scissors'])


class AlwaysRockAgent(OpponentAgent):
    """Always plays rock."""
    
    def __init__(self):
        super().__init__("Always Rock")
    
    def choose(self, history: List[Dict]) -> str:
        return 'rock'


class AlwaysPaperAgent(OpponentAgent):
    """Always plays paper."""
    
    def __init__(self):
        super().__init__("Always Paper")
    
    def choose(self, history: List[Dict]) -> str:
        return 'paper'


class AlwaysScissorsAgent(OpponentAgent):
    """Always plays scissors."""
    
    def __init__(self):
        super().__init__("Always Scissors")
    
    def choose(self, history: List[Dict]) -> str:
        return 'scissors'


class CycleAgent(OpponentAgent):
    """Cycles through rock -> paper -> scissors."""
    
    def __init__(self):
        super().__init__("Cycle")
        self.cycle = ['rock', 'paper', 'scissors']
        self.index = 0
    
    def choose(self, history: List[Dict]) -> str:
        choice = self.cycle[self.index]
        self.index = (self.index + 1) % 3
        return choice
    
    def reset(self):
        super().reset()
        self.index = 0


class ReverseCycleAgent(OpponentAgent):
    """Cycles through rock -> scissors -> paper."""
    
    def __init__(self):
        super().__init__("Reverse Cycle")
        self.cycle = ['rock', 'scissors', 'paper']
        self.index = 0
    
    def choose(self, history: List[Dict]) -> str:
        choice = self.cycle[self.index]
        self.index = (self.index + 1) % 3
        return choice
    
    def reset(self):
        super().reset()
        self.index = 0


class WinStayLoseShiftAgent(OpponentAgent):
    """
    Stays with winning move, shifts after losing.
    Classic psychological pattern.
    """
    
    def __init__(self, shift_type='sequential'):
        super().__init__(f"Win-Stay-Lose-Shift ({shift_type})")
        self.shift_type = shift_type
        self.last_choice = random.choice(['rock', 'paper', 'scissors'])
    
    def choose(self, history: List[Dict]) -> str:
        if not history:
            return self.last_choice
        
        last_game = history[-1]
        
        # If we won, stay with same move
        if last_game['result'] == 'player':
            self.last_choice = last_game['player']
            return self.last_choice
        
        # If we lost or tied, shift
        if self.shift_type == 'sequential':
            # Sequential shift: rock -> paper -> scissors -> rock
            sequence = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            self.last_choice = sequence[last_game['player']]
        elif self.shift_type == 'random':
            # Random shift to different move
            choices = ['rock', 'paper', 'scissors']
            choices.remove(last_game['player'])
            self.last_choice = random.choice(choices)
        else:
            # Counter shift: what would have won
            counter = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            if last_game['result'] == 'computer':
                self.last_choice = counter[last_game['computer']]
            else:  # tie
                self.last_choice = counter[last_game['player']]
        
        return self.last_choice
    
    def reset(self):
        super().reset()
        self.last_choice = random.choice(['rock', 'paper', 'scissors'])


class FrequencyBiasAgent(OpponentAgent):
    """Plays with a bias toward one choice (60-70% of the time)."""
    
    def __init__(self, favorite='rock', bias=0.65):
        super().__init__(f"Frequency Bias ({favorite} {int(bias*100)}%)")
        self.favorite = favorite
        self.bias = bias
        self.others = [c for c in ['rock', 'paper', 'scissors'] if c != favorite]
    
    def choose(self, history: List[Dict]) -> str:
        if random.random() < self.bias:
            return self.favorite
        else:
            return random.choice(self.others)


class AntiTripleAgent(OpponentAgent):
    """Avoids playing the same move 3 times in a row."""
    
    def __init__(self):
        super().__init__("Anti-Triple")
    
    def choose(self, history: List[Dict]) -> str:
        if len(history) < 2:
            return random.choice(['rock', 'paper', 'scissors'])
        
        last_two = [history[-2]['player'], history[-1]['player']]
        
        # If last two moves were the same, don't play that move
        if last_two[0] == last_two[1]:
            choices = ['rock', 'paper', 'scissors']
            choices.remove(last_two[0])
            return random.choice(choices)
        else:
            return random.choice(['rock', 'paper', 'scissors'])


class AlternatingAgent(OpponentAgent):
    """Alternates between two choices."""
    
    def __init__(self, choice1='rock', choice2='paper'):
        super().__init__(f"Alternating ({choice1}/{choice2})")
        self.choices = [choice1, choice2]
        self.index = 0
    
    def choose(self, history: List[Dict]) -> str:
        choice = self.choices[self.index]
        self.index = (self.index + 1) % 2
        return choice
    
    def reset(self):
        super().reset()
        self.index = 0


class CounterAIAgent(OpponentAgent):
    """
    Tries to counter predictable AI by playing what beats the expected AI counter.
    (Level-2 reasoning)
    """
    
    def __init__(self):
        super().__init__("Counter-AI")
        self.favorite = 'rock'  # Fake pattern
    
    def choose(self, history: List[Dict]) -> str:
        # Establish fake rock bias early
        if len(history) < 10:
            if random.random() < 0.7:
                return self.favorite
            else:
                return random.choice(['paper', 'scissors'])
        
        # Then counter the AI's expected counter
        # AI expects rock, will play paper, so we play scissors
        counter_moves = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        ai_expected_counter = counter_moves[self.favorite]
        our_counter = counter_moves[ai_expected_counter]
        
        # Play with 60% confidence
        if random.random() < 0.6:
            return our_counter
        else:
            return random.choice(['rock', 'paper', 'scissors'])


class MarkovAgent(OpponentAgent):
    """
    Uses simple Markov chain - next move depends on current move.
    E.g., after rock, always plays paper.
    """
    
    def __init__(self):
        super().__init__("Markov")
        self.transition = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        self.last_choice = random.choice(['rock', 'paper', 'scissors'])
    
    def choose(self, history: List[Dict]) -> str:
        if not history:
            return self.last_choice
        
        self.last_choice = self.transition[history[-1]['player']]
        return self.last_choice
    
    def reset(self):
        super().reset()
        self.last_choice = random.choice(['rock', 'paper', 'scissors'])


class MixedStrategyAgent(OpponentAgent):
    """
    Plays like a smart human - uses multiple strategies with some randomness.
    30% win-stay/lose-shift, 30% frequency bias, 40% random
    """
    
    def __init__(self):
        super().__init__("Mixed Strategy")
        self.favorite = random.choice(['rock', 'paper', 'scissors'])
        self.last_choice = self.favorite
    
    def choose(self, history: List[Dict]) -> str:
        strategy = random.random()
        
        # 30% Win-Stay-Lose-Shift
        if strategy < 0.3 and history:
            last_game = history[-1]
            if last_game['result'] == 'player':
                self.last_choice = last_game['player']
                return self.last_choice
            else:
                sequence = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                self.last_choice = sequence[last_game['player']]
                return self.last_choice
        
        # 30% Frequency Bias
        elif strategy < 0.6:
            if random.random() < 0.55:
                self.last_choice = self.favorite
                return self.last_choice
        
        # 40% Random
        self.last_choice = random.choice(['rock', 'paper', 'scissors'])
        return self.last_choice
    
    def reset(self):
        super().reset()
        self.favorite = random.choice(['rock', 'paper', 'scissors'])
        self.last_choice = self.favorite


# Create standard opponent suite
def get_opponent_suite() -> List[OpponentAgent]:
    """
    Get standard suite of opponents for testing.
    
    Returns:
        List of opponent agents representing different play styles.
    """
    return [
        # Fixed patterns (should be easiest to beat)
        AlwaysRockAgent(),
        AlwaysPaperAgent(),
        AlwaysScissorsAgent(),
        
        # Cycles (should be very predictable)
        CycleAgent(),
        ReverseCycleAgent(),
        
        # Psychological patterns (medium difficulty)
        WinStayLoseShiftAgent('sequential'),
        WinStayLoseShiftAgent('counter'),
        WinStayLoseShiftAgent('random'),
        
        # Frequency biases (medium difficulty)
        FrequencyBiasAgent('rock', 0.60),
        FrequencyBiasAgent('paper', 0.65),
        FrequencyBiasAgent('scissors', 0.70),
        
        # Pattern variations (medium-hard)
        AntiTripleAgent(),
        AlternatingAgent('rock', 'paper'),
        AlternatingAgent('paper', 'scissors'),
        MarkovAgent(),
        
        # Complex strategies (hardest)
        CounterAIAgent(),
        MixedStrategyAgent(),
        
        # Random (baseline - should be ~33% win rate)
        RandomAgent(),
    ]


def get_weighted_opponent_suite() -> List[tuple]:
    """
    Get opponent suite with weights for fitness calculation.
    
    More common/important patterns get higher weight.
    
    Returns:
        List of (agent, weight) tuples
    """
    return [
        # Fixed patterns (weight: 3) - common beginner mistakes
        (AlwaysRockAgent(), 3),
        (AlwaysPaperAgent(), 3),
        (AlwaysScissorsAgent(), 3),
        
        # Cycles (weight: 2) - common patterns
        (CycleAgent(), 2),
        (ReverseCycleAgent(), 2),
        
        # Psychological patterns (weight: 5) - very common in humans
        (WinStayLoseShiftAgent('sequential'), 5),
        (WinStayLoseShiftAgent('counter'), 4),
        (WinStayLoseShiftAgent('random'), 3),
        
        # Frequency biases (weight: 4) - very common
        (FrequencyBiasAgent('rock', 0.60), 4),
        (FrequencyBiasAgent('paper', 0.65), 4),
        (FrequencyBiasAgent('scissors', 0.70), 4),
        
        # Pattern variations (weight: 3)
        (AntiTripleAgent(), 3),
        (AlternatingAgent('rock', 'paper'), 2),
        (AlternatingAgent('paper', 'scissors'), 2),
        (MarkovAgent(), 3),
        
        # Complex strategies (weight: 4) - sophisticated players
        (CounterAIAgent(), 4),
        (MixedStrategyAgent(), 5),
        
        # Random (weight: 2) - baseline
        (RandomAgent(), 2),
    ]

