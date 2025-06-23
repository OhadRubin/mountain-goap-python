#
# Minecraft Bot converted to use the GOAP Framework
#
# This single file contains the complete GOAP-based implementation.
# It assumes the GOAP framework classes (Agent, Action, Goal, etc.) are available.
#
# The original pybot code is used as a low-level API for world interaction,
# while the GOAP agent handles all high-level decision making.
#

import sys
import time
import threading
from typing import List, Dict, Any, Optional, Callable

# --- Assume GOAP Framework is available ---
# The following classes are part of the provided GOAP framework and are not redefined here.
# from goap_python_code import Agent, Action, Goal, ComparativeGoal, ExtremeGoal, Sensor, ExecutionStatus, ComparisonOperator, ComparisonValuePair, PermutationSelectorGenerators

# --- Import original bot for low-level interaction ---
from pybot import PyBot
from inventory import Chest
from gather import BoundingBox
from workarea import workArea
from javascript import require

# --- Type Aliases ---
StateDictionary = Dict[str, Optional[Any]]
ExecutorCallback = Callable[["Agent", "Action"], "ExecutionStatus"]

# ==============================================================================
# 1. BOT ACTION EXECUTORS
# ==============================================================================
# These functions contain the actual logic for performing actions in the world.
# They call methods on the original pybot instance, which is stored in the
# agent's memory.


def get_pybot(agent: "Agent") -> PyBot:
    """Helper to retrieve the pybot instance from agent memory."""
    return agent.Memory.get("pybot")


def go_to_location_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    """Executor for moving the bot to a target location."""
    pybot = get_pybot(agent)
    target_pos = action.get_parameter("target_pos")
    if not target_pos:
        return ExecutionStatus.Failed

    pybot.pdebug(f"GOAP: Executing go_to_location to {target_pos}", 2)
    pybot.safeWalk(target_pos, 1.5)  # Walk to within 1.5 blocks

    # This action is non-blocking, we assume it succeeds over time.
    # A more robust system would check if pathing is complete.
    time.sleep(2)  # Simulate travel time
    return ExecutionStatus.Succeeded


def eat_food_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    """Executor for eating food."""
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing eat_food", 2)
    if pybot.eatFood():
        return ExecutionStatus.Succeeded
    return ExecutionStatus.Failed


def restock_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    """Executor for restocking inventory from a nearby chest."""
    pybot = get_pybot(agent)
    activity = action.get_parameter("activity")
    if not activity:
        return ExecutionStatus.Failed

    pybot.pdebug(f"GOAP: Executing restock for {activity}", 2)

    if activity == "mining":
        pybot.restockFromChest(pybot.miningEquipList)
    elif activity == "chopping":
        pybot.restockFromChest(pybot.chopEquipList)
    elif activity == "farming":
        pybot.restockFromChest(pybot.farmingEquipList)
    else:
        return ExecutionStatus.Failed

    return ExecutionStatus.Succeeded


def deposit_all_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    """Executor for depositing all non-essential items into a chest."""
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing deposit_all", 2)

    # Keep essential tools and food
    blacklist = list(pybot.miningMinimumList.keys())

    chest = Chest(pybot)
    if not chest.object:
        return ExecutionStatus.Failed

    chest.deposit(blacklist=blacklist)
    chest.close()
    return ExecutionStatus.Succeeded


# --- Chopping Wood Executors ---


def find_tree_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing find_tree", 2)
    tree_block = pybot.findClosestBlock("Spruce Log", xz_radius=25, y_radius=1)
    if tree_block:
        agent.State["tree_location"] = tree_block.position
        agent.State["knows_tree_location"] = True
        pybot.pdebug(f"  Found tree at {tree_block.position}", 3)
        return ExecutionStatus.Succeeded
    return ExecutionStatus.Failed


