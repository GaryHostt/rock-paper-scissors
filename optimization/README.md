# Hyperparameter Optimization Package

This package provides a complete framework for optimizing the hyperparameters of the Rock Paper Scissors AI strategies through simulation-based optimization.

## Quick Start

### Run Basic Optimization

```bash
# Quick test (30 iterations, ~1 minute)
python optimization/run_optimization.py --method random --iterations 30 --rounds 50

# Full optimization (200 iterations, ~5 minutes)
python optimization/run_optimization.py --method annealing --iterations 200 --rounds 100

# Compare both methods
python optimization/run_optimization.py --method both --iterations 100
```

### Results

Optimization results are saved to `optimization/results/`:
- `random_search_best.json` - Best parameters from random search
- `simulated_annealing_best.json` - Best parameters from simulated annealing

## Package Structure

```
optimization/
├── __init__.py              # Package exports
├── hyperparameters.py       # Hyperparameter definitions
├── opponent_agents.py       # Simulated opponent implementations
├── ai_strategies.py         # Parameterized AI strategy functions
├── optimizer.py             # Optimization algorithms and evaluation
├── run_optimization.py      # CLI runner script
└── results/                 # Output directory for optimization results
```

## Modules

### `hyperparameters.py`

Defines hyperparameter configurations for AI strategies:

```python
from optimization.hyperparameters import VeryHardHyperparameters, DEFAULT_VERY_HARD_PARAMS

# Create custom parameters
params = VeryHardHyperparameters(
    strong_frequency_threshold=0.55,
    win_stay_base_confidence=0.75
)

# Save/load parameters
params.save('my_params.json')
loaded = VeryHardHyperparameters.load('my_params.json')

# Get optimization bounds
bounds = params.get_optimization_bounds()
```

**Key Classes:**
- `VeryHardHyperparameters` - 41 parameters for ai_very_hard
- `HardHyperparameters` - Simpler parameters for ai_hard

### `opponent_agents.py`

Simulated opponent agents for testing:

```python
from optimization.opponent_agents import *

# Get all opponents
opponents = get_opponent_suite()  # Returns 18 agents

# Get weighted opponents for fitness calculation
weighted = get_weighted_opponent_suite()  # Returns (agent, weight) tuples

# Use individual agents
agent = WinStayLoseShiftAgent('sequential')
history = []
choice = agent.choose(history)
```

**Available Agents:**
- **Fixed:** AlwaysRock, AlwaysPaper, AlwaysScissors
- **Cycles:** Cycle, ReverseCycle
- **Psychological:** WinStayLoseShift (3 variants)
- **Frequency:** FrequencyBias (3 variants with different biases)
- **Complex:** CounterAI, MixedStrategy, Markov
- **Pattern:** AntiTriple, Alternating (2 variants)
- **Baseline:** Random

### `ai_strategies.py`

Parameterized AI strategy functions:

```python
from optimization.ai_strategies import ai_very_hard_parameterized
from optimization.hyperparameters import DEFAULT_VERY_HARD_PARAMS

history = [...]  # Game history
params = DEFAULT_VERY_HARD_PARAMS

move = ai_very_hard_parameterized(history, params)
```

This is the same logic as `ai_very_hard` in `app.py` but accepts parameters.

### `optimizer.py`

Optimization framework and algorithms:

```python
from optimization.optimizer import *
from optimization.ai_strategies import ai_very_hard_parameterized
from optimization.hyperparameters import DEFAULT_VERY_HARD_PARAMS

# Create fitness evaluator
evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=100)

# Evaluate baseline
fitness = evaluator.evaluate(DEFAULT_VERY_HARD_PARAMS, verbose=True)

# Run random search
optimizer = RandomSearchOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
best_params, best_fitness = optimizer.optimize(iterations=50)

# Run simulated annealing
optimizer = SimulatedAnnealingOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
best_params, best_fitness = optimizer.optimize(iterations=100, initial_temp=10.0)

# Save results
save_optimization_results(best_params, best_fitness, 'random_search', 'results.json')
```

**Key Classes:**
- `SimulationEngine` - Runs games between AI and opponents
- `FitnessEvaluator` - Evaluates hyperparameter configurations
- `RandomSearchOptimizer` - Random search algorithm
- `SimulatedAnnealingOptimizer` - Simulated annealing algorithm

## Usage Examples

### Example 1: Evaluate Custom Parameters

```python
from optimization import *

# Create custom parameters
params = VeryHardHyperparameters(
    strong_frequency_threshold=0.50,
    strong_frequency_confidence=0.95,
    win_stay_base_confidence=0.80
)

# Evaluate
evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=100)
fitness = evaluator.evaluate(params, verbose=True)

print(f"Fitness: {fitness:.2f}")
```

### Example 2: Custom Optimization

```python
from optimization import *

# Setup
evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=50)
optimizer = RandomSearchOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)

# Run optimization
best_params, best_fitness = optimizer.optimize(iterations=100, verbose=True)

# Save results
save_optimization_results(
    best_params, 
    best_fitness, 
    'custom_optimization',
    'optimization/results/custom_best.json'
)

print(f"\nBest fitness: {best_fitness:.2f}")
print(f"Best threshold: {best_params.strong_frequency_threshold:.3f}")
```

### Example 3: Compare Algorithms

