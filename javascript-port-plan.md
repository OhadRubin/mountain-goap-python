# JavaScript/Node.js GOAP RPG Port Plan

## Overview
Port the Python GOAP RPG example to JavaScriptjavascript-port-plan.md/Node.js, maintaining the same architecture and functionality.

## Project Structure
```
rpg-goap-js/
├── package.json
├── src/
│   ├── goap/
│   │   ├── actions.js
│   │   ├── agent.js
│   │   ├── goals.js
│   │   ├── sensors.js
│   │   ├── planning.js
│   │   ├── utils.js
│   │   └── types.js
│   ├── rpg/
│   │   ├── utils.js
│   │   └── factories.js
│   └── example.js
└── README.md
```

## Implementation Steps

### 1. Setup Node.js Project
- Create package.json with dependencies (canvas for graphics)
- Set up ES6 modules structure

### 2. Port Core GOAP System
- **types.js**: Type definitions and interfaces
- **utils.js**: Priority queues, dictionary extensions, utility functions
- **actions.js**: Action class with execution, preconditions, effects
- **sensors.js**: Sensor class for world state monitoring  
- **goals.js**: Goal classes (Goal, ComparativeGoal, ExtremeGoal)
- **planning.js**: A* planner with ActionNode and ActionGraph
- **agent.js**: Main Agent class coordinating everything

### 3. Port RPG-Specific Code
- **rpg/utils.js**: Vector2 class, RpgUtils with distance/movement functions
- **rpg/factories.js**: PlayerFactory, RpgMonsterFactory with sensors/goals/actions

### 4. Create JavaScript Game Loop
- **example.js**: Main game using Node.js Canvas API
- Grid-based rendering similar to pygame version
- Game loop with timed updates (200ms intervals)
- Agent stepping and death processing

### 5. Key JavaScript Adaptations
- Replace Python threads/locks with JavaScript async patterns
- Use Map/Set for efficient lookups instead of Python dictionaries
- Implement priority queue with proper JavaScript semantics
- Handle JavaScript's different number/boolean type behavior
- Use canvas-based rendering instead of pygame

## Technical Considerations
- Use ES6 classes and modules
- Implement proper error handling
- Maintain the same GOAP architecture patterns
- Keep the same game mechanics and AI behavior
- Add TypeScript definitions for better development experience (optional)

## Dependencies
```json
{
  "canvas": "^2.11.2",
  "node-canvas": "^2.11.2"
}
```

## Key Differences from Python Version
1. **Threading**: JavaScript uses event loop instead of threads
2. **Type System**: JavaScript's dynamic typing vs Python's gradual typing
3. **Graphics**: Canvas API instead of pygame
4. **Modules**: ES6 imports instead of Python imports
5. **Data Structures**: JavaScript Map/Set vs Python dict/set