def validate_tree_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing validate_tree", 2)
    tree_location = agent.State.get("tree_location")
    if not tree_location:
        return ExecutionStatus.Failed

    tree_block = pybot.blockAt(tree_location)
    box = BoundingBox(pybot, tree_block)

    if box.dx() == 2 and box.dz() == 2 and box.dy() >= 5:
        agent.Memory["tree_bounding_box"] = box
        agent.State["tree_validated"] = True
        pybot.pdebug(f"  Tree validated. Height: {box.dy()}", 3)
        return ExecutionStatus.Succeeded

    pybot.pdebug("  Tree validation failed.", 2)
    # Invalidate knowledge to allow finding another tree
    agent.State["knows_tree_location"] = False
    agent.State["tree_location"] = None
    return ExecutionStatus.Failed


def climb_tree_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    box = agent.Memory.get("tree_bounding_box")
    if not box:
        return ExecutionStatus.Failed

    # This is a simplified version of the original spiral climb.
    # It performs one cycle of climbing.

    current_y = agent.State.get("tree_climbing_height", box.y_min)
    pybot.pdebug(f"GOAP: Executing climb_tree at Y={current_y}", 2)

    if current_y + 8 >= box.y_max:
        agent.State["tree_at_top"] = True
        return ExecutionStatus.Succeeded

    x0, z0 = box.x_min, box.z_min

    # One spiral cycle
    pybot.wieldItem("Stone Axe")
    pybot.chop(x0, current_y + 1, z0, 3)
    pybot.walkOnBlock(x0, current_y, z0)
    time.sleep(0.5)
    pybot.chop(x0 + 1, current_y + 2, z0, 3)
    pybot.walkOnBlock(x0 + 1, current_y + 1, z0)
    time.sleep(0.5)
    pybot.chop(x0 + 1, current_y + 3, z0 + 1, 3)
    pybot.walkOnBlock(x0 + 1, current_y + 2, z0 + 1)
    time.sleep(0.5)
    pybot.chop(x0, current_y + 4, z0 + 1, 3)
    pybot.walkOnBlock(x0, current_y + 3, z0 + 1)
    time.sleep(0.5)

    agent.State["tree_climbing_height"] = current_y + 4
    return ExecutionStatus.Succeeded


def descend_and_cut_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    box = agent.Memory.get("tree_bounding_box")
    if not box:
        return ExecutionStatus.Failed

    current_y = agent.State.get("tree_climbing_height", box.y_max)
    pybot.pdebug(f"GOAP: Executing descend_and_cut at Y={current_y}", 2)

    if current_y < box.y_min:
        agent.State["tree_chopped"] = True
        return ExecutionStatus.Succeeded

    x0, z0 = box.x_min, box.z_min

    # Chop one level
    pybot.wieldItem("Stone Axe")
    pybot.chop(x0, current_y, z0, 1)
    pybot.chop(x0 + 1, current_y, z0, 1)
    pybot.chop(x0 + 1, current_y, z0 + 1, 1)
    pybot.chop(x0, current_y, z0 + 1, 1)

    agent.State["tree_climbing_height"] = current_y - 1
    return ExecutionStatus.Succeeded


# --- Farming Executors ---
def harvest_crop_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing harvest_crop", 2)
    crop = pybot.findHarvestable(r=25)
    if crop:
        pybot.walkToBlock(crop)
        pybot.bot.dig(crop)
        return ExecutionStatus.Succeeded
    return ExecutionStatus.Failed


def plant_seed_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing plant_seed", 2)
    soil = pybot.findSoil(center=pybot.bot.entity.position, r=25)
    if soil:
        pybot.wieldItemFromList(pybot.farming_seeds)
        pybot.walkOnBlock(soil)
        pybot.bot.placeBlock(soil, require("vec3").Vec3(0, 1, 0))
        return ExecutionStatus.Succeeded
    return ExecutionStatus.Failed


# --- Mining Executors ---
def establish_mine_work_area_executor(
    agent: "Agent", action: "Action"
) -> "ExecutionStatus":
    pybot = get_pybot(agent)
    pybot.pdebug("GOAP: Executing establish_mine_work_area", 2)
    area = workArea(pybot, width=3, height=3, depth=99999)
    if area.valid:
        agent.Memory["mine_work_area"] = area
        agent.State["work_area_defined"] = True
        return ExecutionStatus.Succeeded
    return ExecutionStatus.Failed


