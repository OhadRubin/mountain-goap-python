import random
from typing import List, Dict, Any, Optional

import goap.actions
import goap.agent
import goap.sensors
import goap.goals
from goap.types import StateDictionary
from rpg.utils import Vector2, RpgUtils, MaxX, MaxY

# Aliases for convenience
Action = goap.actions.Action
Agent = goap.agent.Agent
Sensor = goap.sensors.Sensor
StepMode = goap.actions.StepMode
Goal = goap.goals.Goal
ComparativeGoal = goap.goals.ComparativeGoal
ExtremeGoal = goap.goals.ExtremeGoal
ComparisonOperator = goap.goals.ComparisonOperator
ComparisonValuePair = goap.goals.ComparisonValuePair
ExecutionStatus = goap.actions.ExecutionStatus

class CommonRpgAgentHandlers:
    _rng = random.Random()

    @staticmethod
    def _get_food_in_range(
        source: Vector2, food_positions: List[Vector2], range_val: float
    ) -> Optional[Vector2]:
        for position in food_positions:
            if RpgUtils.in_distance(source, position, range_val):
                return position
        return None

    @staticmethod
    def see_enemies_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                sight_range = agent_instance.State.get(
                    "sight_range", 10.0
                )  # Use agent-specific sight range
                enemy_in_range = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, sight_range
                )
                agent_instance.State["canSeeEnemies"] = enemy_in_range is not None

    @staticmethod
    def enemy_proximity_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                enemy_in_range = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, 1.0
                )
                agent_instance.State["nearEnemy"] = enemy_in_range is not None

    @staticmethod
    def kill_nearby_enemy_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                target_enemy = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, 1.0
                )
                if target_enemy is not None:
                    with target_enemy._lock:
                        current_hp = target_enemy.State.get("hp")
                        if isinstance(current_hp, int):
                            current_hp -= 1
                            target_enemy.State["hp"] = current_hp
                            print(
                                f"{agent_instance.Name} attacked {target_enemy.Name}. {target_enemy.Name} HP: {current_hp}"
                            )
                            if current_hp <= 0:
                                print(f"{target_enemy.Name} defeated!")
                                return ExecutionStatus.Succeeded
            return ExecutionStatus.Failed

    @staticmethod
    def go_to_enemy_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        with agent_instance._lock:
            target_agent = action_instance.get_parameter("target")
            agent_position = agent_instance.State.get("position")
            if not isinstance(target_agent, Agent) or not isinstance(
                agent_position, Vector2
            ):
                return ExecutionStatus.Failed
            with target_agent._lock:
                target_position = target_agent.State.get("position")
            if not isinstance(target_position, Vector2):
                return ExecutionStatus.Failed
            new_position = RpgUtils.move_towards_other_position(
                agent_position, target_position
            )
            agent_instance.State["position"] = new_position
            print(
                f"{agent_instance.Name} moving toward {target_agent.Name} from {agent_position} to {new_position}"
            )
            if RpgUtils.in_distance(new_position, target_position, 1.0):
                print(f"{agent_instance.Name} reached {target_agent.Name}!")
                return ExecutionStatus.Succeeded
            else:
                return ExecutionStatus.Executing

    @staticmethod
    def see_food_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agent_position = agent_instance.State.get("position")
            food_positions_in_state = agent_instance.State.get("foodPositions")
            if isinstance(agent_position, Vector2) and isinstance(
                food_positions_in_state, list
            ):
                food_sight_range = agent_instance.State.get(
                    "food_sight_range", 20.0
                )  # Use agent-specific food sight range
                food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                    agent_position, food_positions_in_state, food_sight_range
                )
                agent_instance.State["canSeeFood"] = food_in_range is not None
                if not agent_instance.State["canSeeFood"] and agent_instance.State.get(
                    "eatingFood"
                ):
                    agent_instance.State["eatingFood"] = False

    @staticmethod
    def food_proximity_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agent_position = agent_instance.State.get("position")
            food_positions_in_state = agent_instance.State.get("foodPositions")
            if isinstance(agent_position, Vector2) and isinstance(
                food_positions_in_state, list
            ):
                food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                    agent_position, food_positions_in_state, 1.0
                )
                agent_instance.State["nearFood"] = food_in_range is not None
                if not agent_instance.State["nearFood"] and agent_instance.State.get(
                    "eatingFood"
                ):
                    agent_instance.State["eatingFood"] = False

    @staticmethod
    def look_for_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        agent_position = agent_instance.State.get("position")
        if isinstance(agent_position, Vector2):
            new_x = agent_position.X + CommonRpgAgentHandlers._rng.randint(-1, 1)
            new_y = agent_position.Y + CommonRpgAgentHandlers._rng.randint(-1, 1)
            new_x = max(0, min(new_x, MaxX - 1))
            new_y = max(0, min(new_y, MaxY - 1))
            new_position = Vector2(new_x, new_y)
            agent_instance.State["position"] = new_position
        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed

    @staticmethod
    def go_to_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        food_position = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")
        if not isinstance(food_position, Vector2) or not isinstance(
            agent_position, Vector2
        ):
            return ExecutionStatus.Failed
        new_position = RpgUtils.move_towards_other_position(
            agent_position, food_position
        )
        agent_instance.State["position"] = new_position
        if RpgUtils.in_distance(new_position, food_position, 1.0):
            return ExecutionStatus.Succeeded
        else:
            return ExecutionStatus.Executing

    @staticmethod
    def eat_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        food_positions_in_state = agent_instance.State.get("foodPositions")
        agent_position = agent_instance.State.get("position")
        if isinstance(food_positions_in_state, list) and isinstance(
            agent_position, Vector2
        ):
            food_to_eat = CommonRpgAgentHandlers._get_food_in_range(
                agent_position, food_positions_in_state, 1.0
            )
            if food_to_eat is not None:
                food_eaten = agent_instance.State.get(
                    "food_eaten", 0
                )  # This state is only for player, monster does not have it.
                print(
                    f"{agent_instance.Name} ate food at {food_to_eat}. Food eaten: {food_eaten} -> {food_eaten + 1}"
                    if "food_eaten" in agent_instance.State
                    else f"{agent_instance.Name} ate food at {food_to_eat}"
                )
                food_positions_in_state.remove(food_to_eat)
                # agent_instance.State["food_eaten"] = food_eaten + 1
                return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed


