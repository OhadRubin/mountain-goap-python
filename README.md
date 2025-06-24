# Mountain GOAP Python

This repository demonstrates a Goal-Oriented Action Planning (GOAP) engine and an RPG example built with it.  The code has been organized into logical packages:

- **goap_python** – core planning engine
  - `types.py` – shared type aliases and callback definitions
  - `utils.py` – priority queue, dictionary helpers and common utility functions
  - `goals.py` – classes representing different goal types
  - `sensors.py` – sensor abstraction for agents
  - `actions.py` – step modes and the `Action` class
  - `planning.py` – `ActionNode`, `ActionGraph` and the planner implementation
  - `agent.py` – the `Agent` class itself
- **rpg_goap_python_example** – utilities and factories for the RPG demo
  - `utils.py` – vector math and helper functions
  - `factories.py` – common handlers and character factories
  - `example.py` – pygame loop that runs the sample game

## Setup

### Prerequisites
- Python 3.7 or higher
- pygame for the visual RPG example

### Quick Setup
Run the setup script to install dependencies:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
If you prefer to set up manually:
```bash
# Install pygame
pip install --break-system-packages pygame>=2.0.0
# or use pip install pygame>=2.0.0 if you have a virtual environment
```

## Running the Examples

### RPG Example
Run the interactive RPG example:
```bash
./run.sh
```

Or run it directly:
```bash
python -m rpg_goap_python_example.example
```

### Test with Timeout
To test the example runs successfully:
```bash
timeout 10 python -m rpg_goap_python_example.example
```

The RPG example demonstrates:
- Goal-oriented planning with multiple agents
- Combat system where player fights monsters
- Food collection and consumption
- Autonomous AI behavior using GOAP principles

The player agent will automatically fight monsters and collect food based on its programmed goals and the current game state.