def mine_tunnel_slice_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    area = agent.Memory.get("mine_work_area")
    if not area:
        return ExecutionStatus.Failed

    z = agent.State.get("tunnel_depth", 0)
    pybot.pdebug(f"GOAP: Executing mine_tunnel_slice at depth {z}", 2)

    # Simplified version of one slice of stripMine
    area.walkToBlock3(0, 0, z)

    # Mine main tunnel column
    for x in area.xRange():
        pybot.mineColumn(area, x, z, area.height)
        pybot.floorMine(area, x, z, 2)

    # Bridge
    for x in area.xRange():
        pybot.bridgeIfNeeded(area, x, z)

    agent.State["main_tunnel_cleared_at_depth"] = z
    return ExecutionStatus.Succeeded


def place_torch_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    area = agent.Memory.get("mine_work_area")
    if not area:
        return ExecutionStatus.Failed
    z = agent.State.get("tunnel_depth", 0)
    pybot.pdebug(f"GOAP: Executing place_torch at depth {z}", 2)

    torch_v = area.toWorld(area.width2, 1, z)
    wall_v = area.toWorld(area.width2 + 1, 1, z)
    dv = pybot.Vec3(torch_v.x - wall_v.x, 0, torch_v.z - wall_v.z)

    if pybot.bot.blockAt(wall_v).displayName not in pybot.ignored_blocks:
        pybot.wieldItem("Torch")
        pybot.safePlaceBlock(wall_v, dv)

    return ExecutionStatus.Succeeded


def advance_tunnel_executor(agent: "Agent", action: "Action") -> "ExecutionStatus":
    pybot = get_pybot(agent)
    z = agent.State.get("tunnel_depth", 0)
    pybot.pdebug(f"GOAP: Advancing tunnel from {z} to {z+1}", 2)
    agent.State["tunnel_depth"] = z + 1
    return ExecutionStatus.Succeeded


# ==============================================================================
# 2. BOT SENSORS
# ==============================================================================
# These functions update the agent's world state based on the pybot's perceptions.


def survival_sensor(agent: "Agent"):
    pybot = get_pybot(agent)
    health = pybot.bot.health
    food = pybot.bot.food
    agent.State["health"] = health
    agent.State["food"] = food
    agent.State["health_critical"] = health <= 10  # 50%
    agent.State["needs_healing"] = health < 20 or food < 18


def inventory_sensor(agent: "Agent"):
    pybot = get_pybot(agent)
    agent.State["has_food"] = pybot.invItemCount("Bread") > 0
    agent.State["has_wood"] = pybot.invItemCount("Spruce Log")
    agent.State["has_pickaxe"] = (
        pybot.invItemCount("Stone Pickaxe") > 0
        or pybot.invItemCount("Iron Pickaxe") > 0
    )
    agent.State["has_axe"] = pybot.invItemCount("Stone Axe") > 0
    agent.State["has_seeds"] = pybot.invItemCount("Wheat Seeds") > 0
    agent.State["has_torches"] = pybot.invItemCount("Torch") > 10
    agent.State["inventory_full"] = pybot.bot.inventory.emptySlotCount() == 0

    # Check for restocking needs
    if agent.State.get("current_activity") == "mining":
        agent.State["needs_restocking"] = not pybot.checkMinimumList(
            pybot.miningMinimumList
        )
    elif agent.State.get("current_activity") == "chopping":
        agent.State["needs_restocking"] = not pybot.checkMinimumList(
            {"Stone Axe": 1, "Bread": 1}
        )
    else:
        agent.State["needs_restocking"] = False


