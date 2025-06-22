# // <copyright file="RpgExample.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import time
import os
import pygame
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.StepMode import StepMode
from MountainGoapLogging.DefaultLogger import DefaultLogger

from Examples.RpgExample.PlayerFactory import PlayerFactory
from Examples.RpgExample.RpgMonsterFactory import RpgMonsterFactory
from Examples.RpgExample.RpgUtils import Vector2

# Pygame constants
CELL_SIZE = 30
WIDTH = 20 * CELL_SIZE
HEIGHT = 20 * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class RpgExampleComparativePygame:
    """
    RPG example demo.
    """

    MaxX: int = 20

    MaxY: int = 20

    @staticmethod
    def run() -> None:
        _ = DefaultLogger(log_to_console=False, logging_file="rpg-example.log")
        
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG GOAP Example")
        clock = pygame.time.Clock()
        
        _random = random.Random() # Instance of Random
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = PlayerFactory.create(agents, food_positions)
        agents.append(player)

        # Create food positions
        for _ in range(20):
            food_positions.append(Vector2(_random.randint(0, RpgExampleComparativePygame.MaxX - 1), _random.randint(0, RpgExampleComparativePygame.MaxY - 1)))
        
        # Create monsters
        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(_random.randint(0, RpgExampleComparativePygame.MaxX - 1), _random.randint(0, RpgExampleComparativePygame.MaxY - 1))
            agents.append(monster)
        
        # Game loop
        running = True
        turn = 0
        last_update = pygame.time.get_ticks()
        
        while running and turn < 600:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update game state every 200ms
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 200:
                turn += 1
                print(f"--- Turn {turn} ---")
                
                for agent in agents:
                    agent.step(mode=StepMode.OneAction) # Each agent executes one action
                
                RpgExampleComparativePygame._process_deaths(agents)
                last_update = current_time

                # Check if player is still alive
                if player not in agents:
                    print("Player defeated! Game Over.")
                    break
                # Check if all monsters are defeated (goal met for player)
                monsters_alive = [a for a in agents if a.State.get("faction") == "enemy"]
            
            # Render
            RpgExampleComparativePygame._render_grid(screen, agents, food_positions)
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
            
        print("Game finished.")
        pygame.quit()

    @staticmethod
    def _render_grid(screen: pygame.Surface, agents: List[Agent], food_positions: List[Vector2]) -> None:
        # Clear screen
        screen.fill(BLACK)
        
        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

        # Draw food
        for pos in food_positions:
            if 0 <= pos.X < RpgExampleComparativePygame.MaxX and 0 <= pos.Y < RpgExampleComparativePygame.MaxY:
                rect = pygame.Rect(int(pos.X) * CELL_SIZE + 2, int(pos.Y) * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                pygame.draw.ellipse(screen, YELLOW, rect)

        # Draw agents
        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")
            
            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < RpgExampleComparativePygame.MaxX and 0 <= agent_pos.Y < RpgExampleComparativePygame.MaxY:
                    rect = pygame.Rect(int(agent_pos.X) * CELL_SIZE + 2, int(agent_pos.Y) * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                    
                    if agent_faction == "player":
                        # Red if health below 30, otherwise blue
                        agent_hp = agent.State.get("hp")
                        color = RED if isinstance(agent_hp, int) and agent_hp < 30 else BLUE
                        pygame.draw.rect(screen, color, rect)
                    else: # Monster
                        pygame.draw.rect(screen, GREEN, rect)

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
    RpgExampleComparativePygame.run()

