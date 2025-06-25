# JavaScript-Python Parity Requirements

This document outlines the requirements for achieving full parity between the JavaScript and Python versions of the RPG GOAP example.

## Current State

### Python Version Behavior
The Python version (`rpg_goap_python_example.example`) provides detailed console logging including:
- Turn-by-turn progression (`--- Turn X ---`)
- Agent action execution (`Player executing action: Go To Enemy`)
- Movement details (`Player moving toward Monster 5 from Vector2(10, 10) to Vector2(10, 11)`)
- Proximity events (`Player reached Monster 5!`)
- Combat results (`Player attacked Monster 5. Monster 5 HP: 1`)
- Agent deaths (`Monster 5 defeated! Agent Monster 5 has died.`)
- Health tracking (`Player HP: 79`)
- Food consumption (`Monster 2 ate food at Vector2(1, 11)`)
- Game completion (`Game finished.`)

### JavaScript Version Current Behavior
The JavaScript version (`src/example.js`) currently:
- Runs silently without console output
- Uses canvas for visual rendering only
- Executes GOAP logic correctly but provides no feedback
- Terminates after 10 turns without indication

## Required Changes for Full Parity

### 1. Console Logging Implementation
The JavaScript version needs to match the Python version's console output exactly:

```javascript
// Required logging patterns:
console.log(`--- Turn ${turn} ---`);
console.log(`${agent.name} executing action: ${action.name}`);
console.log(`${agent.name} moving toward ${target.name} from ${startPos} to ${endPos}`);
console.log(`${agent.name} reached ${target.name}!`);
console.log(`${attacker.name} attacked ${target.name}. ${target.name} HP: ${hp}`);
console.log(`${agent.name} defeated!`);
console.log(`Agent ${agent.name} has died.`);
console.log(`${agent.name} ate food at ${position}`);
console.log("Game finished.");
```

### 2. Action Execution Hooks
Implement detailed action logging by:
- Using `Action.registerOnBeginExecute()` and `Action.registerOnFinishExecute()` hooks
- Adding movement tracking in movement executors
- Adding combat result logging in combat executors
- Adding food consumption logging in eating executors

### 3. Game State Tracking
- Track agent health changes
- Monitor agent deaths and remove from active agents list
- Extend game duration to match Python version (30+ turns)
- Implement proper game termination conditions

### 4. Agent Behavior Details
- Log detailed movement paths and destinations
- Track proximity detection ("reached" events)
- Report action precondition failures
- Show goal priority switching

## Fixed Issues

### Import Error Resolution
**Issue**: `ExecutionStatus` was incorrectly imported from `actions.js` instead of `goals.js`
**Fix Applied**: Moved `ExecutionStatus` import to `goals.js` in `src/rpg/factories.js`

### Setup Scripts
**Added**: `setup.sh` and `run.sh` scripts for easier project setup and execution, matching the Python version's convenience scripts.

## Testing Requirements

The JavaScript version should produce output similar to this Python example:
```
--- Turn 1 ---
Player executing action: Go To Enemy
Player moving toward Monster 5 from Vector2(10, 10) to Vector2(10, 11)
Player reached Monster 5!
Monster 1 executing action: Go To Food
Monster 2 executing action: Eat
Monster 2 ate food at Vector2(1, 11)
...
```

## Success Criteria

- [ ] Console output matches Python version format
- [ ] All agent actions are logged with details
- [ ] Movement tracking shows start/end positions
- [ ] Combat results show HP changes
- [ ] Agent deaths are properly reported
- [ ] Game runs for comparable duration
- [ ] Food consumption is logged
- [ ] Game termination is announced

## Implementation Notes

- Use existing action execution hooks rather than modifying core GOAP logic
- Maintain visual canvas rendering alongside console logging
- Preserve existing agent behavior and game mechanics
- Follow JavaScript/Node.js console logging best practices

This parity will ensure both versions provide identical user experience and debugging capabilities.