def environment_sensor(agent: "Agent"):
    pybot = get_pybot(agent)
    pos = pybot.bot.entity.position
    agent.State["position_x"] = pos.x
    agent.State["position_y"] = pos.y
    agent.State["position_z"] = pos.z

    chest = pybot.findClosestBlock("Chest", xz_radius=3)
    agent.State["at_chest"] = chest is not None
    if chest:
        agent.State["chest_location"] = chest.position

    # This is a simplified check for farm/mine locations
    agent.State["at_farm"] = agent.State.get(
        "current_activity"
    ) == "farming" and agent.State.get("at_chest")
    agent.State["at_mine"] = agent.State.get(
        "current_activity"
    ) == "mining" and agent.State.get("at_chest")
    agent.State["at_tree"] = (
        agent.State.get("knows_tree_location")
        and pybot.bot.entity.position.distanceTo(agent.State.get("tree_location")) < 5
    )


def farming_sensor(agent: "Agent"):
    pybot = get_pybot(agent)
    agent.State["mature_crops_available"] = pybot.findHarvestable(r=25) is not None
    agent.State["farmland_available"] = (
        pybot.findSoil(pybot.bot.entity.position, r=25) is not None
    )


def mining_sensor(agent: "Agent"):
    z = agent.State.get("tunnel_depth", 0)
    torch_z = agent.State.get("last_torch_z", -1)
    agent.State["torch_interval_reached"] = (z - torch_z) >= 6
    agent.State["break_interval_reached"] = (
        agent.State.get("blocks_mined", 0) > 100
    )  # simplified


# ==============================================================================
# 3. BOT FACTORY
# ==============================================================================
# This factory assembles the agent with its goals, sensors, and actions.


