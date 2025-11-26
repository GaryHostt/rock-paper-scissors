"""
Hyperparameter Configuration for AI Difficulty Levels

This module defines all tunable hyperparameters for the AI strategies,
particularly for ai_very_hard where optimization is most beneficial.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
import json


@dataclass
class VeryHardHyperparameters:
    """
    Hyperparameters for ai_very_hard strategy.
    
    These values control the confidence levels and exploitation rates
    for various pattern detection strategies.
    """
    
    # Frequency Bias Detection
    strong_frequency_threshold: float = 0.60  # Threshold for "strong" frequency bias
    moderate_frequency_threshold: float = 0.50  # Threshold for "moderate" frequency
    weak_frequency_threshold: float = 0.42  # Threshold for "weak" frequency
    strong_frequency_confidence: float = 0.94  # Confidence when strong bias detected
    moderate_frequency_confidence: float = 0.84  # Confidence when moderate bias
    weak_frequency_confidence: float = 0.72  # Confidence when weak bias
    
    # Win-Stay Pattern Detection
    win_stay_threshold: float = 0.5  # Minimum rate to consider win-stay pattern
    win_stay_base_confidence: float = 0.70  # Base confidence for win-stay
    win_stay_confidence_scaling: float = 0.30  # Additional confidence per rate increase
    
    # Lose-Shift Pattern Detection
    lose_shift_threshold: float = 0.55  # Minimum rate to consider lose-shift pattern
    lose_shift_base_confidence: float = 0.68  # Base confidence for lose-shift
    lose_shift_confidence_scaling: float = 0.25  # Additional confidence per rate increase
    
    # Anti-Triple Pattern
    anti_triple_confidence: float = 0.74  # Confidence that player avoids triples
    
    # Cycle Detection
    cycle_3_confidence: float = 0.87  # Confidence for 3-length cycle detection
    cycle_2_confidence: float = 0.80  # Confidence for 2-length (alternating) cycle
    
    # Markov Chain Prediction
    markov_strong_threshold: float = 0.5  # High probability threshold
    markov_strong_base_confidence: float = 0.85  # Base confidence for strong Markov
    markov_strong_scaling: float = 0.2  # Scaling factor
    markov_moderate_threshold: float = 0.4  # Moderate probability threshold
    markov_moderate_base_confidence: float = 0.70  # Base for moderate Markov
    markov_moderate_scaling: float = 0.15  # Scaling factor
    
    # Opponent Modeling
    predictable_threshold: float = 0.3  # Randomness score for "predictable"
    predictable_confidence: float = 0.92  # Confidence when exploiting predictable
    random_threshold: float = 0.7  # Randomness score for "random"
    random_confidence: float = 0.40  # Confidence with random opponent (Nash)
    
    # Level-K Reasoning
    level_k_threshold: float = 0.4  # Frequency for counter-counter detection
    level_k_confidence: float = 0.78  # Confidence for level-3 reasoning
    sophistication_confidence: float = 0.45  # Confidence vs sophisticated player
    
    # Ensemble Voting System
    vote_bonus_per_predictor: float = 0.15  # Bonus for multiple predictors agreeing
    exploitation_very_high_threshold: float = 1.5  # Score threshold for very high confidence
    exploitation_very_high_rate: float = 0.96  # Exploitation rate
    exploitation_high_threshold: float = 1.0  # Score threshold for high confidence
    exploitation_high_rate: float = 0.88  # Exploitation rate
    exploitation_moderate_threshold: float = 0.7  # Score threshold for moderate
    exploitation_moderate_rate: float = 0.75  # Exploitation rate
    exploitation_low_threshold: float = 0.5  # Score threshold for low
    exploitation_low_rate: float = 0.60  # Exploitation rate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VeryHardHyperparameters':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def save(self, filepath: str):
        """Save hyperparameters to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'VeryHardHyperparameters':
        """Load hyperparameters from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def get_optimization_bounds(self) -> Dict[str, tuple]:
        """
        Get reasonable bounds for each hyperparameter for optimization.
        
        Returns dict mapping parameter name to (min, max) tuple.
        """
        return {
            # Frequency thresholds (0.3-0.8 range)
            'strong_frequency_threshold': (0.50, 0.75),
            'moderate_frequency_threshold': (0.40, 0.60),
            'weak_frequency_threshold': (0.35, 0.50),
            
            # Frequency confidences (0.6-0.99)
            'strong_frequency_confidence': (0.88, 0.98),
            'moderate_frequency_confidence': (0.75, 0.90),
            'weak_frequency_confidence': (0.65, 0.80),
            
            # Win-Stay (threshold 0.3-0.7, confidence 0.6-0.9)
            'win_stay_threshold': (0.35, 0.65),
            'win_stay_base_confidence': (0.60, 0.80),
            'win_stay_confidence_scaling': (0.20, 0.40),
            
            # Lose-Shift (threshold 0.4-0.7, confidence 0.6-0.85)
            'lose_shift_threshold': (0.45, 0.70),
            'lose_shift_base_confidence': (0.60, 0.78),
            'lose_shift_confidence_scaling': (0.20, 0.35),
            
            # Anti-Triple (0.6-0.85)
            'anti_triple_confidence': (0.65, 0.82),
            
            # Cycles (0.75-0.95)
            'cycle_3_confidence': (0.82, 0.92),
            'cycle_2_confidence': (0.72, 0.87),
            
            # Markov
            'markov_strong_threshold': (0.45, 0.60),
            'markov_strong_base_confidence': (0.80, 0.92),
            'markov_strong_scaling': (0.15, 0.30),
            'markov_moderate_threshold': (0.35, 0.50),
            'markov_moderate_base_confidence': (0.65, 0.78),
            'markov_moderate_scaling': (0.10, 0.20),
            
            # Opponent Modeling
            'predictable_threshold': (0.20, 0.40),
            'predictable_confidence': (0.88, 0.96),
            'random_threshold': (0.65, 0.80),
            'random_confidence': (0.33, 0.50),
            
            # Level-K
            'level_k_threshold': (0.35, 0.50),
            'level_k_confidence': (0.70, 0.85),
            'sophistication_confidence': (0.35, 0.55),
            
            # Ensemble
            'vote_bonus_per_predictor': (0.10, 0.25),
            'exploitation_very_high_threshold': (1.3, 1.8),
            'exploitation_very_high_rate': (0.93, 0.98),
            'exploitation_high_threshold': (0.8, 1.2),
            'exploitation_high_rate': (0.83, 0.93),
            'exploitation_moderate_threshold': (0.5, 0.9),
            'exploitation_moderate_rate': (0.68, 0.82),
            'exploitation_low_threshold': (0.3, 0.6),
            'exploitation_low_rate': (0.50, 0.70),
        }


@dataclass
class HardHyperparameters:
    """
    Hyperparameters for ai_hard strategy.
    
    These are simpler than VeryHard but can still benefit from optimization.
    """
    
    # Frequency Bias
    strong_frequency_threshold: float = 0.55
    strong_frequency_rate: float = 0.87
    moderate_frequency_threshold: float = 0.45
    moderate_frequency_rate: float = 0.76
    
    # Win-Stay
    win_stay_threshold: float = 0.4
    win_stay_confidence: float = 0.73
    
    # Lose-Shift
    lose_shift_threshold: float = 0.5
    lose_shift_confidence: float = 0.66
    
    # Anti-Triple
    anti_triple_confidence: float = 0.69
    
    # Cycle
    cycle_confidence: float = 0.62
    
    # General Frequency
    general_frequency_confidence: float = 0.58
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HardHyperparameters':
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# Default instances
DEFAULT_VERY_HARD_PARAMS = VeryHardHyperparameters()
DEFAULT_HARD_PARAMS = HardHyperparameters()

