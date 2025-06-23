# GOAP System Debugging Guide

## System Architecture Overview

This GOAP implementation consists of several key components that must work together:

```
Agent → Sensors → State → Goals → Planner → Actions → Execution
```

**Data Flow:**
1. **Sensors** update Agent **State** based on world conditions
2. **Goals** evaluate current State to determine priority and validity
3. **Planner** uses A* search to find Action sequences that achieve Goals
4. **Agent** executes planned Actions, which modify State
5. Cycle repeats

## Common Failure Patterns

### 1. Agents Don't Act At All
**Symptoms:** `sequences count: 0`, agents call planner but never execute actions

**Investigation Order:**
1. **Planning Failure**: A* can't find valid action sequences
2. **Goal Validity Issues**: No goals are considered valid/reachable  
3. **Action Precondition Problems**: Actions can't satisfy goal requirements
4. **Utility Calculation Bugs**: Valid plans rejected due to incorrect cost/benefit math

### 2. Agents Act But Behavior is Wrong
**Symptoms:** Actions execute but achieve wrong outcomes, endless loops

**Investigation Order:**
1. **Goal Priority Logic**: Wrong goals being selected
2. **Action Effects Mismatch**: Actions don't produce expected state changes
3. **Sensor Update Issues**: State not reflecting actual world conditions
4. **Planning Algorithm Problems**: A* finding suboptimal paths

### 3. Inconsistent Agent Behavior
**Symptoms:** Some agent types work, others don't; intermittent failures

**Investigation Order:**
1. **Agent Configuration Differences**: Compare working vs non-working agent setups
2. **Shared State Corruption**: Agents interfering with each other's state
3. **Threading/Concurrency Issues**: Race conditions in state updates
4. **Goal/Action Compatibility**: Mismatched goals and available actions

## Component-Specific Debugging

### Agent-Level Debugging

**Key Debug Points:**
```python
# In Agent.step()
print(f"DEBUG: {self.Name} step() - IsBusy={self.IsBusy}, IsPlanning={self.IsPlanning}")

# In Agent._execute()  
print(f"DEBUG: {self.Name}._execute() - sequences count: {len(self.CurrentActionSequences)}")
```

**What to Check:**
- Are sensors being called and updating state?
- Is the agent stuck in IsBusy=True state?
- Are action sequences being generated but not executed?

### Planning System Debugging

**Key Debug Points:**
```python
# In Planner.plan()
print(f"PLANNER: Starting planning for {agent.Name}")
for goal in agent.Goals:
    print(f"  Planning for goal: {goal.Name}")
    # After A* search:
    if cursor is not None:
        print(f"    A* found solution for {goal.Name}")
    else:
        print(f"    A* found NO solution for {goal.Name}")
```

**What to Check:**
- Is A* finding solutions for any goals?
- Are solutions being found but rejected during utility calculation?
- Are all goals failing or just specific ones?

### Goal System Debugging

**Key Debug Points:**
```python
# Check goal validity and priority
for goal in agent.Goals:
    is_valid = goal.is_valid(agent.State) if hasattr(goal, 'is_valid') else True
    priority = goal.get_priority(agent.State) if hasattr(goal, 'get_priority') else goal.Weight
    print(f"GOAL DEBUG: {goal.Name} - valid={is_valid}, priority={priority}")
```

**What to Check:**
- Are goals valid for the current state?
- Do goal priorities make sense?
- Are desired states achievable with available actions?

### Action System Debugging

**Key Debug Points:**
```python
# In Action.is_possible()
print(f"ACTION DEBUG: Checking {self.Name} preconditions against state: {state}")
for key, value in self._preconditions.items():
    actual = state.get(key)
    matches = actual == value
    print(f"  {key}: need={value}, have={actual}, matches={matches}")

# In Action.execute()
print(f"ACTION EXEC: {self.Name} starting with status {self.ExecutionStatus}")
```

**What to Check:**
- Are preconditions realistic and achievable?
- Do action effects actually modify state as expected?
- Are actions reporting correct execution status?

### State Management Debugging

**Key Debug Points:**
```python
# Monitor critical state variables
critical_state = {
    'canSeeEnemies': agent.State.get('canSeeEnemies'),
    'canSeeFood': agent.State.get('canSeeFood'), 
    'nearEnemy': agent.State.get('nearEnemy'),
    'nearFood': agent.State.get('nearFood'),
    'position': agent.State.get('position')
}
print(f"STATE DEBUG: {agent.Name} critical state: {critical_state}")
```

**What to Check:**
- Is state being updated by sensors correctly?
- Are actions modifying state as expected?
- Is state consistent between planning and execution?

## Debugging Insertion Points

### High-Level System Flow
1. **Agent.step()** - Entry point for each agent turn
2. **Planner.plan()** - Goal evaluation and A* search
3. **Agent._execute()** - Action sequence execution
4. **Action.execute()** - Individual action execution