```python
from optimization import *

evaluator = FitnessEvaluator(ai_very_hard_parameterized, rounds_per_opponent=100)

# Random search
rs_optimizer = RandomSearchOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
rs_params, rs_fitness = rs_optimizer.optimize(iterations=50)

# Simulated annealing
sa_optimizer = SimulatedAnnealingOptimizer(evaluator, DEFAULT_VERY_HARD_PARAMS)
sa_params, sa_fitness = sa_optimizer.optimize(iterations=50)

print(f"Random Search: {rs_fitness:.2f}")
print(f"Simulated Annealing: {sa_fitness:.2f}")

if sa_fitness > rs_fitness:
    print("Simulated Annealing won!")
    best = sa_params
else:
    print("Random Search won!")
    best = rs_params
```

### Example 4: Test Against Specific Opponent

```python
from optimization import *

# Create opponent
opponent = WinStayLoseShiftAgent('sequential')

# Create engine
engine = SimulationEngine(ai_very_hard_parameterized)

# Run game
params = DEFAULT_VERY_HARD_PARAMS
result = engine.run_game(opponent, params, num_rounds=1000)

print(f"Win rate: {result['win_rate']*100:.1f}%")
print(f"Wins: {result['wins']}, Losses: {result['losses']}, Ties: {result['ties']}")
```

## Command-Line Interface

The `run_optimization.py` script provides a complete CLI:

```bash
python optimization/run_optimization.py --help
```

**Options:**
- `--method {random,annealing,both}` - Optimization method
- `--iterations N` - Number of iterations (default: 50)
- `--rounds N` - Rounds per opponent (default: 100)
- `--skip-baseline` - Skip baseline evaluation

**Examples:**

```bash
# Quick test
python optimization/run_optimization.py --method random --iterations 20 --rounds 30

# Production optimization
python optimization/run_optimization.py --method annealing --iterations 300 --rounds 200

# Compare methods
python optimization/run_optimization.py --method both --iterations 100 --rounds 100
```

## Performance

**Computational Cost:**
- **Per evaluation:** ~0.5 seconds (18 opponents × 100 rounds)
- **Random search (100 iter):** ~1-2 minutes
- **Simulated annealing (200 iter):** ~3-5 minutes

**Memory Usage:**
- Minimal (< 100MB)
- No large data structures stored
- History tracked per game only

## Optimization Results

### Baseline (Default Parameters)
- **Fitness:** 57.76
- **Weighted Win Rate:** 60.16%

### Optimized (Random Search, 30 iterations)
- **Fitness:** 63.66 (+10.2%)
- **Weighted Win Rate:** Higher across all categories
- **Time:** < 1 minute

See [HYPERPARAMETER_OPTIMIZATION.md](../docs/HYPERPARAMETER_OPTIMIZATION.md) for detailed results.

## Extending the System

### Add New Opponent Agent

```python
# In opponent_agents.py
class MyNewAgent(OpponentAgent):
    def __init__(self):
        super().__init__("My New Agent")
    
    def choose(self, history):
        # Your logic here
        return 'rock'  # or 'paper' or 'scissors'

# Add to suite in get_opponent_suite()
def get_opponent_suite():
    return [
        # ... existing agents ...
        MyNewAgent(),
    ]
```

### Add New Hyperparameters

```python
# In hyperparameters.py
@dataclass
class VeryHardHyperparameters:
    # ... existing parameters ...
    my_new_param: float = 0.5
    
    def get_optimization_bounds(self):
        return {
            # ... existing bounds ...
            'my_new_param': (0.3, 0.7),
        }

# Use in ai_strategies.py
def ai_very_hard_parameterized(history, params):
    # ... existing logic ...
    if some_condition:
        confidence = params.my_new_param  # Use new parameter
```

### Add New Optimization Algorithm

```python
# In optimizer.py
class GeneticAlgorithmOptimizer:
    def __init__(self, evaluator, params_template):
        self.evaluator = evaluator
        self.params_template = params_template
        self.population = []
    
    def optimize(self, iterations, population_size=50):
        # Initialize population
        # Evaluate fitness
        # Selection, crossover, mutation
        # Return best individual
        pass
```

## Testing

Run tests to verify the optimization system:

```bash
# Test imports
python -c "from optimization import *; print('✓ All imports successful')"

# Test opponent agents
python -c "from optimization import get_opponent_suite; agents = get_opponent_suite(); print(f'✓ {len(agents)} agents loaded')"

# Test evaluation
python -c "from optimization import *; evaluator = FitnessEvaluator(ai_very_hard_parameterized, 10); fitness = evaluator.evaluate(DEFAULT_VERY_HARD_PARAMS); print(f'✓ Fitness: {fitness:.2f}')"

# Test optimization (quick)
python optimization/run_optimization.py --method random --iterations 5 --rounds 10 --skip-baseline
```

## Troubleshooting

### Issue: Optimization is slow

**Solutions:**
- Reduce `--rounds` per opponent (e.g., 50 instead of 100)
- Reduce `--iterations` (e.g., 30 instead of 100)
- Use `--method random` instead of `annealing` for faster results
- Remove less important opponents from the suite

### Issue: Fitness scores seem wrong

**Check:**
- Verify opponent agents are working correctly
- Ensure game history is being tracked properly
- Check that parameters are within valid bounds
- Compare against baseline evaluation

### Issue: Parameters don't improve

**Try:**
- Run more iterations
- Try different optimization method
- Check if parameter bounds are too restrictive
- Verify fitness function is correct

## References

- **Full Documentation:** [HYPERPARAMETER_OPTIMIZATION.md](../docs/HYPERPARAMETER_OPTIMIZATION.md)
- **Code Refactoring:** [CODE_REFACTORING.md](../docs/CODE_REFACTORING.md)
- **AI Strategies:** [STRATEGIES.md](../docs/STRATEGIES.md)
- **Main Application:** [../app.py](../app.py)

## License

Part of the Rock Paper Scissors AI project.