class MinecraftBotFactory:
    @staticmethod
    def create_agent(pybot_instance: PyBot) -> "Agent":

        # --- GOALS ---
        goals = [
            Goal("Stay Healthy", weight=1.0, desired_state={"needs_healing": False}),
            ComparativeGoal(
                "Gather 64 Wood",
                weight=0.8,
                desired_state={
                    "has_wood": ComparisonValuePair(
                        value=64, operator=ComparisonOperator.GreaterThanOrEquals
                    )
                },
            ),
            ComparativeGoal(
                "Gather 64 Wheat",
                weight=0.7,
                desired_state={
                    "has_wheat": ComparisonValuePair(
                        value=64, operator=ComparisonOperator.GreaterThanOrEquals
                    )
                },
            ),
            Goal(
                "Mine for an Hour",
                weight=0.6,
                desired_state={"mined_for_an_hour": True},
            ),
            Goal("Be Idle", weight=0.1, desired_state={"has_activity": False}),
        ]

        # --- SENSORS ---
        sensors = [
            Sensor(survival_sensor, "Survival Sensor"),
            Sensor(inventory_sensor, "Inventory Sensor"),
            Sensor(environment_sensor, "Environment Sensor"),
            Sensor(farming_sensor, "Farming Sensor"),
            Sensor(mining_sensor, "Mining Sensor"),
        ]

        # --- ACTIONS ---

        # Generic Actions
        action_eat_food = Action(
            name="Eat Food",
            executor=eat_food_executor,
            preconditions={"needs_healing": True, "has_food": True},
            arithmetic_postconditions={"food": 20, "health": 20},  # Simplified effect
        )

        action_restock = Action(
            name="Restock Inventory",
            executor=restock_executor,
            preconditions={"at_chest": True, "needs_restocking": True},
            postconditions={"needs_restocking": False},
            permutation_selectors={
                "activity": PermutationSelectorGenerators.select_from_collection(
                    ["mining", "chopping", "farming"]
                )
            },
        )

        action_go_to_chest = Action(
            name="Go to Chest",
            executor=go_to_location_executor,
            preconditions={"knows_chest_location": True, "at_chest": False},
            postconditions={"at_chest": True},
            permutation_selectors={
                "target_pos": PermutationSelectorGenerators.select_from_collection_in_state(
                    "chest_location"
                )
            },
        )

        action_deposit_all = Action(
            name="Deposit All Items",
            executor=deposit_all_executor,
            preconditions={"at_chest": True, "inventory_full": True},
            postconditions={"inventory_full": False},
        )

        # Wood Chopping Actions
        action_find_tree = Action(
            name="Find Tree",
            executor=find_tree_executor,
            preconditions={"knows_tree_location": False},
            postconditions={"knows_tree_location": True},
        )

        action_go_to_tree = Action(
            name="Go to Tree",
            executor=go_to_location_executor,
            preconditions={"knows_tree_location": True, "at_tree": False},
            postconditions={"at_tree": True},
            permutation_selectors={
                "target_pos": PermutationSelectorGenerators.select_from_collection_in_state(
                    "tree_location"
                )
            },
        )

        action_validate_tree = Action(
            name="Validate Tree",
            executor=validate_tree_executor,
            preconditions={"at_tree": True, "tree_validated": False},
            postconditions={"tree_validated": True},
        )

        action_climb_tree = Action(
            name="Climb Tree",
            executor=climb_tree_executor,
            preconditions={
                "tree_validated": True,
                "tree_at_top": False,
                "has_axe": True,
            },
            # Effects are managed internally by executor
        )

        action_descend_and_cut = Action(
            name="Descend and Cut Tree",
            executor=descend_and_cut_executor,
            preconditions={"tree_at_top": True, "has_axe": True},
            arithmetic_postconditions={"has_wood": 4},  # Approx per level
        )

        # Farming Actions
        action_harvest_crop = Action(
            name="Harvest Crop",
            executor=harvest_crop_executor,
            preconditions={"at_farm": True, "mature_crops_available": True},
            postconditions={"mature_crops_available": False},
            arithmetic_postconditions={"has_wheat": 1, "has_seeds": 2},
        )

        action_plant_seed = Action(
            name="Plant Seed",
            executor=plant_seed_executor,
            preconditions={
                "at_farm": True,
                "farmland_available": True,
                "has_seeds": True,
            },
            postconditions={"farmland_available": False},
            arithmetic_postconditions={"has_seeds": -1},
        )

        # Mining Actions
        action_establish_mine_work_area = Action(
            name="Establish Mine Work Area",
            executor=establish_mine_work_area_executor,
            preconditions={"at_mine": True, "work_area_defined": False},
            postconditions={"work_area_defined": True},
        )

        action_mine_tunnel_slice = Action(
            name="Mine Tunnel Slice",
            executor=mine_tunnel_slice_executor,
            preconditions={"work_area_defined": True, "has_pickaxe": True},
            arithmetic_postconditions={"blocks_mined": 10},  # Approx
        )

        action_place_torch = Action(
            name="Place Mining Torch",
            executor=place_torch_executor,
            preconditions={
                "work_area_defined": True,
                "torch_interval_reached": True,
                "has_torches": True,
            },
            postconditions={"torch_interval_reached": False},
            arithmetic_postconditions={"has_torches": -1},
        )

        action_advance_tunnel = Action(
            name="Advance Tunnel",
            executor=advance_tunnel_executor,
            preconditions={"work_area_defined": True},
            # Effect is managed by executor
        )

        actions = [
            action_eat_food,
            action_restock,
            action_go_to_chest,
            action_deposit_all,
            action_find_tree,
            action_go_to_tree,
            action_validate_tree,
            action_climb_tree,
            action_descend_and_cut,
            action_harvest_crop,
            action_plant_seed,
            action_establish_mine_work_area,
            action_mine_tunnel_slice,
            action_place_torch,
            action_advance_tunnel,
        ]

        # --- AGENT ---
        agent = Agent(
            name="MinecraftPyBot",
            state={
                "has_activity": False,
                "current_activity": "idle",
                "knows_tree_location": False,
                "tree_location": None,
                "at_tree": False,
                "tree_validated": False,
                "tree_climbing_height": 0,
                "tree_at_top": False,
                "tree_chopped": False,
                "has_wheat": 0,
                "tunnel_depth": 0,
                "last_torch_z": -1,
                "work_area_defined": False,
                "blocks_mined": 0,
                "mined_for_an_hour": False,  # This would be set by a timer sensor
                "at_mine": False,
                "at_farm": False,
            },
            goals=goals,
            sensors=sensors,
            actions=actions,
            memory={"pybot": pybot_instance},
        )

        return agent


# ==============================================================================
# 4. MAIN EXECUTION LOOP
# ==============================================================================

