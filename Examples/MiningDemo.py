# // <copyright file="MiningDemo.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import time
from typing import Dict, Any, Optional, List

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ExtremeGoal import ExtremeGoal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.StepMode import StepMode
from MountainGoapLogging.DefaultLogger import DefaultLogger

class MiningDemo:
    """
    GOAP Mining Demo - Shows competing goals and dynamic priority switching.
    """

    # World layout indices
    SMELTER_INDEX = 0
    MINE_INDEX = 4
    HOSPITAL_INDEX = 7

    LOCATIONS = [
        "smelter", "road", "road", "road",
        "mine shaft", "road", "road", "hospital"
    ]

    @staticmethod
    def run() -> None:
        _ = DefaultLogger(log_to_console=False)  # Disable logging for cleaner output
        
        rnd = random.Random()

        # ---------- initial agent state ----------
        state = {
            "position": MiningDemo.MINE_INDEX,
            "health": 10,
            "ore_count": 0,
            "gold_count": 0,
        }

        # ---------- goals (2 competing goals) ----------
        stay_alive = ComparativeGoal(
            name="Stay Alive",
            desired_state={
                "health": ComparisonValuePair(
                    value=3, 
                    operator=ComparisonOperator.GreaterThanOrEquals
                )
            },
            weight=10.0  # Higher priority
        )

        get_gold = ExtremeGoal(
            name="Get Gold",
            desired_state={
                "gold_count": True
            },
            weight=5.0  # Lower priority
        )

        # ---------- actions (multiple paths to each goal) ----------
        
        # Step-by-step movement actions
        move_left = Action(
            name="Move Left",
            executor=MiningDemo._move_left_executor,
            # TODO: implement
            cost=1.0
        )

        move_right = Action(
            name="Move Right",
            executor=MiningDemo._move_right_executor,
            # TODO: implement
            cost=1.0
        )

        # Work actions
        mine_ore = Action(
            name="Mine Ore",
            executor=MiningDemo._mine_ore_executor,
            # TODO: implement
            cost=2.0
        )

        smelt_gold = Action(
            name="Smelt Gold",
            executor=MiningDemo._smelt_gold_executor,
            # TODO: implement
            cost=1.0
        )

        heal = Action(
            name="Get Medical Treatment",
            executor=MiningDemo._heal_executor,
            # TODO: implement
            cost=1.0
        )

        # ---------- sensors ----------
        health_monitor = Sensor(
            lambda agent: MiningDemo._health_monitor_sensor(agent, rnd),
            "Health Monitor"
        )


        # ---------- build agent ----------
        agent = Agent(
            name="Miner",
            state=state,
            goals=[stay_alive, get_gold],
            actions=[move_left, move_right, mine_ore, smelt_gold, heal],
            sensors=[health_monitor
                     ]
        )

        # ---------- simulation loop ----------
        turn = 0
        while agent.State.get("health", 0) > 0 and turn < 50:
            MiningDemo._write_status(turn, agent)
            agent.step(mode=StepMode.OneAction)
            turn += 1
            time.sleep(0.8)  # Slow down to see movement

        print("\n🏁 Simulation ended.")

    @staticmethod
    def _move_left_executor(agent: Agent, action: Action) -> ExecutionStatus:
        
        return ExecutionStatus.Succeeded

    @staticmethod
    def _move_right_executor(agent: Agent, action: Action) -> ExecutionStatus:
        # TODO: implement
        return ExecutionStatus.Succeeded

    @staticmethod
    def _mine_ore_executor(agent: Agent, action: Action) -> ExecutionStatus:
        # TODO: implement
        return ExecutionStatus.Succeeded

    @staticmethod
    def _smelt_gold_executor(agent: Agent, action: Action) -> ExecutionStatus:
        # TODO: implement
        return ExecutionStatus.Succeeded

    @staticmethod
    def _heal_executor(agent: Agent, action: Action) -> ExecutionStatus:
        # TODO: implement
        return ExecutionStatus.Succeeded

    @staticmethod
    def _health_monitor_sensor(agent: Agent, rnd: random.Random) -> None:
        # Random damage
        if rnd.random() < 0.15:
            hp = agent.State.get("health", 10)
            if isinstance(hp, int):
                new_hp = max(0, hp - 1)
                agent.State["health"] = new_hp
                print(f"💔 Took damage! Health: {new_hp}")


    @staticmethod
    def _write_status(turn: int, agent: Agent) -> None:

        # Display world visualization
        world_view = []
        for i in range(len(MiningDemo.LOCATIONS)):
            location_char = {
                "smelter": "S",
                "mine shaft": "M",
                "hospital": "H",
                "road": "R"
            }.get(MiningDemo.LOCATIONS[i], MiningDemo.LOCATIONS[i][0].upper())

            if i == pos:
                world_view.append(f"[{location_char}*]")  # Agent position
            else:
                world_view.append(f"[{location_char}]")

        print(f"T{turn:2} | {'-'.join(world_view)}")
        
        print()


if __name__ == "__main__":
    MiningDemo.run()