# A* Infinite Loop Debugging Guide

## The Problem: When A* Search Never Terminates

A* search can get stuck in infinite loops when exploring action sequences, particularly with ComparativeGoals and infinite search limits. This guide helps identify and fix these cases.

## Root Cause Analysis

### Symptom: Planner Hangs on Goal Planning
```
DEBUG: Player calling planner
PLANNER DEBUG: Starting planning for Player
  Player state: food_eaten=4, well_rested=False, stretched=False
  Planning for goal: Get exactly 5 food
{infinite loop - no further output}
```

**Investigation Order:**
1. **Infinite Search Limits**: Check if `cost_maximum=inf` and `step_maximum=inf`
2. **Goal Type Issues**: ComparativeGoals can cause infinite exploration
3. **Action Permutation Explosion**: Multiple action variants creating vast search spaces
4. **Heuristic Function Bugs**: Poor heuristics encouraging infinite exploration

### Key Debug Points

**Add A* Search Debugging:**
```python
# In ActionAStar.__init__()
is_debug_search = False
if start.State.get('faction') == 'player' and start.State.get('food_eaten') == 4:
    is_debug_search = True
    print(f"A* DEBUG: Starting search for goal {goal.Name}")
    print(f"Start state: food_eaten={start.State.get('food_eaten')}")
    print(f"Limits: cost_maximum={cost_maximum}, step_maximum={step_maximum}")
    
nodes_explored = 0
while frontier.count > 0:
    nodes_explored += 1
    if nodes_explored > 100:
        print(f"A* WARNING: Explored {nodes_explored} nodes, possible infinite loop!")
        break
```

## Common Infinite Loop Patterns

### Pattern 1: Infinite Search Limits
**Symptoms:** A* explores thousands of nodes, never terminates
```
Limits: cost_maximum=inf, step_maximum=inf
```

**Root Cause:** With no limits, A* thinks it can always find a "better" path by exploring longer action sequences, even when simple solutions exist.

**Solution:** This is NOT solved by adding artificial limits. The root cause must be identified first.

### Pattern 2: ComparativeGoal Edge Cases
**Symptoms:** Goal is achievable in 2 steps but A* explores infinite alternatives
```python
food_goal = ComparativeGoal(
    name="Get exactly 5 food",
    desired_state={"food_eaten": ComparisonValuePair(operator=ComparisonOperator.Equals, value=5)}
)
```

**Root Cause:** ComparativeGoal requires `action_node.Action is not None`, forcing A* to find action sequences even when current state could satisfy goal directly.

**Investigation:**
```python
# Check if goal can be satisfied in current state
current_satisfies = Utils.meets_goal(goal, start_node, start_node)
print(f"Current state satisfies goal: {current_satisfies}")

# Check action sequence requirements
if isinstance(goal, ComparativeGoal):
    print("ComparativeGoal requires action sequences - cannot use zero-action solutions")
```

### Pattern 3: Action Permutation Explosion
**Symptoms:** Hundreds of similar action variants in ActionGraph
```
Available actions: ['Go To Food', 'Go To Food', 'Go To Food', ... (18 times)]
```

**Root Cause:** Permutation selectors create one action variant per target, multiplying search space exponentially.

**Investigation:**
```python
# In ActionGraph.__init__()
for action in actions:
    permutations = action.get_permutations(state)
    print(f"Action {action.Name}: {len(permutations)} permutations")
    if len(permutations) > 10:
        print(f"WARNING: {action.Name} has excessive permutations!")
```

## Debugging Strategies by Root Cause

### Strategy 1: Find The Real Bug
```python
# DO NOT add artificial limits - this masks the real issue
# Instead, identify why A* cannot find the simple solution
print(f"A* should find: Go To Food -> Eat Food (2 steps)")
print(f"But it's exploring infinite alternatives - WHY?")
```

### Strategy 2: Add Early Termination
```python
# In ActionAStar.__init__()
nodes_explored = 0
while frontier.count > 0:
    current = frontier.dequeue()
    nodes_explored += 1
    
    # Emergency brake for infinite loops
    if nodes_explored > 1000:
        print(f"A* TIMEOUT: Explored {nodes_explored} nodes, terminating search")
        break
```

### Strategy 3: Optimize Goal Types
```python
# Replace problematic ComparativeGoal with simple Goal when possible
# Instead of:
ComparativeGoal(name="Get exactly 5 food", 
                desired_state={"food_eaten": ComparisonValuePair(operator=Equals, value=5)})

# Use conditions to make goal inactive when satisfied:
class ConditionalGoal(Goal):
    def is_valid(self, world_state):
        return world_state.get("food_eaten", 0) < 5  # Only active when not satisfied
```

