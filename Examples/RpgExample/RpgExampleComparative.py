# // <copyright file="RpgExample.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import time
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.StepMode import StepMode
from MountainGoapLogging.DefaultLogger import DefaultLogger

from Examples.RpgExample.PlayerFactory import PlayerFactory
from Examples.RpgExample.RpgMonsterFactory import RpgMonsterFactory
from Examples.RpgExample.RpgUtils import Vector2

# A helper function to clear the console (platform dependent)
def clear_console():
    # pass
    os.system('cls' if os.name == 'nt' else 'clear')

class RpgExampleComparative:
    """
    RPG example demo.
    """

    MaxX: int = 20

    MaxY: int = 20

    @staticmethod
    def run() -> None:
        _ = DefaultLogger(log_to_console=False, logging_file="rpg-example.log")
        
        _random = random.Random() # Instance of Random
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = PlayerFactory.create(agents, food_positions)
        agents.append(player)

        # Create food positions
        for _ in range(20):
            food_positions.append(Vector2(_random.randint(0, RpgExampleComparative.MaxX - 1), _random.randint(0, RpgExampleComparative.MaxY - 1)))
        
        # Create monsters
        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(_random.randint(0, RpgExampleComparative.MaxX - 1), _random.randint(0, RpgExampleComparative.MaxY - 1))
            agents.append(monster)
        
        # Game loop
        for i in range(600): # 600 steps, each 200ms -> 120 seconds = 2 minutes
            print(f"--- Turn {i+1} ---")
            for agent in agents:
                agent.step(mode=StepMode.OneAction) # Each agent executes one action
            
            RpgExampleComparative._process_deaths(agents)
            RpgExampleComparative._print_grid(agents, food_positions)
            time.sleep(0.2) # 200ms delay

            # Check if player is still alive
            if player not in agents:
                print("Player defeated! Game Over.")
                break
            # Check if all monsters are defeated (goal met for player)
            monsters_alive = [a for a in agents if a.State.get("faction") == "enemy"]
            
        print("Game finished.")

    @staticmethod
    def _print_grid(agents: List[Agent], food_positions: List[Vector2]) -> None:
        clear_console() # Clear screen before printing new frame
        
        grid: List[List[str]] = [[" " for _ in range(RpgExampleComparative.MaxY)] for _ in range(RpgExampleComparative.MaxX)]

        for pos in food_positions:
            if 0 <= pos.X < RpgExampleComparative.MaxX and 0 <= pos.Y < RpgExampleComparative.MaxY:
                grid[int(pos.X)][int(pos.Y)] = "f"

        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")
            
            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < RpgExampleComparative.MaxX and 0 <= agent_pos.Y < RpgExampleComparative.MaxY:
                    if agent_faction == "player":
                        # Show % if health below 30, otherwise @
                        agent_hp = agent.State.get("hp")
                        if isinstance(agent_hp, int) and agent_hp < 30:
                            grid[int(agent_pos.X)][int(agent_pos.Y)] = "%"
                        else:
                            grid[int(agent_pos.X)][int(agent_pos.Y)] = "@"
                    else: # Monster
                        grid[int(agent_pos.X)][int(agent_pos.Y)] = "g"
        
        for row in grid:
            print("".join(row))

    @staticmethod
    def _process_deaths(agents: List[Agent]) -> None:
        cull_list: List[Agent] = []
        for agent in agents:
            hp = agent.State.get("hp")
            if isinstance(hp, int) and hp <= 0:
                cull_list.append(agent)
        
        for agent_to_remove in cull_list:
            agents.remove(agent_to_remove)
            print(f"Agent {agent_to_remove.Name} has died.")


if __name__ == "__main__":
    RpgExampleComparative.run()