# --- RPG Character Factories ---
class RpgCharacterFactory:
    @staticmethod
    def create(agents: List["Agent"], name: str = "Player") -> "Agent":
        remove_enemies_goal = Goal(
            name="Remove Enemies", weight=1.0, desired_state={"canSeeEnemies": False}
        )
        see_enemies_sensor = Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        )
        enemy_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler,
            "Enemy Proximity Sensor",
        )
        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions={"canSeeEnemies": True, "nearEnemy": False},
            postconditions={"nearEnemy": True},
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_enemy_cost,
        )
        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions={"nearEnemy": True},
            postconditions={"canSeeEnemies": False, "nearEnemy": False},
        )
        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "hp": 80,
                "position": Vector2(10, 10),
                "faction": "enemy" if "Monster" in name else "player",
                "agents": agents,
                "sight_range": (
                    5.0 if "Monster" in name else 10.0
                ),  # Set range based on type
            },
            goals=[remove_enemies_goal],
            sensors=[see_enemies_sensor, enemy_proximity_sensor],
            actions=[go_to_enemy_action, kill_nearby_enemy_action],
        )
        return agent


class PlayerFactory:
    @staticmethod
    def create(
        agents: List["Agent"],
        food_positions: List[Vector2],
        name: str = "Player",
        use_extreme=False,
    ) -> "Agent":

        if use_extreme:
            food_goal = ExtremeGoal(
                name="Maximize Food Eaten",
                weight=1.0,
                desired_state={"food_eaten": True},
            )
        else:
            food_goal = ComparativeGoal(
                name="Get exactly 3 food",
                weight=1.0,
                desired_state={
                    "food_eaten": ComparisonValuePair(
                        operator=ComparisonOperator.Equals, value=3
                    )
                },
            )
        remove_enemies_goal = Goal(
            name="Remove Enemies", weight=10.0, desired_state={"canSeeEnemies": False}
        )
        see_enemies_sensor = Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        )
        enemy_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler,
            "Enemy Proximity Sensor",
        )
        see_food_sensor = Sensor(
            CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor"
        )
        food_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.food_proximity_sensor_handler,
            "Food Proximity Sensor",
        )
        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions={"canSeeEnemies": True, "nearEnemy": False},
            postconditions={"nearEnemy": True},
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_enemy_cost,
        )
        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions={"nearEnemy": True},
            postconditions={"canSeeEnemies": False, "nearEnemy": False},
        )
        look_for_food_action = Action(
            name="Look For Food",
            executor=CommonRpgAgentHandlers.look_for_food_executor,
            preconditions={"canSeeFood": False},
            postconditions={"canSeeFood": True},
        )
        go_to_food_action = Action(
            name="Go To Food",
            executor=CommonRpgAgentHandlers.go_to_food_executor,
            preconditions={"canSeeFood": True, "nearFood": False},
            postconditions={"nearFood": True},
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_food_cost,
        )
        eat_food_action = Action(
            name="Eat Food",
            executor=CommonRpgAgentHandlers.eat_food_executor,
            preconditions={"nearFood": True},
            arithmetic_postconditions={"food_eaten": 1},
        )

        def rest_executor(agent_instance, action_instance):
            print(f"{agent_instance.Name} is resting")
            return ExecutionStatus.Succeeded

        rest_action = Action(
            name="Rest",
            executor=rest_executor,
            preconditions={"well_rested": False},
            postconditions={"well_rested": True, "stretched": False},
            cost_callback=lambda agent_instance, action_instance: 100,
        )

        def walk_around_executor(agent_instance, action_instance):
            print(f"{agent_instance.Name} is walking around")
            return ExecutionStatus.Succeeded

        walk_around_action = Action(
            name="Walk Around",
            executor=walk_around_executor,
            preconditions={"stretched": False},
            postconditions={"stretched": True, "well_rested": False},
            cost_callback=lambda agent_instance, action_instance: 100,
        )
        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "canSeeFood": False,
                "nearFood": False,
                "hp": 80,
                "food_eaten": 0,
                "position": Vector2(10, 10),
                "faction": "player",
                "agents": agents,
                "foodPositions": food_positions,
                "well_rested": False,
                "stretched": False,
                "sight_range": 10.0,
                "food_sight_range": 20.0,
            },
            goals=[
                food_goal,
                remove_enemies_goal,
                Goal(
                    name="Get well rested",
                    weight=0.11,
                    desired_state={"well_rested": True},
                ),
                Goal(
                    name="Get stretched", weight=0.1, desired_state={"stretched": True}
                ),
            ],
            sensors=[
                see_enemies_sensor,
                enemy_proximity_sensor,
                see_food_sensor,
                food_proximity_sensor,
            ],
            actions=[
                go_to_enemy_action,
                kill_nearby_enemy_action,
                look_for_food_action,
                go_to_food_action,
                eat_food_action,
                rest_action,
                walk_around_action,
            ],
        )
        return agent