### Strategy 4: Reduce Action Permutations
```python
# Limit permutation explosion
def limited_food_permutations(state):
    all_food = RpgUtils.food_permutations(state)
    return all_food[:5]  # Only consider closest 5 food items

go_to_food_action = Action(
    permutation_selectors={"target": limited_food_permutations}
)
```

## Investigation Checklist

### ✅ Search Configuration  
- [ ] Is there a simple valid path that A* should find but isn't?
- [ ] Is the goal type appropriate (Goal vs ComparativeGoal vs ExtremeGoal)?
- [ ] Are action permutations reasonable in number?

### ✅ Goal Analysis
- [ ] Can the goal be satisfied in the current state without actions?
- [ ] Does the goal require action sequences when simpler solutions exist?
- [ ] Are goal priorities causing conflicts between multiple active goals?

### ✅ Action Chain Validity
- [ ] Is there a valid action sequence that achieves the goal?
- [ ] Are action preconditions achievable from the current state?
- [ ] Do action effects actually move toward goal satisfaction?

### ✅ Heuristic Function
- [ ] Does the heuristic correctly estimate distance to goal?
- [ ] Are there bugs causing infinite cost calculations?
- [ ] Does the heuristic encourage shorter vs longer paths appropriately?

## Critical Debugging Lessons Learned

### WRONG Approaches That Mask The Real Issue

**❌ DON'T add artificial limits:**
```python
# This is WRONG - it hides the bug instead of fixing it
agent.CostMaximum = 50.0  # NO
agent.StepMaximum = 10    # NO
```

**❌ DON'T implement fixes before detecting:**
```python
# This is WRONG - always detect the issue first
if some_theory:
    implement_fix()  # NO - detect first!
```

**❌ DON'T use complex theoretical solutions:**
```python
# This is WRONG - look for simple edge cases instead
class ComplexCustomGoalSystem:  # NO - find the real bug
```

### ✅ RIGHT Approach: Systematic Detection

**1. Theory Formation:**
- Form specific, testable hypotheses about what's wrong
- Don't guess - use evidence from debug output

**2. Detection Before Fixing:**
```python
# ALWAYS add detection first
print(f"THEORY_X_DEBUG: Checking if condition Y occurs...")
if suspected_issue:
    print(f"THEORY_X_DEBUG: CONFIRMED - Issue Y detected!")
    assert False  # Assert is easier than complex logging
```

**3. Evidence-Based Debugging:**
```python
# Look at actual debug output, don't theorize
print(f"A* should find: Go To Food -> Eat Food (2 steps)")
print(f"But debug shows: {actual_behavior}")
print(f"WHY is this happening?")
```

**4. Focus on What's Actually Happening:**
```python
# Don't overthink - debug what the planner is doing
if infinite_loop:
    print("What is the planner actually doing?")
    # Add debugging to see the real behavior
```

**5. Look for Edge Cases and Off-By-One Errors:**
- Check state transitions carefully
- Verify action preconditions/postconditions  
- Look for simple logical errors, not complex architectural issues

## Common Solutions

### Proper Fix: Goal Redesign
```python
# Replace infinite-exploration goals with bounded alternatives
instead_of_extreme_goal = Goal(
    name="Be well rested",
    desired_state={"well_rested": True}
)

instead_of_comparative_equals = Goal(
    name="Have enough food", 
    desired_state={"has_enough_food": True}
)
# Set has_enough_food=True when food_eaten >= 5
```

### Advanced Fix: Custom Goal Validation
```python
class BoundedComparativeGoal(ComparativeGoal):
    def is_still_relevant(self, world_state):
        # Stop pursuing goal when satisfied
        for key, comp_pair in self.DesiredState.items():
            current_val = world_state.get(key)
            desired_val = comp_pair.Value
            if comp_pair.Operator == ComparisonOperator.Equals:
                if current_val == desired_val:
                    return False  # Goal satisfied, stop pursuing
        return True
```

## Conclusion

A* infinite loops typically stem from unlimited search parameters combined with goals that encourage endless exploration. The key is identifying whether the issue is:

1. **Search Configuration** - Fix with reasonable limits
2. **Goal Design** - Fix with simpler goal types  
3. **Action Explosion** - Fix with permutation limits
4. **Algorithmic Issues** - Fix with early termination

Always start with search limits as an emergency brake, then address the root cause for a proper solution.