# Mountain GOAP Python

This repository demonstrates a Goal-Oriented Action Planning (GOAP) engine and an RPG example built with it.  The code has been organized into logical packages:

- **goap** – core planning engine
  - `types.py` – shared type aliases and callback definitions
  - `utils.py` – priority queue, dictionary helpers and common utility functions
  - `goals.py` – classes representing different goal types
  - `sensors.py` – sensor abstraction for agents
  - `actions.py` – step modes and the `Action` class
  - `planning.py` – `ActionNode`, `ActionGraph` and the planner implementation
  - `agent.py` – the `Agent` class itself
- **rpg** – utilities and factories for the RPG demo
  - `utils.py` – vector math and helper functions
  - `factories.py` – common handlers and character factories
  - `example.py` – pygame loop that runs the sample game

The entry point `goal_single_file.py` imports the packages and launches the example if run directly.