class RpgMonsterFactory:
    _counter = 1

    @staticmethod
    def create(agents: List["Agent"], food_positions: List[Vector2]) -> "Agent":
        monster_name = f"Monster {RpgMonsterFactory._counter}"
        RpgMonsterFactory._counter += 1
        agent = RpgCharacterFactory.create(agents, monster_name)
        agent.State["faction"] = "enemy"
        eat_food_goal = Goal(
            name="Eat Food", weight=0.1, desired_state={"eatingFood": True}
        )
        see_food_sensor = Sensor(
            CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor"
        )
        food_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.food_proximity_sensor_handler,
            "Food Proximity Sensor",
        )
        look_for_food_action = Action(
            name="Look For Food",
            executor=CommonRpgAgentHandlers.look_for_food_executor,
            preconditions={"canSeeFood": False, "canSeeEnemies": False},
            postconditions={"canSeeFood": True},
        )
        go_to_food_action = Action(
            name="Go To Food",
            executor=CommonRpgAgentHandlers.go_to_food_executor,
            preconditions={"canSeeFood": True, "canSeeEnemies": False},
            postconditions={"nearFood": True},
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_food_cost,
        )
        eat_action = Action(
            name="Eat",
            executor=CommonRpgAgentHandlers.eat_food_executor,
            preconditions={"nearFood": True, "canSeeEnemies": False},
            postconditions={"eatingFood": True},
        )
        # Initialize monster state
        agent.State.update(
            {
                "canSeeFood": False,
                "nearFood": False,
                "eatingFood": False,
                "foodPositions": food_positions,
                "hp": 2,
                "sight_range": 5.0,
                "food_sight_range": 5.0,
            }
        )

        agent.Goals.append(eat_food_goal)
        agent.Sensors.extend([see_food_sensor, food_proximity_sensor])
        agent.Actions.extend([go_to_food_action, look_for_food_action, eat_action])
        return agent