### Detailed Investigation Points
1. **ActionGraph creation** - Are actions being generated with correct permutations?
2. **A* search loop** - Is the search exploring valid neighbors?
3. **Goal evaluation** - Is Utils.meets_goal() working correctly?
4. **Utility calculation** - Are valid plans being rejected due to math errors?

## Investigation Strategies by Symptom

### "Agents Never Act"
```python
# 1. Confirm agents are being processed
print(f"Processing agent {agent.Name}")

# 2. Check if planning is called
print(f"{agent.Name} calling planner")

# 3. Verify A* results
print(f"A* result for {goal.Name}: {cursor is not None}")

# 4. Check utility calculation
print(f"Plan utility: {utility}")
```

### "Wrong Actions Chosen"
```python
# 1. Check goal priorities
for goal in agent.Goals:
    print(f"Goal {goal.Name}: weight={goal.Weight}, valid={goal.is_valid(agent.State)}")

# 2. Verify action preconditions
for action in agent.Actions:
    print(f"Action {action.Name}: possible={action.is_possible(agent.State)}")

# 3. Trace A* path selection
print(f"A* chose path with cost {plan_cost} for goal {goal.Name}")
```

### "Inconsistent Behavior"
```python
# 1. Compare agent configurations
print(f"Agent {agent.Name}: {len(agent.Goals)} goals, {len(agent.Actions)} actions")

# 2. Check for state interference
print(f"Shared state references: {[id(agent.State) for agent in agents]}")

# 3. Monitor state changes
before_state = agent.State.copy()
# ... action execution ...
after_state = agent.State.copy()
changes = {k: (before_state.get(k), after_state.get(k)) 
          for k in set(before_state.keys()) | set(after_state.keys())
          if before_state.get(k) != after_state.get(k)}
print(f"State changes: {changes}")
```

## Quick Diagnostic Checklist

When agents aren't behaving correctly, check these in order:

### ✅ Basic System Health
- [ ] Are agents being processed each turn?
- [ ] Are sensors running and updating state?
- [ ] Is the planner being called?

### ✅ Planning System  
- [ ] Is A* finding solutions for any goals?
- [ ] Are goals valid for current state?
- [ ] Are action preconditions achievable?

### ✅ Execution System
- [ ] Are planned actions reaching execution?
- [ ] Are actions reporting correct status?
- [ ] Are action effects modifying state?

### ✅ Goal/Action Compatibility
- [ ] Do available actions actually achieve goal desired states?
- [ ] Are goal priorities set correctly?
- [ ] Are preconditions realistic given the world state?

## Common Gotchas in This Codebase

1. **Goal.is_valid() vs Goal priority**: Some goals may need both validity checks and priority calculations
2. **Action permutations**: Actions with permutation selectors may fail if selectors return empty lists
3. **State sharing**: Agents sharing references to the same state objects can cause interference
4. **Threading issues**: Async planning with state modifications can cause race conditions
5. **Utility calculation edge cases**: Division by zero, negative costs, or NaN values in utility math

## Performance Debugging

If the system is slow:
1. **A* search explosion**: Too many action permutations or poor heuristics
2. **Excessive replanning**: Agents replanning every turn instead of following sequences
3. **Sensor overhead**: Complex sensor calculations running too frequently
4. **Memory leaks**: ActionNode objects not being properly garbage collected

## Investigation Results Log

### Fix #8: Action.__eq__ and __hash__ Overrides ❌ **TESTED - PARTIAL EFFECT**

**Theory:** Python Action class uses name-based equality/hashing while C# uses reference equality, potentially breaking A* search.

**Test Method:** Removed Action.__eq__ and __hash__ methods to match C# reference equality behavior.

**Results:** 
- A* search behavior changed significantly - now explores many more nodes (queue overflow from 100k to 1M needed)
- Monster 1: Changed from "A* found solution" to "A* found NO solution" 
- Monster 2: Still finds zero-action plans for already-satisfied goals
- **Core Issue Persists:** Monsters still don't execute any actions (`sequences count: 0`)

**Conclusion:** Action equality was affecting A* search efficiency but is NOT the root cause of monsters not acting. The search space exploration improved but planning still fails.

**Next Investigation:** Need to focus on why A* finds "NO solution" for valid action chains (e.g., Monster 1 with `canSeeEnemies=True, nearEnemy=False` should be able to execute "Go To Enemy" action).

---

## Conclusion

GOAP debugging requires understanding the complete data flow from sensors through planning to execution. The key is isolating which component is failing and using targeted debugging at the appropriate insertion points. Always start with high-level symptoms and work down to specific component failures.

**Critical Lesson Learned:** Even when a fix appears to address a major architectural difference (like Action equality semantics), the core planning logic may still have deeper issues. Always verify that fixes actually resolve the end-to-end behavior, not just intermediate symptoms.