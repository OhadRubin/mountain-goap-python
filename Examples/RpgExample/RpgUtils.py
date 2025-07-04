# // <copyright file="RpgUtils.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import math
from typing import List, Any, Optional, Dict, TYPE_CHECKING

# Assuming MountainGoap is available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action

if TYPE_CHECKING:
    from MountainGoap.Internals.ActionNode import ActionNode # For type hints in cost callbacks

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

# C# `System.Numerics.Vector2` equivalent for this example
class Vector2:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.X == other.X and self.Y == other.Y

    def __hash__(self) -> int:
        return hash((self.X, self.Y))
    
    def __repr__(self) -> str:
        return f"Vector2({self.X}, {self.Y})"

class RpgUtils:
    """
    Utility classes for the RPG example.
    """

    @staticmethod
    def in_distance(pos1: Vector2, pos2: Vector2, max_distance: float) -> bool:
        """
        Checks if two positions are within a certain distance of one another.
        """
        distance = RpgUtils._distance(pos1, pos2)
        return distance <= max_distance

    @staticmethod
    def get_enemy_in_range(source: Agent, agents: List[Agent], distance: float) -> Optional[Agent]:
        """
        Gets an enemy within a given range of a source agent.
        """
        for agent in agents:
            if agent == source:
                continue
            
            # Type checking and access values
            source_pos = source.State.get("position")
            agent_pos = agent.State.get("position")
            source_faction = source.State.get("faction")
            agent_faction = agent.State.get("faction")

            if isinstance(source_pos, Vector2) and \
               isinstance(agent_pos, Vector2) and \
               isinstance(source_faction, str) and \
               isinstance(agent_faction, str) and \
               RpgUtils.in_distance(source_pos, agent_pos, distance) and \
               source_faction != agent_faction:
                return agent
        return None

    @staticmethod
    def move_towards_other_position(pos1: Vector2, pos2: Vector2) -> Vector2:
        """
        Moves a position towards another position one space and returns the result.
        This is a simple Manhattan-like move.
        """
        new_pos = Vector2(pos1.X, pos1.Y) # Create a copy to modify
        
        x_diff = pos2.X - new_pos.X
        y_diff = pos2.Y - new_pos.Y

        x_sign = 0
        if x_diff > 0: x_sign = 1
        elif x_diff < 0: x_sign = -1

        y_sign = 0
        if y_diff > 0: y_sign = 1
        elif y_diff < 0: y_sign = -1
        
        # C# Math.Sign behavior
        # `if (xSign != 0) pos1.X += xSign; else pos1.Y += ySign;`
        # This means it prioritizes X movement, and only moves Y if X is aligned.
        if x_sign != 0:
            new_pos.X += x_sign
        elif y_sign != 0: # Only if x_sign is 0, move in Y direction
            new_pos.Y += y_sign
        
        return new_pos

    @staticmethod
    def enemy_permutations(state: StateDictionary) -> List[Any]:
        """
        Permutation selector to grab all enemies.
        """
        enemies: List[Any] = []
        
        agents_list = state.get("agents")
        agent_faction = state.get("faction")

        if not isinstance(agents_list, list) or \
           not all(isinstance(a, Agent) for a in agents_list) or \
           not isinstance(agent_faction, str):
            return enemies
        
        # Filter agents that are not in the same faction as the current agent
        for agent in agents_list:
            if isinstance(agent.State.get("faction"), str) and agent.State["faction"] != agent_faction:
                enemies.append(agent)
        return enemies

    @staticmethod
    def food_permutations(state: StateDictionary) -> List[Any]:
        """
        Permutation selector to grab all food positions.
        """
        food_positions: List[Any] = []
        
        source_positions = state.get("foodPositions")
        
        if not isinstance(source_positions, list) or \
           not all(isinstance(p, Vector2) for p in source_positions):
            return food_positions
        
        # Copy elements from sourcePositions to foodPositions (list copy)
        food_positions.extend(source_positions)
        return food_positions

    @staticmethod
    def starting_position_permutations(state: StateDictionary) -> List[Any]:
        """
        Gets a list of all possible starting positions for a move action.
        """
        starting_positions: List[Any] = []
        position = state.get("position")
        
        if not isinstance(position, Vector2):
            return starting_positions
        
        starting_positions.append(position)
        return starting_positions

    @staticmethod
    def go_to_enemy_cost(action: Action, state: StateDictionary) -> float:
        """
        Gets the cost of moving to an enemy.
        """
        starting_position = action.get_parameter("startingPosition")
        target_agent = action.get_parameter("target")

        if not isinstance(starting_position, Vector2) or \
           not isinstance(target_agent, Agent):
            return float('inf') # float.MaxValue in C#
        
        target_position = target_agent.State.get("position")

        if not isinstance(target_position, Vector2):
            return float('inf')
        
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def go_to_food_cost(action: Action, state: StateDictionary) -> float:
        """
        Gets the cost of moving to food.
        """
        starting_position = action.get_parameter("startingPosition")
        target_position = action.get_parameter("target")

        if not isinstance(starting_position, Vector2) or \
           not isinstance(target_position, Vector2):
            return float('inf') # float.MaxValue in C#
        
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def _distance(pos1: Vector2, pos2: Vector2) -> float:
        """
        Calculates the Euclidean distance between two Vector2 positions.
        """
        return math.sqrt(math.pow(abs(pos2.X - pos1.X), 2) + math.pow(abs(pos2.Y - pos1.Y), 2))

