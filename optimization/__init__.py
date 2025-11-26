"""
Optimization Package for RPS AI Hyperparameter Tuning
"""

from optimization.hyperparameters import (
    VeryHardHyperparameters,
    HardHyperparameters,
    DEFAULT_VERY_HARD_PARAMS,
    DEFAULT_HARD_PARAMS
)

from optimization.opponent_agents import (
    OpponentAgent,
    RandomAgent,
    AlwaysRockAgent,
    WinStayLoseShiftAgent,
    FrequencyBiasAgent,
    get_opponent_suite,
    get_weighted_opponent_suite
)

from optimization.optimizer import (
    SimulationEngine,
    FitnessEvaluator,
    RandomSearchOptimizer,
    SimulatedAnnealingOptimizer,
    save_optimization_results
)

__all__ = [
    'VeryHardHyperparameters',
    'HardHyperparameters',
    'DEFAULT_VERY_HARD_PARAMS',
    'DEFAULT_HARD_PARAMS',
    'OpponentAgent',
    'get_opponent_suite',
    'get_weighted_opponent_suite',
    'SimulationEngine',
    'FitnessEvaluator',
    'RandomSearchOptimizer',
    'SimulatedAnnealingOptimizer',
    'save_optimization_results'
]