if __name__ == "__main__":
    import argparse
    from account import account as bot_account

    parser = argparse.ArgumentParser(prog="python goap_bot.py")
    parser.add_argument("--nowindow", action="store_true", help="run in the background")
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="verbosity from 1-5"
    )
    args = parser.parse_args()

    print("Initializing original PyBot instance...")
    if args.nowindow:
        pybot = PyBot(bot_account.account)
    else:
        from ui import PyBotWithUI

        pybot = PyBotWithUI(bot_account.account)

    if args.verbose:
        pybot.debug_lvl = args.verbose

    # Wait for bot to be ready
    while not pybot.bot.health:
        time.sleep(1)

    print("Initializing GOAP Agent...")
    goap_agent = MinecraftBotFactory.create_agent(pybot)

    print("GOAP Agent Ready. Starting main loop...")

    # Main loop for the GOAP agent
    def goap_main_loop():
        while True:
            try:
                # The agent's step method will run sensors, and if not busy, plan and execute.
                goap_agent.step(mode=StepMode.OneAction)

                # Update the UI if it exists
                if hasattr(pybot, "win"):
                    pybot.win.update_idletasks()
                    pybot.win.update()

                time.sleep(1)  # Tick rate for the GOAP agent's decisions
            except (KeyboardInterrupt, SystemExit):
                print("Stopping GOAP agent.")
                break
            except Exception as e:
                print(f"An error occurred in the main loop: {e}")
                pybot.pexception("GOAP Main Loop Error", e)
                time.sleep(5)

    # --- Start Chat Listener and GOAP Loop in Threads ---

    # Keep the original bot's chat listener for commands
    @On(pybot.bot, "chat")
    def onChat(sender, message, this, *rest):
        # Instead of executing commands directly, we add goals to the agent.
        print(f"GOAP received command: '{message}' from {sender}")
        message = message.lower().strip()

        if message == "chop wood":
            pybot.chat("Okay, I'll find a tree to chop.")
            # Add a temporary, high-priority goal
            new_goal = ComparativeGoal(
                "Gather 64 Wood",
                weight=10.0,
                desired_state={
                    "has_wood": ComparisonValuePair(
                        value=64, operator=ComparisonOperator.GreaterThanOrEquals
                    )
                },
            )
            goap_agent.Goals.insert(0, new_goal)  # Insert at front for high priority
            goap_agent.State["current_activity"] = "chopping"

        elif message == "farm":
            pybot.chat("Okay, I'll start farming.")
            new_goal = ComparativeGoal(
                "Gather 64 Wheat",
                weight=10.0,
                desired_state={
                    "has_wheat": ComparisonValuePair(
                        value=64, operator=ComparisonOperator.GreaterThanOrEquals
                    )
                },
            )
            goap_agent.Goals.insert(0, new_goal)
            goap_agent.State["current_activity"] = "farming"

        elif message == "mine":
            pybot.chat("Okay, I'll start mining.")
            new_goal = Goal(
                "Mine Tunnel", weight=10.0, desired_state={"tunnel_depth": 50}
            )
            goap_agent.Goals.insert(0, new_goal)
            goap_agent.State["current_activity"] = "mining"

        elif message == "stop":
            pybot.chat("Okay, stopping my current plan.")
            goap_agent.clear_plan()
            goap_agent.State["current_activity"] = "idle"
            # Remove any high-priority commanded goals
            goap_agent.Goals = [g for g in goap_agent.Goals if g.Weight < 10.0]

        elif message == "inventory":
            pybot.printInventory()

        elif message == "status":
            pybot.sayStatus()

    # The original bot's health check remains, as it's a critical safety feature
    @On(pybot.bot, "health")
    def onHealth(arg):
        pybot.healthCheck()

    # Start the GOAP loop in a separate thread
    goap_thread = threading.Thread(target=goap_main_loop, daemon=True)
    goap_thread.start()

    # Run the UI main loop if it exists
    if hasattr(pybot, "win"):
        pybot.mainloop()
    else:
        # If no UI, just wait for the thread (which runs forever until interrupted)
        goap_thread.join()
