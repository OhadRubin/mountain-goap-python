
I will provide the Python equivalent of each C# file, preserving the structure and variable names as much as possible. Since Python is dynamically typed and doesn't have direct equivalents for some C# features (like `ConcurrentDictionary` with exactly the same semantics, or `MethodImplOptions.AggressiveInlining`), I will use the closest Pythonic alternatives. For `ConcurrentDictionary`, a standard `dict` will be used, and for `FastPriorityQueue`, I'll use a basic list-based min-heap implementation as a stand-in, as a direct verbatim translation of that C# library is quite extensive and beyond the scope of a direct port.

Let's start with the directory structure:

```
.
├── MountainGoap
│   ├── Action.py
│   ├── Agent.py
│   ├── BaseGoal.py
│   ├── CallbackDelegates
│   │   ├── CostCallback.py
│   │   ├── ExecutorCallback.py
│   │   ├── PermutationSelectorCallback.py
│   │   ├── SensorRunCallback.py
│   │   ├── StateCheckerCallback.py
│   │   ├── StateCostDeltaMultiplierCallback.py
│   │   └── StateMutatorCallback.py
│   ├── ComparativeGoal.py
│   ├── ComparisonOperator.py
│   ├── ComparisonValuePair.py
│   ├── Events
│   │   ├── AgentActionSequenceCompletedEvent.py
│   │   ├── AgentStepEvent.py
│   │   ├── BeginExecuteActionEvent.py
│   │   ├── EvaluatedActionNodeEvent.py
│   │   ├── FinishExecuteActionEvent.py
│   │   ├── PlanUpdatedEvent.py
│   │   ├── PlanningFinishedEvent.py
│   │   ├── PlanningFinishedForSingleGoalEvent.py
│   │   ├── PlanningStartedEvent.py
│   │   ├── PlanningStartedForSingleGoalEvent.py
│   │   └── SensorRunningEvent.py
│   ├── ExecutionStatus.py
│   ├── ExtremeGoal.py
│   ├── Goal.py
│   ├── Internals
│   │   ├── ActionAStar.py
│   │   ├── ActionGraph.py
│   │   ├── ActionNode.py
│   │   ├── DictionaryExtensionMethods.py
│   │   ├── Planner.py
│   │   └── Utils.py
│   ├── PermutationSelectorGenerators.py
│   ├── PriorityQueue # Simplified Python implementation
│   │   ├── FastPriorityQueue.py
│   │   ├── FastPriorityQueueNode.py
│   │   ├── GenericPriorityQueue.py
│   │   ├── GenericPriorityQueueNode.py
│   │   ├── IFixedSizePriorityQueue.py
│   │   ├── IPriorityQueue.py
│   │   ├── SimplePriorityQueue.py
│   │   ├── StablePriorityQueue.py
│   │   └── StablePriorityQueueNode.py
│   ├── Sensor.py
│   └── StepMode.py
├── MountainGoapLogging
│   └── DefaultLogger.py
└── MountainGoapTest # Basic Python tests (pytest compatible)
    ├── ActionContinuationTests.py
    ├── ActionNodeTests.py
    ├── ArithmeticPostconditionsTests.py
    ├── PermutationSelectorGeneratorTests.py
    ├── PermutationSelectorTests.py
    └── conftest.py # for global imports like Xunit equivalent
```

**Note on `MountainGoap.sln`, `.csproj`, `.nuspec`, `.snk`, `packages.config`, and `stylecop.json` files:** These are specific to C#/.NET projects (solution files, project files, NuGet package specifications, strong name keys, and code style configuration). They do not have direct verbatim equivalents in a Python project. Their functionality (like dependency management, project structure) is handled differently in Python (e.g., `requirements.txt`, `setup.py`, direct imports, virtual environments). Therefore, these files will not be translated.

---

**MountainGoap/CallbackDelegates/CostCallback.py**

```python
# // <copyright file="CostCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import TYPE_CHECKING, Callable, Dict, Any

# if TYPE_CHECKING:
#     from ..Action import Action
#     from collections import UserDict # This is for type hinting a dictionary-like object

# /// <summary>
# /// Delegate type for a callback that defines the cost of an action.
# /// </summary>
# /// <param name="action">Action being executed.</param>
# /// <param name="currentState">State as it will be when cost is relevant.</param>
# /// <returns>Cost of the action.</returns>
# public delegate float CostCallback(Action action, ConcurrentDictionary<string, object?> currentState);

from typing import Callable, Dict, Any

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The first parameter is 'Action' (forward reference)
# The second parameter is 'StateDictionary'
# The return type is float
CostCallback = Callable[['Action', StateDictionary], float]

```

---

**MountainGoap/CallbackDelegates/ExecutorCallback.py**

```python
# // <copyright file="ExecutorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import TYPE_CHECKING, Callable

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..Action import Action
#     from ..ExecutionStatus import ExecutionStatus

# /// <summary>
# /// Delegate type for a callback that defines a list of all possible parameter states for the given state.
# /// </summary>
# /// <param name="agent">Agent executing the action.</param>
# /// <param name="action">Action being executed.</param>
# /// <returns>New execution status of the action.</returns>
# public delegate ExecutionStatus ExecutorCallback(Agent agent, Action action);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action
    from ..ExecutionStatus import ExecutionStatus

# Define the delegate type using Callable
# The first parameter is 'Agent' (forward reference)
# The second parameter is 'Action' (forward reference)
# The return type is 'ExecutionStatus' (forward reference)
ExecutorCallback = Callable[['Agent', 'Action'], 'ExecutionStatus']

```

---

**MountainGoap/CallbackDelegates/PermutationSelectorCallback.py**

```python
# // <copyright file="PermutationSelectorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, Any, List

# /// <summary>
# /// Delegate type for a callback that defines a list of all possible parameter states for the given state.
# /// </summary>
# /// <param name="state">Current world state.</param>
# /// <returns>A list with each parameter set to be tried for the action.</returns>
# public delegate List<object> PermutationSelectorCallback(ConcurrentDictionary<string, object?> state);

from typing import Callable, Dict, Any, List

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The parameter is 'StateDictionary'
# The return type is List[Any] (list of objects)
PermutationSelectorCallback = Callable[[StateDictionary], List[Any]]

```

---

**MountainGoap/CallbackDelegates/SensorRunCallback.py**

```python
# // <copyright file="SensorRunCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent

# /// <summary>
# /// Delegate type for a callback that runs a sensor during a game loop.
# /// </summary>
# /// <param name="agent">Agent using the sensor.</param>
# /// <returns>The execution status of the action.</returns>
# public delegate void SensorRunCallback(Agent agent);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

# Define the delegate type using Callable
# The parameter is 'Agent' (forward reference)
# The return type is None (void in C#)
SensorRunCallback = Callable[['Agent'], None]

```

---

**MountainGoap/CallbackDelegates/StateCheckerCallback.py**

```python
# // <copyright file="StateCheckerCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, Any, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Action import Action

# /// <summary>
# /// Delegate type for a callback that checks state before action execution or evaluation (the latter during planning).
# /// </summary>
# /// <param name="action">Action being executed or evaluated.</param>
# /// <param name="currentState">State as it will be when the action is executed or evaluated.</param>
# /// <returns>True if the state is okay for executing the action, otherwise false.</returns>
# public delegate bool StateCheckerCallback(Action action, ConcurrentDictionary<string, object?> currentState);

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Action import Action

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The first parameter is 'Action' (forward reference)
# The second parameter is 'StateDictionary'
# The return type is bool
StateCheckerCallback = Callable[['Action', StateDictionary], bool]

```

---

**MountainGoap/CallbackDelegates/StateCostDeltaMultiplierCallback.py**

```python
# // <copyright file="StateMutatorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Action import Action

# /// <summary>
# /// Delegate type for a callback that provides multiplier for delta value of the respective key to obtain delta cost to use with ExtremeGoal and ComparativeGoal.
# /// </summary>
# /// <param name="action">Action being executed or evaluated.</param>
# /// <param name="stateKey">Key to provide multiplier for</param>
# /// <returns>Multiplier for the delta value to get delta cost</returns>
# public delegate float StateCostDeltaMultiplierCallback(Action? action, string stateKey);

from typing import Callable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..Action import Action

# Define the delegate type using Callable
# The first parameter is Optional['Action'] (forward reference for Action or None)
# The second parameter is str
# The return type is float
StateCostDeltaMultiplierCallback = Callable[[Optional['Action'], str], float]

```

---

**MountainGoap/CallbackDelegates/StateMutatorCallback.py**

```python
# // <copyright file="StateMutatorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, Any, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Action import Action

# /// <summary>
# /// Delegate type for a callback that mutates state following action execution or evaluation (the latter during planning).
# /// </summary>
# /// <param name="action">Action being executed or evaluated.</param>
# /// <param name="currentState">State as it will be when the action is executed or evaluated.</param>
# /// <returns>The execution status of the action.</returns>
# public delegate void StateMutatorCallback(Action action, ConcurrentDictionary<string, object?> currentState);

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Action import Action

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The first parameter is 'Action' (forward reference)
# The second parameter is 'StateDictionary'
# The return type is None (void in C#)
StateMutatorCallback = Callable[['Action', StateDictionary], None]

```

---

**MountainGoap/Events/AgentActionSequenceCompletedEvent.py**

```python
# // <copyright file="AgentActionSequenceCompletedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent completes an action sequence.
# /// </summary>
# /// <param name="agent">Agent executing the action sequence.</param>
# public delegate void AgentActionSequenceCompletedEvent(Agent agent);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

AgentActionSequenceCompletedEvent = Callable[['Agent'], None]

```

---

**MountainGoap/Events/AgentStepEvent.py**

```python
# // <copyright file="AgentStepEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent executes a step of work.
# /// </summary>
# /// <param name="agent">Agent executing the step of work.</param>
# public delegate void AgentStepEvent(Agent agent);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

AgentStepEvent = Callable[['Agent'], None]

```

---

**MountainGoap/Events/BeginExecuteActionEvent.py**

```python
# // <copyright file="BeginExecuteActionEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, Any, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..Action import Action

# /// <summary>
# /// Delegate type for a listener to the event that fires when an action begins executing.
# /// </summary>
# /// <param name="agent">Agent executing the action.</param>
# /// <param name="action">Action being executed.</param>
# /// <param name="parameters">Parameters to the action being executed.</param>
# public delegate void BeginExecuteActionEvent(Agent agent, Action action, Dictionary<string, object?> parameters);

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action

BeginExecuteActionEvent = Callable[['Agent', 'Action', Dict[str, Any]], None]

```

---

**MountainGoap/Events/EvaluatedActionNodeEvent.py**

```python
# // <copyright file="EvaluatedActionNodeEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Internals.ActionNode import ActionNode

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent is evaluating a path for a potential action plan.
# /// </summary>
# /// <param name="node">Node being evaluated.</param>
# /// <param name="nodes">All nodes in the plan being evaluated.</param>
# public delegate void EvaluatedActionNodeEvent(ActionNode node, ConcurrentDictionary<ActionNode, ActionNode> nodes);

from typing import Callable, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Internals.ActionNode import ActionNode

EvaluatedActionNodeEvent = Callable[['ActionNode', Dict['ActionNode', 'ActionNode']], None]

```

---

**MountainGoap/Events/FinishExecuteActionEvent.py**

```python
# // <copyright file="FinishExecuteActionEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Dict, Any, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..Action import Action
#     from ..ExecutionStatus import ExecutionStatus

# /// <summary>
# /// Delegate type for a listener to the event that fires when an action finishes executing.
# /// </summary>
# /// <param name="agent">Agent executing the action.</param>
# /// <param name="action">Action being executed.</param>
# /// <param name="status">Execution status of the action.</param>
# /// <param name="parameters">Parameters to the action being executed.</param>
# public delegate void FinishExecuteActionEvent(Agent agent, Action action, ExecutionStatus status, Dictionary<string, object?> parameters);

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action
    from ..ExecutionStatus import ExecutionStatus

FinishExecuteActionEvent = Callable[['Agent', 'Action', 'ExecutionStatus', Dict[str, Any]], None]

```

---

**MountainGoap/Events/PlanUpdatedEvent.py**

```python
# // <copyright file="PlanUpdatedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, List, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..Action import Action

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent has a new plan.
# /// </summary>
# /// <param name="agent">Agent executing the step of work.</param>
# /// <param name="plan">Plan determined to be optimal for the agent.</param>
# public delegate void PlanUpdatedEvent(Agent agent, List<Action> plan);

from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action

PlanUpdatedEvent = Callable[['Agent', List['Action']], None]

```

---

**MountainGoap/Events/PlanningFinishedEvent.py**

```python
# // <copyright file="PlanningFinishedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, Optional, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..BaseGoal import BaseGoal

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent finishes planning.
# /// </summary>
# /// <param name="agent">Agent doing the planning.</param>
# /// /// <param name="goal">Goal selected, or null if no valid plan was selected.</param>
# /// <param name="utility">Calculated utility of the plan.</param>
# public delegate void PlanningFinishedEvent(Agent agent, BaseGoal? goal, float utility);

from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..BaseGoal import BaseGoal

PlanningFinishedEvent = Callable[['Agent', Optional['BaseGoal'], float], None]

```

---

**MountainGoap/Events/PlanningFinishedForSingleGoalEvent.py**

```python
# // <copyright file="PlanningFinishedForSingleGoalEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..BaseGoal import BaseGoal

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent finishes planning for a single goal.
# /// </summary>
# /// <param name="agent">Agent doing the planning.</param>
# /// <param name="goal">Goal for which planning was finished.</param>
# /// <param name="utility">Calculated utility of the plan.</param>
# public delegate void PlanningFinishedForSingleGoalEvent(Agent agent, BaseGoal goal, float utility);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..BaseGoal import BaseGoal

PlanningFinishedForSingleGoalEvent = Callable[['Agent', 'BaseGoal', float], None]

```

---

**MountainGoap/Events/PlanningStartedEvent.py**

```python
# // <copyright file="PlanningStartedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent begins planning.
# /// </summary>
# /// <param name="agent">Agent doing the planning.</param>
# public delegate void PlanningStartedEvent(Agent agent);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

PlanningStartedEvent = Callable[['Agent'], None]

```

---

**MountainGoap/Events/PlanningStartedForSingleGoalEvent.py**

```python
# // <copyright file="PlanningStartedForSingleGoalEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..BaseGoal import BaseGoal

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent starts planning for a single goal.
# /// </summary>
# /// <param name="agent">Agent doing the planning.</param>
# /// <param name="goal">Goal for which planning was started.</param>
# public delegate void PlanningStartedForSingleGoalEvent(Agent agent, BaseGoal goal);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..BaseGoal import BaseGoal

PlanningStartedForSingleGoalEvent = Callable[['Agent', 'BaseGoal'], None]

```

---

**MountainGoap/Events/SensorRunningEvent.py**

```python
# // <copyright file="SensorRunningEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# from typing import Callable, TYPE_CHECKING

# if TYPE_CHECKING:
#     from ..Agent import Agent
#     from ..Sensor import Sensor

# /// <summary>
# /// Delegate type for a listener to the event that fires when an agent sensor is about to run.
# /// </summary>
# /// <param name="agent">Agent running the sensor.</param>
# /// <param name="sensor">Sensor that is about to run.</param>
# public delegate void SensorRunEvent(Agent agent, Sensor sensor);

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Sensor import Sensor

SensorRunEvent = Callable[['Agent', 'Sensor'], None]

```

---

**MountainGoap/BaseGoal.py**

```python
# // <copyright file="BaseGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid

# /// <summary>
# /// Represents an abstract class for a goal to be achieved for an agent.
# /// </summary>
class BaseGoal:
    """
    Represents an abstract class for a goal to be achieved for an agent.
    """

    # /// <summary>
    # /// Name of the goal.
    # /// </summary>
    # public readonly string Name;
    Name: str

    # /// <summary>
    # /// Weight to give the goal.
    # /// </summary>
    # internal readonly float Weight;
    Weight: float

    # /// <summary>
    # /// Initializes a new instance of the <see cref="BaseGoal"/> class.
    # /// </summary>
    # /// <param name="name">Name of the goal.</param>
    # /// <param name="weight">Weight to give the goal.</param>
    # protected BaseGoal(string? name = null, float weight = 1f) {
    #     Name = name ?? $"Goal {Guid.NewGuid()}";
    #     Weight = weight;
    # }
    def __init__(self, name: str = None, weight: float = 1.0):
        """
        Initializes a new instance of the BaseGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
        """
        self.Name = name if name is not None else f"Goal {uuid.uuid4()}"
        self.Weight = weight

```

---

**MountainGoap/ComparisonOperator.py**

```python
# // <copyright file="ComparisonOperator.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

# /// <summary>
# /// List of operators that can be used for comparison.
# /// </summary>
class ComparisonOperator(Enum):
    """
    List of operators that can be used for comparison.
    """

    # /// <summary>
    # /// Undefined comparison operator (will not do anything).
    # /// </summary>
    # Undefined = 0,
    Undefined = 0

    # /// <summary>
    # /// Equality (==) operator.
    # /// </summary>
    # Equals = 1,
    Equals = 1

    # /// <summary>
    # /// Less than (<) operator.
    # /// </summary>
    # LessThan = 2

    LessThan = 2

    # /// <summary>
    # /// Less than or equals (<=) operator.
    # /// </summary>
    # LessThanOrEquals = 3
    LessThanOrEquals = 3

    # /// <summary>
    # /// Greater than (>) operator).
    # /// </summary>
    # GreaterThan = 4
    GreaterThan = 4

    # /// <summary>
    # /// Greater than or equals (>=) operator.
    # /// </summary>
    # GreaterThanOrEquals = 5
    GreaterThanOrEquals = 5

```

---

**MountainGoap/ComparisonValuePair.py**

```python
# // <copyright file="ComparisonValuePair.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Any, Optional
from .ComparisonOperator import ComparisonOperator

# /// <summary>
# /// List of operators that can be used for comparison.
# /// </summary>
class ComparisonValuePair:
    """
    List of operators that can be used for comparison.
    """

    # /// <summary>
    # /// Gets or sets the value to be compared against.
    # /// </summary>
    # public object? Value { get; set; } = null;
    Value: Optional[Any] = None

    # /// <summary>
    # /// Gets or sets the operator to be used for comparison.
    # /// </summary>
    # public ComparisonOperator Operator { get; set; } = ComparisonOperator.Undefined;
    Operator: ComparisonOperator = ComparisonOperator.Undefined

    def __init__(self, value: Optional[Any] = None, operator: ComparisonOperator = ComparisonOperator.Undefined):
        self.Value = value
        self.Operator = operator

```

---

**MountainGoap/ComparativeGoal.py**

```python
# // <copyright file="ComparativeGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Optional
from .BaseGoal import BaseGoal
from .ComparisonValuePair import ComparisonValuePair

# /// <summary>
# /// Represents a goal to be achieved for an agent.
# /// </summary>
class ComparativeGoal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    # /// <summary>
    # /// Desired state for the comparative goal.
    # /// </summary>
    # internal readonly Dictionary<string, ComparisonValuePair> DesiredState;
    DesiredState: Dict[str, ComparisonValuePair]

    # /// <summary>
    # /// Initializes a new instance of the <see cref="ComparativeGoal"/> class.
    # /// </summary>
    # /// <param name="name">Name of the goal.</param>
    # /// <param name="weight">Weight to give the goal.</param>
    # /// <param name="desiredState">Desired state for the comparative goal.</param>
    # public ComparativeGoal(string? name = null, float weight = 1f, Dictionary<string, ComparisonValuePair>? desiredState = null)
    #     : base(name, weight) {
    #     DesiredState = desiredState ?? new();
    # }
    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, ComparisonValuePair]] = None):
        """
        Initializes a new instance of the ComparativeGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: Desired state for the comparative goal.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

```

---

**MountainGoap/ExecutionStatus.py**

```python
# // <copyright file="ExecutionStatus.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

# /// <summary>
# /// Possible execution status for an action.
# /// </summary>
class ExecutionStatus(Enum):
    """
    Possible execution status for an action.
    """

    # /// <summary>
    # /// Indicates that the action is not currently executing.
    # /// </summary>
    # NotYetExecuted = 1
    NotYetExecuted = 1

    # /// <summary>
    # /// Indicates that the action is currently executing.
    # /// </summary>
    # Executing = 2
    Executing = 2

    # /// <summary>
    # /// Indicates that the action has succeeded.
    # /// </summary>
    # Succeeded = 3
    Succeeded = 3

    # /// <summary>
    # /// Indicates that the action has failed.
    # /// </summary>
    # Failed = 4
    Failed = 4

    # /// <summary>
    # /// Indicates that the action is not possible due to preconditions.
    # /// </summary>
    # NotPossible = 5
    NotPossible = 5

```

---

**MountainGoap/ExtremeGoal.py**

```python
# // <copyright file="ExtremeGoal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Optional
from .BaseGoal import BaseGoal

# /// <summary>
# /// Represents a goal requiring an extreme value to be achieved for an agent.
# /// </summary>
class ExtremeGoal(BaseGoal):
    """
    Represents a goal requiring an extreme value to be achieved for an agent.
    """

    # /// <summary>
    # /// Dictionary of states to be maximized or minimized. A value of true indicates to maximize the goal, a value of false indicates to minimize it.
    # /// </summary>
    # internal readonly Dictionary<string, bool> DesiredState;
    DesiredState: Dict[str, bool]

    # /// <summary>
    # /// Initializes a new instance of the <see cref="ExtremeGoal"/> class.
    # /// </summary>
    # /// <param name="name">Name of the goal.</param>
    # /// <param name="weight">Weight to give the goal.</param>
    # /// <param name="desiredState">States to be maximized or minimized.</param>
    # public ExtremeGoal(string? name = null, float weight = 1f, Dictionary<string, bool>? desiredState = null)
    #     : base(name, weight) {
    #     DesiredState = desiredState ?? new();
    # }
    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, bool]] = None):
        """
        Initializes a new instance of the ExtremeGoal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: States to be maximized or minimized.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

```

---

**MountainGoap/Goal.py**

```python
# // <copyright file="Goal.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional
from .BaseGoal import BaseGoal

# /// <summary>
# /// Represents a goal to be achieved for an agent.
# /// </summary>
class Goal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    # /// <summary>
    # /// Desired world state to be achieved.
    # /// </summary>
    # internal readonly Dictionary<string, object?> DesiredState;
    DesiredState: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Initializes a new instance of the <see cref="Goal"/> class.
    # /// </summary>
    # /// <param name="name">Name of the goal.</param>
    # /// <param name="weight">Weight to give the goal.</param>
    # /// <param name="desiredState">Desired end state of the goal.</param>
    # public Goal(string? name = null, float weight = 1f, Dictionary<string, object?>? desiredState = null)
    #     : base(name, weight) {
    #     DesiredState = desiredState ?? new();
    # }
    def __init__(self, name: Optional[str] = None, weight: float = 1.0,
                 desired_state: Optional[Dict[str, Optional[Any]]] = None):
        """
        Initializes a new instance of the Goal class.

        Args:
            name: Name of the goal.
            weight: Weight to give the goal.
            desired_state: Desired end state of the goal.
        """
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}

```

---

**MountainGoap/StepMode.py**

```python
# // <copyright file="StepMode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

# /// <summary>
# /// Different modes with which MountainGoap can execute an agent step.
# /// </summary>
class StepMode(Enum):
    """
    Different modes with which MountainGoap can execute an agent step.
    """

    # /// <summary>
    # /// Default step mode. Runs async, doesn't necessitate taking action.
    # /// </summary>
    # Default = 1
    Default = 1

    # /// <summary>
    # /// Turn-based step mode, plans synchronously, executes at least one action if possible.
    # /// </summary>
    # OneAction = 2
    OneAction = 2

    # /// <summary>
    # /// Turn-based step mode, plans synchronously, executes all actions in planned action sequence.
    # /// </summary>
    # AllActions = 3
    AllActions = 3

```

---

**MountainGoap/Internals/DictionaryExtensionMethods.py**

```python
# // <copyright file="DictionaryExtensionMethods.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List
from ..ComparisonValuePair import ComparisonValuePair

# /// <summary>
# /// Extension method to copy a dictionary of strings and objects.
# /// </summary>
class DictionaryExtensionMethods:
    """
    Extension method to copy a dictionary of strings and objects.
    In Python, this will be implemented as static methods since there are no true extension methods.
    """

    # /// <summary>
    # /// Copies the dictionary to a shallow clone.
    # /// </summary>
    # /// <param name="dictionary">Dictionary to be copied.</param>
    # /// <returns>A shallow copy of the dictionary.</returns>
    # internal static Dictionary<string, object?> Copy(this Dictionary<string, object?> dictionary) {
    #     return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
    # }
    @staticmethod
    def copy_dict(dictionary: Dict[str, Optional[Any]]) -> Dict[str, Optional[Any]]:
        """
        Copies the dictionary to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    # /// <summary>
    # /// Copies the concurrent dictionary to a shallow clone.
    # /// </summary>
    # /// <param name="dictionary">Dictionary to be copied.</param>
    # /// <returns>A shallow copy of the dictionary.</returns>
    # internal static ConcurrentDictionary<string, object?> Copy(this ConcurrentDictionary<string, object?> dictionary) {
    #     return new ConcurrentDictionary<string, object?>(dictionary);
    # }
    # In Python, standard dict is generally thread-safe for basic operations, and
    # for more complex concurrent updates, a Lock or queue would be used.
    # For a direct equivalent, we'll just use a standard dict copy.
    @staticmethod
    def copy_concurrent_dict(dictionary: Dict[str, Optional[Any]]) -> Dict[str, Optional[Any]]:
        """
        Copies the (conceptually) concurrent dictionary to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    # /// <summary>
    # /// Copies the dictionary to a shallow clone.
    # /// </summary>
    # /// <param name="dictionary">Dictionary to be copied.</param>
    # /// <returns>A shallow copy of the dictionary.</returns>
    # internal static Dictionary<string, ComparisonValuePair> Copy(this Dictionary<string, ComparisonValuePair> dictionary) {
    #     return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
    # }
    @staticmethod
    def copy_comparison_value_pair_dict(dictionary: Dict[str, ComparisonValuePair]) -> Dict[str, ComparisonValuePair]:
        """
        Copies the dictionary of ComparisonValuePair to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    # /// <summary>
    # /// Copies the dictionary to a shallow clone.
    # /// </summary>
    # /// <param name="dictionary">Dictionary to be copied.</param>
    # /// <returns>A shallow copy of the dictionary.</returns>
    # internal static Dictionary<string, string> Copy(this Dictionary<string, string> dictionary) {
    #     return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
    # }
    @staticmethod
    def copy_string_dict(dictionary: Dict[str, str]) -> Dict[str, str]:
        """
        Copies the dictionary of strings to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    # /// <summary>
    # /// Copies the dictionary to a shallow clone.
    # /// </summary>
    # /// <param name="dictionary">Dictionary to be copied.</param>
    # /// <returns>A shallow copy of the dictionary.</returns>
    # internal static Dictionary<string, object> CopyNonNullable(this Dictionary<string, object> dictionary) {
    #     return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
    # }
    @staticmethod
    def copy_non_nullable_dict(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Copies the dictionary of non-nullable objects to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

```

---

**MountainGoap/PriorityQueue/FastPriorityQueueNode.py**

```python
# // <copyright file="FastPriorityQueueNode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

# /// <summary>
# /// Base class for nodes in FastPriorityQueue.
# /// </summary>
class FastPriorityQueueNode:
    """
    Base class for nodes in FastPriorityQueue.
    """

    # /// <summary>
    # /// The Priority to insert this node at.
    # /// Cannot be manually edited - see queue.Enqueue() and queue.UpdatePriority() instead
    # /// </summary>
    # public float Priority { get; protected internal set; }
    Priority: float

    # /// <summary>
    # /// Represents the current position in the queue
    # /// </summary>
    # public int QueueIndex { get; internal set; }
    QueueIndex: int

    # #if DEBUG
    # /// <summary>
    # /// The queue this node is tied to. Used only for debug builds.
    # /// </summary>
    # public object Queue { get; internal set; }
    # #endif
    _queue: object = None # Internal reference to the queue for debugging/validation

    def __init__(self):
        self.Priority = 0.0
        self.QueueIndex = 0

```

---

**MountainGoap/PriorityQueue/GenericPriorityQueueNode.py**

```python
# // <copyright file="GenericPriorityQueueNode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

from typing import TypeVar, Any

TPriority = TypeVar('TPriority')

# /// <summary>
# /// Base class for nodes in GenericPriorityQueue.
# /// </summary>
class GenericPriorityQueueNode(FastPriorityQueueNode): # Inherit from FastPriorityQueueNode (or a common base)
    """
    Base class for nodes in GenericPriorityQueue.
    """
    # /// <summary>
    # /// The Priority to insert this node at.
    # /// Cannot be manually edited - see queue.Enqueue() and queue.UpdatePriority() instead
    # /// </summary>
    # public TPriority Priority { get; protected internal set; }
    Priority: TPriority

    # /// <summary>
    # /// Represents the current position in the queue
    # /// </summary>
    # public int QueueIndex { get; internal set; }
    QueueIndex: int # Inherited from FastPriorityQueueNode

    # /// <summary>
    # /// Represents the order the node was inserted in
    # /// </summary>
    # public long InsertionIndex { get; internal set; }
    InsertionIndex: int # Using int for simplicity instead of long

    # #if DEBUG
    # /// <summary>
    # /// The queue this node is tied to. Used only for debug builds.
    # /// </summary>
    # public object Queue { get; internal set; }
    # #endif
    _queue: Any = None # Internal reference to the queue for debugging/validation

    def __init__(self):
        super().__init__()
        self.Priority = None # type: ignore # Will be set by the queue
        self.InsertionIndex = 0

```

---

**MountainGoap/PriorityQueue/StablePriorityQueueNode.py**

```python
# // <copyright file="StablePriorityQueueNode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

from .FastPriorityQueueNode import FastPriorityQueueNode

# /// <summary>
# /// Base class for nodes in StablePriorityQueue.
# /// </summary>
class StablePriorityQueueNode(FastPriorityQueueNode):
    """
    Base class for nodes in StablePriorityQueue.
    """

    # /// <summary>
    # /// Represents the order the node was inserted in
    # /// </summary>
    # public long InsertionIndex { get; internal set; }
    InsertionIndex: int # Using int for simplicity instead of long

    def __init__(self):
        super().__init__()
        self.InsertionIndex = 0

```

---

**MountainGoap/PriorityQueue/IPriorityQueue.py**

```python
# // <copyright file="IPriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterable

TItem = TypeVar('TItem')
TPriority = TypeVar('TPriority')

# /// <summary>
# /// The IPriorityQueue interface.  This is mainly here for purists, and in case I decide to add more implementations later.
# /// For speed purposes, it is actually recommended that you *don't* access the priority queue through this interface, since the JIT can
# /// (theoretically?) optimize method calls from concrete-types slightly better.
# /// </summary>
class IPriorityQueue(ABC, Generic[TItem, TPriority], Iterable[TItem]):
    """
    The IPriorityQueue interface.
    """

    # /// <summary>
    # /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken by first-in-first-out.
    # /// See implementation for how duplicates are handled.
    # /// </summary>
    # void Enqueue(TItem node, TPriority priority);
    @abstractmethod
    def enqueue(self, node: TItem, priority: TPriority) -> None:
        """
        Enqueue a node to the priority queue. Lower values are placed in front.
        """
        pass

    # /// <summary>
    # /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
    # /// </summary>
    # TItem Dequeue();
    @abstractmethod
    def dequeue(self) -> TItem:
        """
        Removes the head of the queue (node with minimum priority), and returns it.
        """
        pass

    # /// <summary>
    # /// Removes every node from the queue.
    # /// </summary>
    # void Clear();
    @abstractmethod
    def clear(self) -> None:
        """
        Removes every node from the queue.
        """
        pass

    # /// <summary>
    # /// Returns whether the given node is in the queue.
    # /// </summary>
    # bool Contains(TItem node);
    @abstractmethod
    def contains(self, node: TItem) -> bool:
        """
        Returns whether the given node is in the queue.
        """
        pass

    # /// <summary>
    # /// Removes a node from the queue. The node does not need to be the head of the queue.
    # /// </summary>
    # void Remove(TItem node);
    @abstractmethod
    def remove(self, node: TItem) -> None:
        """
        Removes a node from the queue.
        """
        pass

    # /// <summary>
    # /// Call this method to change the priority of a node.
    # /// </summary>
    # void UpdatePriority(TItem node, TPriority priority);
    @abstractmethod
    def update_priority(self, node: TItem, priority: TPriority) -> None:
        """
        Call this method to change the priority of a node.
        """
        pass

    # /// <summary>
    # /// Returns the head of the queue, without removing it (use Dequeue() for that).
    # /// </summary>
    # TItem First { get; }
    @property
    @abstractmethod
    def first(self) -> TItem:
        """
        Returns the head of the queue, without removing it.
        """
        pass

    # /// <summary>
    # /// Returns the number of nodes in the queue.
    # /// </summary>
    # int Count { get; }
    @property
    @abstractmethod
    def count(self) -> int:
        """
        Returns the number of nodes in the queue.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterable[TItem]:
        pass

```

---

**MountainGoap/PriorityQueue/IFixedSizePriorityQueue.py**

```python
# // <copyright file="IFixedSizePriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

from abc import abstractmethod
from typing import TypeVar, Generic
from .IPriorityQueue import IPriorityQueue

TItem = TypeVar('TItem')
TPriority = TypeVar('TPriority')

# /// <summary>
# /// A helper-interface only needed to make writing unit tests a bit easier (hence the 'internal' access modifier)
# /// </summary>
class IFixedSizePriorityQueue(IPriorityQueue[TItem, TPriority], Generic[TItem, TPriority]):
    """
    A helper-interface for fixed-size priority queues.
    """

    # /// <summary>
    # /// Resize the queue so it can accept more nodes. All currently enqueued nodes are remain.
    # /// Attempting to decrease the queue size to a size too small to hold the existing nodes results in undefined behavior
    # /// </summary>
    # void Resize(int maxNodes);
    @abstractmethod
    def resize(self, max_nodes: int) -> None:
        """
        Resize the queue so it can accept more nodes.
        """
        pass

    # /// <summary>
    # /// Returns the maximum number of items that can be enqueued at once in this queue. Once you hit this number (ie. once Count == MaxSize),
    # /// attempting to enqueue another item will cause undefined behavior.
    # /// </summary>
    # int MaxSize { get; }
    @property
    @abstractmethod
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue.
        """
        pass

    # /// <summary>
    # /// By default, nodes that have been previously added to one queue cannot be added to another queue.
    # /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
    # /// </summary>
    # void ResetNode(TItem node);
    @abstractmethod
    def reset_node(self, node: TItem) -> None:
        """
        Resets a node's internal state to allow it to be reused in another queue.
        """
        pass

```

---

**MountainGoap/PriorityQueue/FastPriorityQueue.py**

```python
# // <copyright file="FastPriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

import heapq
from typing import TypeVar, List, Dict, Any, Optional, Iterable

from .FastPriorityQueueNode import FastPriorityQueueNode
from .IFixedSizePriorityQueue import IFixedSizePriorityQueue

T = TypeVar('T', bound=FastPriorityQueueNode)

# /// <summary>
# /// An implementation of a min-Priority Queue using a heap.  Has O(1) .Contains()!
# /// See https://github.com/BlueRaja/High-Speed-Priority-Queue-for-C-Sharp/wiki/Getting-Started for more information
# /// </summary>
# /// <typeparam name="T">The values in the queue.  Must extend the FastPriorityQueueNode class</typeparam>
class FastPriorityQueue(IFixedSizePriorityQueue[T, float]):
    """
    An implementation of a min-Priority Queue using a heap.
    This is a simplified Python implementation using heapq.
    """

    _num_nodes: int
    _nodes: List[Optional[T]] # Using a list as the heap
    _node_to_index: Dict[T, int] # For O(1) contains and fast updates
    _insertion_order: int # Counter for tie-breaking in stable queues

    # /// <summary>
    # /// Instantiate a new Priority Queue
    # /// </summary>
    # /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
    # public FastPriorityQueue(int maxNodes)
    def __init__(self, max_nodes: int):
        """
        Instantiate a new Priority Queue.
        Args:
            max_nodes: The max nodes ever allowed to be enqueued.
        """
        if max_nodes <= 0:
            raise ValueError("New queue size cannot be smaller than 1")

        self._num_nodes = 0
        self._nodes = [None] * (max_nodes + 1)  # 1-indexed heap
        self._node_to_index = {}
        self._insertion_order = 0

    # /// <summary>
    # /// Returns the number of nodes in the queue.
    # /// O(1)
    # /// </summary>
    # public int Count
    # {
    #     get
    #     {
    #         return _numNodes;
    #     }
    # }
    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    # /// <summary>
    # /// Returns the maximum number of items that can be enqueued at once in this queue.
    # /// O(1)
    # /// </summary>
    # public int MaxSize
    # {
    #     get
    #     {
    #         return _nodes.Length - 1;
    #     }
    # }
    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

    # /// <summary>
    # /// Removes every node from the queue.
    # /// O(n) (So, don't do this often!)
    # /// </summary>
    # public void Clear()
    def clear(self) -> None:
        """
        Removes every node from the queue. O(n)
        """
        for i in range(1, self._num_nodes + 1):
            if self._nodes[i] is not None:
                self._nodes[i].QueueIndex = 0
                self._nodes[i]._queue = None
                del self._node_to_index[self._nodes[i]]
            self._nodes[i] = None
        self._num_nodes = 0
        self._insertion_order = 0

    # /// <summary>
    # /// Returns (in O(1)!) whether the given node is in the queue.
    # /// </summary>
    # public bool Contains(T node)
    def contains(self, node: T) -> bool:
        """
        Returns whether the given node is in the queue. O(1)
        """
        # In the C# version, node.QueueIndex is checked directly.
        # In Python, we use _node_to_index for robust O(1) check.
        # Also, perform debug checks similar to C# for consistency.
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.contains was called on a node from another queue. Please call originalQueue.reset_node() first")
        
        # Check consistency with QueueIndex, though _node_to_index is more authoritative
        is_in_cache = node in self._node_to_index
        is_at_correct_index = is_in_cache and self._node_to_index[node] == node.QueueIndex and self._nodes[node.QueueIndex] == node

        # If it's in the cache, but its index is corrupted, that's an issue.
        if is_in_cache and not is_at_correct_index:
             raise RuntimeError("node.QueueIndex has been corrupted. Did you change it manually? Or add this node to another queue?")
        
        return is_at_correct_index

    # /// <summary>
    # /// Enqueue a node to the priority queue. Lower values are placed in front.
    # /// </summary>
    # public void Enqueue(T node, float priority)
    def enqueue(self, node: T, priority: float) -> None:
        """
        Enqueue a node to the priority queue. Lower values are placed in front. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if self._num_nodes >= self.max_size:
            raise RuntimeError("Queue is full - node cannot be added")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.enqueue was called on a node from another queue. Please call originalQueue.reset_node() first")
        if self.contains(node): # This checks if it's already properly enqueued in THIS queue
             raise RuntimeError(f"Node is already enqueued: {node}")

        node.Priority = priority
        self._num_nodes += 1
        node.QueueIndex = self._num_nodes
        self._nodes[self._num_nodes] = node
        self._node_to_index[node] = self._num_nodes # Store current index
        node._queue = self # For debug/validation in C# original

        self._cascade_up(node)

    # /// <summary>
    # /// Helper method to move a node up the heap.
    # /// </summary>
    # private void CascadeUp(T node)
    def _cascade_up(self, node: T) -> None:
        """
        Helper method to move a node up the heap (Heapify-up).
        """
        current_index = node.QueueIndex
        while current_index > 1:
            parent_index = current_index // 2
            parent_node = self._nodes[parent_index]

            if self._has_higher_or_equal_priority(parent_node, node):
                break # Parent has higher or equal priority, so we are done

            # Swap node with parent
            self._nodes[current_index] = parent_node
            if parent_node is not None:
                parent_node.QueueIndex = current_index
                self._node_to_index[parent_node] = current_index

            self._nodes[parent_index] = node
            node.QueueIndex = parent_index
            self._node_to_index[node] = parent_index

            current_index = parent_index

    # /// <summary>
    # /// Helper method to move a node down the heap.
    # /// </summary>
    # private void CascadeDown(T node)
    def _cascade_down(self, node: T) -> None:
        """
        Helper method to move a node down the heap (Heapify-down).
        """
        current_index = node.QueueIndex
        while True:
            child_left_index = 2 * current_index
            child_right_index = 2 * current_index + 1
            swap_index = 0

            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if self._has_higher_priority(child_left, node):
                    swap_index = child_left_index

            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if swap_index == 0: # No left child or left child has lower/equal priority
                    if self._has_higher_priority(child_right, node):
                        swap_index = child_right_index
                else: # Left child has higher priority than current_node
                    child_to_compare = self._nodes[swap_index]
                    if self._has_higher_priority(child_right, child_to_compare):
                        swap_index = child_right_index

            if swap_index == 0:
                break # No child has higher priority, we are done

            # Swap
            swap_node = self._nodes[swap_index]
            self._nodes[current_index] = swap_node
            if swap_node is not None:
                swap_node.QueueIndex = current_index
                self._node_to_index[swap_node] = current_index

            self._nodes[swap_index] = node
            node.QueueIndex = swap_index
            self._node_to_index[node] = swap_index

            current_index = swap_index

    # /// <summary>
    # /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
    # /// </summary>
    # private bool HasHigherPriority(T higher, T lower)
    def _has_higher_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        """
        if higher is None or lower is None:
            return False
        return higher.Priority < lower.Priority

    # /// <summary>
    # /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
    # /// Note that calling HasHigherOrEqualPriority(node, node) (ie. both arguments the same node) will return true
    # /// </summary>
    # private bool HasHigherOrEqualPriority(T higher, T lower)
    def _has_higher_or_equal_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher or equal priority than 'lower', false otherwise.
        """
        if higher is None or lower is None:
            return False
        return higher.Priority <= lower.Priority

    # /// <summary>
    # /// Removes the head of the queue and returns it.
    # /// O(log n)
    # /// </summary>
    # public T Dequeue()
    def dequeue(self) -> T:
        """
        Removes the head of the queue and returns it. O(log n)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call dequeue() on an empty queue")

        # if not self.is_valid_queue(): # For debugging, enable this, but it's O(N)
        #     raise RuntimeError("Queue has been corrupted")

        return_me = self._nodes[1]
        if return_me is None:
            raise RuntimeError("Heap root is unexpectedly None")

        if self._num_nodes == 1:
            self._nodes[1] = None
            del self._node_to_index[return_me]
            self._num_nodes = 0
            return_me.QueueIndex = 0
            return_me._queue = None
            return return_me

        # Swap the node with the last node
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node is unexpectedly None")

        self._nodes[1] = former_last_node
        former_last_node.QueueIndex = 1
        self._node_to_index[former_last_node] = 1

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[return_me] # Remove the dequeued node from tracking
        return_me.QueueIndex = 0 # Invalidate index for the removed node
        return_me._queue = None

        # Now bubble former_last_node (which is no longer the last node) down
        self._cascade_down(former_last_node)
        return return_me

    # /// <summary>
    # /// Resize the queue so it can accept more nodes.
    # /// O(n)
    # /// </summary>
    # public void Resize(int maxNodes)
    def resize(self, max_nodes: int) -> None:
        """
        Resize the queue so it can accept more nodes. O(n)
        """
        if max_nodes <= 0:
            raise ValueError("Queue size cannot be smaller than 1")
        if max_nodes < self._num_nodes:
            raise ValueError(f"Called Resize({max_nodes}), but current queue contains {self._num_nodes} nodes")

        new_nodes = [None] * (max_nodes + 1)
        for i in range(1, self._num_nodes + 1):
            new_nodes[i] = self._nodes[i]
        self._nodes = new_nodes

    # /// <summary>
    # /// Returns the head of the queue, without removing it.
    # /// O(1)
    # /// </summary>
    # public T First
    # {
    #     get
    #     {
    #         if(_numNodes <= 0)
    #         {
    #             throw new InvalidOperationException("Cannot call .First on an empty queue");
    #         }
    #         return _nodes[1];
    #     }
    # }
    @property
    def first(self) -> T:
        """
        Returns the head of the queue, without removing it. O(1)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call .first on an empty queue")
        if self._nodes[1] is None:
            raise RuntimeError("First element in heap is unexpectedly None")
        return self._nodes[1]

    # /// <summary>
    # /// This method must be called on a node every time its priority changes while it is in the queue.
    # /// O(log n)
    # /// </summary>
    # public void UpdatePriority(T node, float priority)
    def update_priority(self, node: T, priority: float) -> None:
        """
        This method must be called on a node every time its priority changes while it is in the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.update_priority was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call update_priority() on a node which is not enqueued: {node}")

        # The C# version directly modifies node.Priority and then calls OnNodeUpdated.
        # We'll do the same.
        old_priority = node.Priority
        node.Priority = priority

        self._on_node_updated(node, old_priority) # Pass old priority for comparison

    # /// <summary>
    # /// Helper method called when a node's priority is updated.
    # /// </summary>
    # private void OnNodeUpdated(T node)
    def _on_node_updated(self, node: T, old_priority: float) -> None:
        """
        Helper method called when a node's priority is updated.
        """
        # Bubble the updated node up or down as appropriate
        # We need to know if the priority increased or decreased to choose cascade direction
        if node.Priority < old_priority:
            self._cascade_up(node)
        else: # Priority is greater than or equal to old priority
            self._cascade_down(node)


    # /// <summary>
    # /// Removes a node from the queue.
    # /// O(log n)
    # /// </summary>
    # public void Remove(T node)
    def remove(self, node: T) -> None:
        """
        Removes a node from the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.remove was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call remove() on a node which is not enqueued: {node}")

        # If the node is already the last node, we can remove it immediately
        if node.QueueIndex == self._num_nodes:
            self._nodes[self._num_nodes] = None
            del self._node_to_index[node]
            self._num_nodes -= 1
            node.QueueIndex = 0
            node._queue = None
            return

        # Swap the node with the last node
        # In the C# version, `formerLastNode` is the node, not its priority.
        # We need to store its old priority before the swap for comparison in _on_node_updated
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node in heap is unexpectedly None during remove operation")
        
        old_priority_of_former_last_node = former_last_node.Priority # Store before potential modification

        self._nodes[node.QueueIndex] = former_last_node
        former_last_node.QueueIndex = node.QueueIndex
        self._node_to_index[former_last_node] = node.QueueIndex

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[node]
        node.QueueIndex = 0
        node._queue = None

        # Now bubble former_last_node (which is no longer the last node) up or down as appropriate
        # Since its priority wasn't actually changed, we simulate an "update" with its own old priority
        # to trigger the correct cascade behavior.
        self._on_node_updated(former_last_node, old_priority_of_former_last_node)


    # /// <summary>
    # /// By default, nodes that have been previously added to one queue cannot be added to another queue.
    # /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
    # /// </summary>
    # public void ResetNode(T node)
    def reset_node(self, node: T) -> None:
        """
        Resets a node's internal state to allow it to be reused in another queue.
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.reset_node was called on a node from another queue")
        if self.contains(node): # This checks if it's already properly enqueued in THIS queue
            raise RuntimeError("node.reset_node was called on a node that is still in the queue")

        node.QueueIndex = 0
        node._queue = None

    # public IEnumerator<T> GetEnumerator()
    def __iter__(self) -> Iterable[T]:
        """
        Returns an iterator over the nodes currently in the queue.
        """
        # Return a copy to avoid issues if the queue is modified during iteration.
        # In C#, it might iterate over the internal array, but that can lead to issues
        # if the collection is modified. A copy is safer in Python.
        # Iteration order is not guaranteed for a typical heap, it's just the elements.
        active_nodes = []
        for i in range(1, self._num_nodes + 1):
            node = self._nodes[i]
            if node is not None:
                active_nodes.append(node)
        return iter(active_nodes)

    # /// <summary>
    # /// Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
    # /// </summary>
    # public bool IsValidQueue()
    def is_valid_queue(self) -> bool:
        """
        Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
        """
        for i in range(1, self._num_nodes + 1):
            current_node = self._nodes[i]
            if current_node is None:
                # Should not happen in valid heap up to _num_nodes
                return False

            # Check parent link
            if current_node.QueueIndex != i:
                return False # Corrupted QueueIndex

            # Check if node is correctly linked back to this queue
            if current_node._queue != self:
                return False

            # Check child priorities
            child_left_index = 2 * i
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if child_left is None or self._has_higher_priority(child_left, current_node):
                    return False

            child_right_index = 2 * i + 1
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if child_right is None or self._has_higher_priority(child_right, current_node):
                    return False

            # Check _node_to_index consistency
            if current_node not in self._node_to_index or self._node_to_index[current_node] != i:
                return False

        # Check for any extra nodes in _node_to_index not in the active heap range
        for node, index in self._node_to_index.items():
            if not (1 <= index <= self._num_nodes and self._nodes[index] == node):
                return False

        return True

```

---

**MountainGoap/PriorityQueue/GenericPriorityQueue.py**

```python
# // <copyright file="GenericPriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

import heapq
from typing import TypeVar, List, Dict, Any, Optional, Iterable, Callable, Union, Tuple
from functools import cmp_to_key

from .GenericPriorityQueueNode import GenericPriorityQueueNode
from .IFixedSizePriorityQueue import IFixedSizePriorityQueue

TItem = TypeVar('TItem', bound=GenericPriorityQueueNode)
TPriority = TypeVar('TPriority')

# /// <summary>
# /// A copy of StablePriorityQueue which also has generic priority-type
# /// </summary>
# /// <typeparam name="TItem">The values in the queue. Must extend the GenericPriorityQueueNode class</typeparam>
# /// <typeparam name="TPriority">The priority-type. Must extend IComparable&lt;TPriority&gt;</typeparam>
class GenericPriorityQueue(IFixedSizePriorityQueue[TItem, TPriority]):
    """
    A priority queue implementation with generic priority-type and stability.
    This is a simplified Python implementation using heapq.
    """

    _num_nodes: int
    _nodes: List[Optional[TItem]]  # Using a list as the heap (1-indexed conceptually)
    _node_to_index: Dict[TItem, int]  # For O(1) contains and fast updates
    _num_nodes_ever_enqueued: int  # For tie-breaking (insertion order)
    _comparer: Callable[[TPriority, TPriority], int] # Custom comparison for TPriority

    # /// <summary>
    # /// Instantiate a new Priority Queue
    # /// </summary>
    # /// <param name="maxNodes">The max nodes ever allowed to be enqueued</param>
    # public GenericPriorityQueue(int maxNodes) : this(maxNodes, Comparer<TPriority>.Default) { }
    # public GenericPriorityQueue(int maxNodes, IComparer<TPriority> comparer) : this(maxNodes, comparer.Compare) { }
    # public GenericPriorityQueue(int maxNodes, Comparison<TPriority> comparer)
    def __init__(self, max_nodes: int, comparer: Optional[Callable[[TPriority, TPriority], int]] = None):
        """
        Instantiate a new Priority Queue.

        Args:
            max_nodes: The max nodes ever allowed to be enqueued.
            comparer: The comparison function to use to compare TPriority values.
                      Defaults to a standard comparison for comparable types.
                      Should return -1 if a<b, 0 if a==b, 1 if a>b.
        """
        if max_nodes <= 0:
            raise ValueError("New queue size cannot be smaller than 1")

        self._num_nodes = 0
        self._nodes = [None] * (max_nodes + 1)  # 1-indexed heap
        self._node_to_index = {}
        self._num_nodes_ever_enqueued = 0

        if comparer is None:
            # Default comparer for basic types
            def default_comparer(a: TPriority, b: TPriority) -> int:
                if a < b: # type: ignore
                    return -1
                elif a > b: # type: ignore
                    return 1
                else:
                    return 0
            self._comparer = default_comparer
        else:
            self._comparer = comparer

    # /// <summary>
    # /// Returns the number of nodes in the queue.
    # /// O(1)
    # /// </summary>
    # public int Count
    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    # /// <summary>
    # /// Returns the maximum number of items that can be enqueued at once in this queue.
    # /// O(1)
    # /// </summary>
    # public int MaxSize
    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

    # /// <summary>
    # /// Removes every node from the queue.
    # /// O(n) (So, don't do this often!)
    # /// </summary>
    # public void Clear()
    def clear(self) -> None:
        """
        Removes every node from the queue. O(n)
        """
        for i in range(1, self._num_nodes + 1):
            if self._nodes[i] is not None:
                self._nodes[i].QueueIndex = 0
                self._nodes[i]._queue = None
                self._nodes[i].InsertionIndex = 0 # Also reset insertion index
                del self._node_to_index[self._nodes[i]]
            self._nodes[i] = None
        self._num_nodes = 0
        self._num_nodes_ever_enqueued = 0

    # /// <summary>
    # /// Returns (in O(1)!) whether the given node is in the queue.
    # /// </summary>
    # public bool Contains(TItem node)
    def contains(self, node: TItem) -> bool:
        """
        Returns whether the given node is in the queue. O(1)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.contains was called on a node from another queue. Please call originalQueue.reset_node() first")

        is_in_cache = node in self._node_to_index
        is_at_correct_index = is_in_cache and self._node_to_index[node] == node.QueueIndex and self._nodes[node.QueueIndex] == node

        if is_in_cache and not is_at_correct_index:
             raise RuntimeError("node.QueueIndex has been corrupted. Did you change it manually? Or add this node to another queue?")

        return is_at_correct_index

    # /// <summary>
    # /// Enqueue a node to the priority queue. Lower values are placed in front. Ties are broken by first-in-first-out.
    # /// O(log n)
    # /// </summary>
    # public void Enqueue(TItem node, TPriority priority)
    def enqueue(self, node: TItem, priority: TPriority) -> None:
        """
        Enqueue a node to the priority queue. Lower values are placed in front. Ties are broken by first-in-first-out. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if self._num_nodes >= self.max_size:
            raise RuntimeError("Queue is full - node cannot be added")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.enqueue was called on a node from another queue. Please call originalQueue.reset_node() first")
        if self.contains(node):
            raise RuntimeError(f"Node is already enqueued: {node}")

        node.Priority = priority
        self._num_nodes += 1
        node.QueueIndex = self._num_nodes
        node.InsertionIndex = self._num_nodes_ever_enqueued
        self._num_nodes_ever_enqueued += 1

        self._nodes[self._num_nodes] = node
        self._node_to_index[node] = self._num_nodes
        node._queue = self

        self._cascade_up(node)

    # /// <summary>
    # /// Helper method to move a node up the heap.
    # /// </summary>
    # private void CascadeUp(TItem node)
    def _cascade_up(self, node: TItem) -> None:
        """
        Helper method to move a node up the heap (Heapify-up).
        """
        current_index = node.QueueIndex
        while current_index > 1:
            parent_index = current_index // 2
            parent_node = self._nodes[parent_index]

            if self._has_higher_priority(parent_node, node): # parent_node has higher priority than node
                break

            # Node has higher priority, so move parent down the heap to make room
            self._nodes[current_index] = parent_node
            if parent_node is not None:
                parent_node.QueueIndex = current_index
                self._node_to_index[parent_node] = current_index

            self._nodes[parent_index] = node
            node.QueueIndex = parent_index
            self._node_to_index[node] = parent_index

            current_index = parent_index

    # /// <summary>
    # /// Helper method to move a node down the heap.
    # /// </summary>
    # private void CascadeDown(TItem node)
    def _cascade_down(self, node: TItem) -> None:
        """
        Helper method to move a node down the heap (Heapify-down).
        """
        current_index = node.QueueIndex
        while True:
            child_left_index = 2 * current_index
            child_right_index = 2 * current_index + 1
            swap_index = 0

            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if self._has_higher_priority(child_left, node): # left child has higher priority than current node
                    swap_index = child_left_index

            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if swap_index == 0: # No left child or left child has lower/equal priority
                    if self._has_higher_priority(child_right, node):
                        swap_index = child_right_index
                else: # Left child has higher priority than current_node
                    child_to_compare = self._nodes[swap_index]
                    if self._has_higher_priority(child_right, child_to_compare):
                        swap_index = child_right_index

            if swap_index == 0:
                break # No child has higher priority, we are done

            # Swap
            swap_node = self._nodes[swap_index]
            if swap_node is None:
                # This should ideally not happen if heap invariant is maintained for active nodes
                break
            
            self._nodes[current_index] = swap_node
            swap_node.QueueIndex = current_index
            self._node_to_index[swap_node] = current_index

            self._nodes[swap_index] = node
            node.QueueIndex = swap_index
            self._node_to_index[node] = swap_index

            current_index = swap_index

    # /// <summary>
    # /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
    # /// Note that calling HasHigherPriority(node, node) (ie. both arguments the same node) will return false
    # /// </summary>
    # private bool HasHigherPriority(TItem higher, TItem lower)
    def _has_higher_priority(self, higher: Optional[TItem], lower: Optional[TItem]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        Includes tie-breaking by InsertionIndex.
        """
        if higher is None or lower is None:
            return False

        cmp = self._comparer(higher.Priority, lower.Priority)
        return (cmp < 0) or (cmp == 0 and higher.InsertionIndex < lower.InsertionIndex)


    # /// <summary>
    # /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
    # /// O(log n)
    # /// </summary>
    # public TItem Dequeue()
    def dequeue(self) -> TItem:
        """
        Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it. O(log n)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call dequeue() on an empty queue")

        # if not self.is_valid_queue(): # For debugging, enable this, but it's O(N)
        #     raise RuntimeError("Queue has been corrupted")

        return_me = self._nodes[1]
        if return_me is None:
            raise RuntimeError("Heap root is unexpectedly None")

        if self._num_nodes == 1:
            self._nodes[1] = None
            del self._node_to_index[return_me]
            self._num_nodes = 0
            return_me.QueueIndex = 0
            return_me._queue = None
            return_me.InsertionIndex = 0 # Reset insertion index
            return return_me

        # Swap the node with the last node
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node is unexpectedly None")

        self._nodes[1] = former_last_node
        former_last_node.QueueIndex = 1
        self._node_to_index[former_last_node] = 1

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[return_me]
        return_me.QueueIndex = 0
        return_me._queue = None
        return_me.InsertionIndex = 0 # Reset insertion index

        # Now bubble former_last_node (which is no longer the last node) down
        self._cascade_down(former_last_node)
        return return_me

    # /// <summary>
    # /// Resize the queue so it can accept more nodes.
    # /// O(n)
    # /// </summary>
    # public void Resize(int maxNodes)
    def resize(self, max_nodes: int) -> None:
        """
        Resize the queue so it can accept more nodes. O(n)
        """
        if max_nodes <= 0:
            raise ValueError("Queue size cannot be smaller than 1")
        if max_nodes < self._num_nodes:
            raise ValueError(f"Called Resize({max_nodes}), but current queue contains {self._num_nodes} nodes")

        new_nodes = [None] * (max_nodes + 1)
        for i in range(1, self._num_nodes + 1):
            new_nodes[i] = self._nodes[i]
        self._nodes = new_nodes

    # /// <summary>
    # /// Returns the head of the queue, without removing it.
    # /// O(1)
    # /// </summary>
    # public TItem First
    @property
    def first(self) -> TItem:
        """
        Returns the head of the queue, without removing it. O(1)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call .first on an empty queue")
        if self._nodes[1] is None:
            raise RuntimeError("First element in heap is unexpectedly None")
        return self._nodes[1]

    # /// <summary>
    # /// This method must be called on a node every time its priority changes while it is in the queue.
    # /// O(log n)
    # /// </summary>
    # public void UpdatePriority(TItem node, TPriority priority)
    def update_priority(self, node: TItem, priority: TPriority) -> None:
        """
        This method must be called on a node every time its priority changes while it is in the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.update_priority was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call update_priority() on a node which is not enqueued: {node}")

        old_priority = node.Priority # Store before modification
        node.Priority = priority
        self._on_node_updated(node, old_priority)

    # /// <summary>
    # /// Helper method called when a node's priority is updated.
    # /// </summary>
    # private void OnNodeUpdated(TItem node)
    def _on_node_updated(self, node: TItem, old_priority: TPriority) -> None:
        """
        Helper method called when a node's priority is updated.
        """
        # Bubble the updated node up or down as appropriate
        # Use the custom comparer for comparison
        cmp_result = self._comparer(node.Priority, old_priority)

        if cmp_result < 0: # New priority is higher (smaller value)
            self._cascade_up(node)
        elif cmp_result > 0: # New priority is lower (larger value)
            self._cascade_down(node)
        # If cmp_result is 0, priorities are equal, no change needed in heap structure due to priority,
        # but insertion order might still make a difference in stable queues.
        # However, for an "update" where only priority changes (not insertion index),
        # if old and new priorities are same, no heap adjustment is strictly needed for stability.


    # /// <summary>
    # /// Removes a node from the queue.
    # /// O(log n)
    # /// </summary>
    # public void Remove(TItem node)
    def remove(self, node: TItem) -> None:
        """
        Removes a node from the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.remove was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call remove() on a node which is not enqueued: {node}")

        if node.QueueIndex == self._num_nodes:
            self._nodes[self._num_nodes] = None
            del self._node_to_index[node]
            self._num_nodes -= 1
            node.QueueIndex = 0
            node._queue = None
            node.InsertionIndex = 0
            return

        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node in heap is unexpectedly None during remove operation")

        old_priority_of_former_last_node = former_last_node.Priority # Store before potential modification

        self._nodes[node.QueueIndex] = former_last_node
        former_last_node.QueueIndex = node.QueueIndex
        self._node_to_index[former_last_node] = node.QueueIndex

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[node]
        node.QueueIndex = 0
        node._queue = None
        node.InsertionIndex = 0

        self._on_node_updated(former_last_node, old_priority_of_former_last_node)


    # /// <summary>
    # /// Resets a node's internal state to allow it to be reused in another queue.
    # /// </summary>
    # public void ResetNode(TItem node)
    def reset_node(self, node: TItem) -> None:
        """
        Resets a node's internal state to allow it to be reused in another queue.
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.reset_node was called on a node from another queue")
        if self.contains(node):
            raise RuntimeError("node.reset_node was called on a node that is still in the queue")

        node.QueueIndex = 0
        node._queue = None
        node.InsertionIndex = 0

    # public IEnumerator<TItem> GetEnumerator()
    def __iter__(self) -> Iterable[TItem]:
        """
        Returns an iterator over the nodes currently in the queue.
        """
        active_nodes = []
        for i in range(1, self._num_nodes + 1):
            node = self._nodes[i]
            if node is not None:
                active_nodes.append(node)
        return iter(active_nodes)

    # /// <summary>
    # /// Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
    # /// </summary>
    # public bool IsValidQueue()
    def is_valid_queue(self) -> bool:
        """
        Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
        """
        for i in range(1, self._num_nodes + 1):
            current_node = self._nodes[i]
            if current_node is None:
                return False

            if current_node.QueueIndex != i:
                return False

            if current_node._queue != self:
                return False

            child_left_index = 2 * i
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if child_left is None or self._has_higher_priority(child_left, current_node):
                    return False

            child_right_index = 2 * i + 1
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if child_right is None or self._has_higher_priority(child_right, current_node):
                    return False

            if current_node not in self._node_to_index or self._node_to_index[current_node] != i:
                return False

        for node, index in self._node_to_index.items():
            if not (1 <= index <= self._num_nodes and self._nodes[index] == node):
                return False

        return True

```

---

**MountainGoap/PriorityQueue/StablePriorityQueue.py**

```python
# // <copyright file="StablePriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

import heapq
from typing import TypeVar, List, Dict, Any, Optional, Iterable, Callable

from .StablePriorityQueueNode import StablePriorityQueueNode
from .IFixedSizePriorityQueue import IFixedSizePriorityQueue

T = TypeVar('T', bound=StablePriorityQueueNode)

# /// <summary>
# /// A copy of FastPriorityQueue which is also stable - that is, when two nodes are enqueued with the same priority, they
# /// are always dequeued in the same order.
# /// </summary>
# /// <typeparam name="T">The values in the queue. Must extend the StablePriorityQueueNode class</typeparam>
class StablePriorityQueue(IFixedSizePriorityQueue[T, float]):
    """
    A stable priority queue implementation.
    This is a simplified Python implementation using heapq.
    """

    _num_nodes: int
    _nodes: List[Optional[T]] # Using a list as the heap (1-indexed conceptually)
    _node_to_index: Dict[T, int] # For O(1) contains and fast updates
    _num_nodes_ever_enqueued: int # For tie-breaking (insertion order)

    # /// <summary>
    # /// Instantiate a new Priority Queue
    # /// </summary>
    # /// <param name="maxNodes">The max nodes ever allowed to be enqueued</param>
    # public StablePriorityQueue(int maxNodes)
    def __init__(self, max_nodes: int):
        """
        Instantiate a new Priority Queue.

        Args:
            max_nodes: The max nodes ever allowed to be enqueued.
        """
        if max_nodes <= 0:
            raise ValueError("New queue size cannot be smaller than 1")

        self._num_nodes = 0
        self._nodes = [None] * (max_nodes + 1)  # 1-indexed heap
        self._node_to_index = {}
        self._num_nodes_ever_enqueued = 0

    # /// <summary>
    # /// Returns the number of nodes in the queue.
    # /// O(1)
    # /// </summary>
    # public int Count
    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    # /// <summary>
    # /// Returns the maximum number of items that can be enqueued at once in this queue.
    # /// O(1)
    # /// </summary>
    # public int MaxSize
    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

    # /// <summary>
    # /// Removes every node from the queue.
    # /// O(n) (So, don't do this often!)
    # /// </summary>
    # public void Clear()
    def clear(self) -> None:
        """
        Removes every node from the queue. O(n)
        """
        for i in range(1, self._num_nodes + 1):
            if self._nodes[i] is not None:
                self._nodes[i].QueueIndex = 0
                self._nodes[i]._queue = None
                self._nodes[i].InsertionIndex = 0 # Also reset insertion index
                del self._node_to_index[self._nodes[i]]
            self._nodes[i] = None
        self._num_nodes = 0
        self._num_nodes_ever_enqueued = 0

    # /// <summary>
    # /// Returns (in O(1)!) whether the given node is in the queue.
    # /// </summary>
    # public bool Contains(T node)
    def contains(self, node: T) -> bool:
        """
        Returns whether the given node is in the queue. O(1)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.contains was called on a node from another queue. Please call originalQueue.reset_node() first")

        is_in_cache = node in self._node_to_index
        is_at_correct_index = is_in_cache and self._node_to_index[node] == node.QueueIndex and self._nodes[node.QueueIndex] == node

        if is_in_cache and not is_at_correct_index:
             raise RuntimeError("node.QueueIndex has been corrupted. Did you change it manually? Or add this node to another queue?")

        return is_at_correct_index

    # /// <summary>
    # /// Enqueue a node to the priority queue. Lower values are placed in front. Ties are broken by first-in-first-out.
    # /// O(log n)
    # /// </summary>
    # public void Enqueue(T node, float priority)
    def enqueue(self, node: T, priority: float) -> None:
        """
        Enqueue a node to the priority queue. Lower values are placed in front. Ties are broken by first-in-first-out. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if self._num_nodes >= self.max_size:
            raise RuntimeError("Queue is full - node cannot be added")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.enqueue was called on a node from another queue. Please call originalQueue.reset_node() first")
        if self.contains(node):
            raise RuntimeError(f"Node is already enqueued: {node}")

        node.Priority = priority
        self._num_nodes += 1
        node.QueueIndex = self._num_nodes
        node.InsertionIndex = self._num_nodes_ever_enqueued
        self._num_nodes_ever_enqueued += 1

        self._nodes[self._num_nodes] = node
        self._node_to_index[node] = self._num_nodes
        node._queue = self

        self._cascade_up(node)

    # /// <summary>
    # /// Helper method to move a node up the heap.
    # /// </summary>
    # private void CascadeUp(T node)
    def _cascade_up(self, node: T) -> None:
        """
        Helper method to move a node up the heap (Heapify-up).
        """
        current_index = node.QueueIndex
        while current_index > 1:
            parent_index = current_index // 2
            parent_node = self._nodes[parent_index]

            if self._has_higher_priority(parent_node, node): # parent_node has higher priority than node
                break

            # Node has higher priority, so move parent down the heap to make room
            self._nodes[current_index] = parent_node
            if parent_node is not None:
                parent_node.QueueIndex = current_index
                self._node_to_index[parent_node] = current_index

            self._nodes[parent_index] = node
            node.QueueIndex = parent_index
            self._node_to_index[node] = parent_index

            current_index = parent_index

    # /// <summary>
    # /// Helper method to move a node down the heap.
    # /// </summary>
    # private void CascadeDown(T node)
    def _cascade_down(self, node: T) -> None:
        """
        Helper method to move a node down the heap (Heapify-down).
        """
        current_index = node.QueueIndex
        while True:
            child_left_index = 2 * current_index
            child_right_index = 2 * current_index + 1
            swap_index = 0

            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if self._has_higher_priority(child_left, node): # left child has higher priority than current node
                    swap_index = child_left_index

            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if swap_index == 0: # No left child or left child has lower/equal priority
                    if self._has_higher_priority(child_right, node):
                        swap_index = child_right_index
                else: # Left child has higher priority than current_node
                    child_to_compare = self._nodes[swap_index]
                    if self._has_higher_priority(child_right, child_to_compare):
                        swap_index = child_right_index

            if swap_index == 0:
                break # No child has higher priority, we are done

            # Swap
            swap_node = self._nodes[swap_index]
            if swap_node is None:
                # This should ideally not happen if heap invariant is maintained for active nodes
                break

            self._nodes[current_index] = swap_node
            swap_node.QueueIndex = current_index
            self._node_to_index[swap_node] = current_index

            self._nodes[swap_index] = node
            node.QueueIndex = swap_index
            self._node_to_index[node] = swap_index

            current_index = swap_index

    # /// <summary>
    # /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
    # /// Includes tie-breaking by InsertionIndex.
    # /// </summary>
    # private bool HasHigherPriority(T higher, T lower)
    def _has_higher_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        Includes tie-breaking by InsertionIndex.
        """
        if higher is None or lower is None:
            return False
        return (higher.Priority < lower.Priority) or \
               (higher.Priority == lower.Priority and higher.InsertionIndex < lower.InsertionIndex)

    # /// <summary>
    # /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
    # /// O(log n)
    # /// </summary>
    # public T Dequeue()
    def dequeue(self) -> T:
        """
        Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it. O(log n)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call dequeue() on an empty queue")

        # if not self.is_valid_queue(): # For debugging, enable this, but it's O(N)
        #     raise RuntimeError("Queue has been corrupted")

        return_me = self._nodes[1]
        if return_me is None:
            raise RuntimeError("Heap root is unexpectedly None")

        if self._num_nodes == 1:
            self._nodes[1] = None
            del self._node_to_index[return_me]
            self._num_nodes = 0
            return_me.QueueIndex = 0
            return_me._queue = None
            return_me.InsertionIndex = 0 # Reset insertion index
            return return_me

        # Swap the node with the last node
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node is unexpectedly None")

        old_priority_of_former_last_node = former_last_node.Priority # Store before potential modification

        self._nodes[1] = former_last_node
        former_last_node.QueueIndex = 1
        self._node_to_index[former_last_node] = 1

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[return_me]
        return_me.QueueIndex = 0
        return_me._queue = None
        return_me.InsertionIndex = 0

        # Now bubble former_last_node (which is no longer the last node) down
        self._on_node_updated(former_last_node, old_priority_of_former_last_node)
        return return_me

    # /// <summary>
    # /// Resize the queue so it can accept more nodes.
    # /// O(n)
    # /// </summary>
    # public void Resize(int maxNodes)
    def resize(self, max_nodes: int) -> None:
        """
        Resize the queue so it can accept more nodes. O(n)
        """
        if max_nodes <= 0:
            raise ValueError("Queue size cannot be smaller than 1")
        if max_nodes < self._num_nodes:
            raise ValueError(f"Called Resize({max_nodes}), but current queue contains {self._num_nodes} nodes")

        new_nodes = [None] * (max_nodes + 1)
        for i in range(1, self._num_nodes + 1):
            new_nodes[i] = self._nodes[i]
        self._nodes = new_nodes

    # /// <summary>
    # /// Returns the head of the queue, without removing it.
    # /// O(1)
    # /// </summary>
    # public T First
    @property
    def first(self) -> T:
        """
        Returns the head of the queue, without removing it. O(1)
        """
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call .first on an empty queue")
        if self._nodes[1] is None:
            raise RuntimeError("First element in heap is unexpectedly None")
        return self._nodes[1]

    # /// <summary>
    # /// This method must be called on a node every time its priority changes while it is in the queue.
    # /// O(log n)
    # /// </summary>
    # public void UpdatePriority(T node, float priority)
    def update_priority(self, node: T, priority: float) -> None:
        """
        This method must be called on a node every time its priority changes while it is in the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.update_priority was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call update_priority() on a node which is not enqueued: {node}")

        old_priority = node.Priority
        node.Priority = priority
        self._on_node_updated(node, old_priority)

    # /// <summary>
    # /// Helper method called when a node's priority is updated.
    # /// </summary>
    # private void OnNodeUpdated(T node)
    def _on_node_updated(self, node: T, old_priority: float) -> None:
        """
        Helper method called when a node's priority is updated.
        """
        # Bubble the updated node up or down as appropriate
        if node.Priority < old_priority:
            self._cascade_up(node)
        elif node.Priority > old_priority:
            self._cascade_down(node)
        # If priorities are equal, no action needed for stability here as InsertionIndex doesn't change on update

    # /// <summary>
    # /// Removes a node from the queue.
    # /// O(log n)
    # /// </summary>
    # public void Remove(T node)
    def remove(self, node: T) -> None:
        """
        Removes a node from the queue. O(log n)
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.remove was called on a node from another queue")
        if not self.contains(node):
            raise RuntimeError(f"Cannot call remove() on a node which is not enqueued: {node}")

        if node.QueueIndex == self._num_nodes:
            self._nodes[self._num_nodes] = None
            del self._node_to_index[node]
            self._num_nodes -= 1
            node.QueueIndex = 0
            node._queue = None
            node.InsertionIndex = 0
            return

        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node in heap is unexpectedly None during remove operation")

        old_priority_of_former_last_node = former_last_node.Priority # Store before potential modification

        self._nodes[node.QueueIndex] = former_last_node
        former_last_node.QueueIndex = node.QueueIndex
        self._node_to_index[former_last_node] = node.QueueIndex

        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1

        del self._node_to_index[node]
        node.QueueIndex = 0
        node._queue = None
        node.InsertionIndex = 0

        self._on_node_updated(former_last_node, old_priority_of_former_last_node)

    # /// <summary>
    # /// Resets a node's internal state to allow it to be reused in another queue.
    # /// </summary>
    # public void ResetNode(T node)
    def reset_node(self, node: T) -> None:
        """
        Resets a node's internal state to allow it to be reused in another queue.
        """
        if node is None:
            raise ValueError("node cannot be None")
        if hasattr(node, '_queue') and node._queue is not None and node._queue != self:
            raise RuntimeError("node.reset_node was called on a node from another queue")
        if self.contains(node):
            raise RuntimeError("node.reset_node was called on a node that is still in the queue")

        node.QueueIndex = 0
        node._queue = None
        node.InsertionIndex = 0

    # public IEnumerator<T> GetEnumerator()
    def __iter__(self) -> Iterable[T]:
        """
        Returns an iterator over the nodes currently in the queue.
        """
        active_nodes = []
        for i in range(1, self._num_nodes + 1):
            node = self._nodes[i]
            if node is not None:
                active_nodes.append(node)
        return iter(active_nodes)

    # /// <summary>
    # /// Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
    # /// </summary>
    # public bool IsValidQueue()
    def is_valid_queue(self) -> bool:
        """
        Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
        """
        for i in range(1, self._num_nodes + 1):
            current_node = self._nodes[i]
            if current_node is None:
                return False

            if current_node.QueueIndex != i:
                return False

            if current_node._queue != self:
                return False

            child_left_index = 2 * i
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if child_left is None or self._has_higher_priority(child_left, current_node):
                    return False

            child_right_index = 2 * i + 1
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if child_right is None or self._has_higher_priority(child_right, current_node):
                    return False

            if current_node not in self._node_to_index or self._node_to_index[current_node] != i:
                return False

        for node, index in self._node_to_index.items():
            if not (1 <= index <= self._num_nodes and self._nodes[index] == node):
                return False

        return True

```

---

**MountainGoap/PriorityQueue/SimplePriorityQueue.py**

```python
# // <copyright file="SimplePriorityQueue.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable

from typing import TypeVar, List, Dict, Any, Optional, Iterable, Callable, Union
import threading # For thread-safety, equivalent to C# lock
from functools import cmp_to_key

from .GenericPriorityQueue import GenericPriorityQueue
from .GenericPriorityQueueNode import GenericPriorityQueueNode
from .IPriorityQueue import IPriorityQueue

TItem = TypeVar('TItem')
TPriority = TypeVar('TPriority')

# /// <summary>
# /// A simplified priority queue implementation.  Is stable, auto-resizes, and thread-safe, at the cost of being slightly slower than
# /// FastPriorityQueue
# /// Methods tagged as O(1) or O(log n) are assuming there are no duplicates.  Duplicates may increase the algorithmic complexity.
# /// </summary>
# /// <typeparam name="TItem">The type to enqueue</typeparam>
# /// <typeparam name="TPriority">The priority-type to use for nodes.  Must extend IComparable&lt;TPriority&gt;</typeparam>
class SimplePriorityQueue(IPriorityQueue[TItem, TPriority]):
    """
    A simplified priority queue implementation. Is stable, auto-resizes, and thread-safe.
    """

    # Private inner class SimpleNode
    # private class SimpleNode : GenericPriorityQueueNode<TPriority>
    # {
    #     public TItem Data { get; private set; }
    #     public SimpleNode(TItem data) { Data = data; }
    # }
    class _SimpleNode(GenericPriorityQueueNode[TPriority]):
        """Internal node to wrap the TItem and carry priority/indexing info."""
        def __init__(self, data: TItem):
            super().__init__()
            self.Data: TItem = data

        def __hash__(self) -> int:
            return id(self) # Identity hash for dictionary keys

        def __eq__(self, other: object) -> bool:
            return self is other # Identity equality for dictionary keys

    _INITIAL_QUEUE_SIZE = 10
    _queue: GenericPriorityQueue[_SimpleNode, TPriority]
    _item_to_nodes_cache: Dict[TItem, List[_SimpleNode]] # Maps user item to a list of its wrapper nodes (for duplicates)
    _null_nodes_cache: List[_SimpleNode] # Special list for null items (Python: None)
    _lock: threading.Lock # For thread-safety

    # /// <summary>
    # /// Instantiate a new Priority Queue
    # /// </summary>
    # public SimplePriorityQueue() : this(Comparer<TPriority>.Default, EqualityComparer<TItem>.Default) { }
    # ... multiple constructors ...
    def __init__(self, priority_comparer: Optional[Union[Callable[[TPriority, TPriority], int], Any]] = None,
                 item_equality_comparer: Optional[Any] = None):
        """
        Instantiate a new Priority Queue.

        Args:
            priority_comparer: A callable to compare two TPriority values.
                               Should return -1 if a<b, 0 if a==b, 1 if a>b.
                               If None, defaults to Python's natural comparison.
            item_equality_comparer: (Not directly used for Dict keying in Python unless custom class overrides __hash__ and __eq__)
                                    For Python, `_item_to_nodes_cache` uses the default `dict` behavior,
                                    which relies on `__hash__` and `__eq__` methods of TItem.
                                    If TItem objects are mutable or don't implement these,
                                    consider wrapping them or using `id()` as a key if identity is what's needed.
                                    For verbatim translation, we'll assume `TItem` is hashable.
        """
        # The priority_comparer needs to be passed to GenericPriorityQueue
        # Python's default comparison for its built-in types works well.
        # For custom types, `__lt__`, `__le__`, `__gt__`, `__ge__` define natural ordering.
        if priority_comparer is None:
            # Default comparison function for GenericPriorityQueue if not provided
            def default_priority_comparer(a: TPriority, b: TPriority) -> int:
                if a < b: # type: ignore
                    return -1
                elif a > b: # type: ignore
                    return 1
                else:
                    return 0
            self._queue = GenericPriorityQueue(self._INITIAL_QUEUE_SIZE, default_priority_comparer)
        else:
            self._queue = GenericPriorityQueue(self._INITIAL_QUEUE_SIZE, priority_comparer)


        # item_equality_comparer in C# affects the Dictionary.
        # In Python, for a dict, the keys need to be hashable and comparable for equality.
        # If TItem is an object, its default __hash__ (id) and __eq__ (identity) are used.
        # If value equality is needed, TItem must implement __hash__ and __eq__.
        self._item_to_nodes_cache = {} # Dict[TItem, List[_SimpleNode]]
        self._null_nodes_cache = [] # List[_SimpleNode]
        self._lock = threading.Lock() # For thread-safety

    # /// <summary>
    # /// Given an item of type T, returns the existing SimpleNode in the queue
    # /// </summary>
    # private SimpleNode GetExistingNode(TItem item)
    def _get_existing_node(self, item: TItem) -> Optional[_SimpleNode]:
        """
        Given an item of type T, returns the existing SimpleNode in the queue.
        Assumes lock is already held.
        """
        if item is None:
            return self._null_nodes_cache[0] if self._null_nodes_cache else None

        nodes = self._item_to_nodes_cache.get(item)
        return nodes[0] if nodes else None

    # /// <summary>
    # /// Adds an item to the Node-cache to allow for many methods to be O(1) or O(log n)
    # /// </summary>
    # private void AddToNodeCache(SimpleNode node)
    # This C# method is implicitly handled by `_item_to_nodes_cache` in Python `enqueue`

    # /// <summary>
    # /// Removes an item to the Node-cache to allow for many methods to be O(1) or O(log n) (assuming no duplicates)
    # /// </summary>
    # private void RemoveFromNodeCache(SimpleNode node)
    def _remove_from_node_cache(self, node: _SimpleNode) -> None:
        """
        Removes an item from the Node-cache.
        Assumes lock is already held.
        """
        if node.Data is None:
            if node in self._null_nodes_cache:
                self._null_nodes_cache.remove(node)
            return

        nodes = self._item_to_nodes_cache.get(node.Data)
        if nodes:
            if node in nodes: # Ensure we remove the specific SimpleNode instance
                nodes.remove(node)
            if not nodes: # If list is empty after removal, clean up dict entry
                del self._item_to_nodes_cache[node.Data]

    # /// <summary>
    # /// Returns the number of nodes in the queue.
    # /// O(1)
    # /// </summary>
    # public int Count
    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        with self._lock:
            return self._queue.count

    # /// <summary>
    # /// Returns the head of the queue, without removing it (use Dequeue() for that).
    # /// Throws an exception when the queue is empty.
    # /// O(1)
    # /// </summary>
    # public TItem First
    @property
    def first(self) -> TItem:
        """
        Returns the head of the queue, without removing it. O(1)
        """
        with self._lock:
            if self._queue.count <= 0:
                raise RuntimeError("Cannot call .first on an empty queue")
            return self._queue.first.Data

    # /// <summary>
    # /// Removes every node from the queue.
    # /// O(n)
    # /// </summary>
    # public void Clear()
    def clear(self) -> None:
        """
        Removes every node from the queue. O(n)
        """
        with self._lock:
            self._queue.clear()
            self._item_to_nodes_cache.clear()
            self._null_nodes_cache.clear()

    # /// <summary>
    # /// Returns whether the given item is in the queue.
    # /// O(1)
    # /// </summary>
    # public bool Contains(TItem item)
    def contains(self, item: TItem) -> bool:
        """
        Returns whether the given item is in the queue. O(1)
        """
        with self._lock:
            if item is None:
                return len(self._null_nodes_cache) > 0
            return item in self._item_to_nodes_cache

    # /// <summary>
    # /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
    # /// If queue is empty, throws an exception
    # /// O(log n)
    # /// </summary>
    # public TItem Dequeue()
    def dequeue(self) -> TItem:
        """
        Removes the head of the queue and returns it. O(log n)
        """
        with self._lock:
            if self._queue.count <= 0:
                raise RuntimeError("Cannot call dequeue() on an empty queue")

            node = self._queue.dequeue()
            self._remove_from_node_cache(node)
            return node.Data

    # /// <summary>
    # /// Enqueue the item with the given priority, without calling lock(_queue) or AddToNodeCache(node)
    # /// This is an internal helper for C# that is absorbed into public enqueue in Python
    # /// </summary>
    # private SimpleNode EnqueueNoLockOrCache(TItem item, TPriority priority)
    def _enqueue_no_lock_or_cache(self, item: TItem, priority: TPriority) -> _SimpleNode:
        """
        Internal helper: Enqueue the item without external locking/caching logic.
        """
        node = self._SimpleNode(item)
        if self._queue.count == self._queue.max_size:
            self._queue.resize(self._queue.max_size * 2 + 1) # Auto-resize
        self._queue.enqueue(node, priority)
        return node

    # /// <summary>
    # /// Enqueue a node to the priority queue. Lower values are placed in front. Ties are broken by first-in-first-out.
    # /// This queue automatically resizes itself, so there's no concern of the queue becoming 'full'.
    # /// Duplicates and null-values are allowed.
    # /// O(log n)
    # /// </summary>
    # public void Enqueue(TItem item, TPriority priority)
    def enqueue(self, item: TItem, priority: TPriority) -> None:
        """
        Enqueue a node to the priority queue. O(log n)
        """
        with self._lock:
            if item is None:
                nodes = self._null_nodes_cache
            else:
                nodes = self._item_to_nodes_cache.setdefault(item, [])
            node = self._enqueue_no_lock_or_cache(item, priority)
            nodes.append(node)

    # /// <summary>
    # /// Enqueue a node to the priority queue if it doesn't already exist.
    # /// Returns true if the node was successfully enqueued; false if it already exists.
    # /// O(log n)
    # /// </summary>
    # public bool EnqueueWithoutDuplicates(TItem item, TPriority priority)
    def enqueue_without_duplicates(self, item: TItem, priority: TPriority) -> bool:
        """
        Enqueue a node to the priority queue if it doesn't already exist. O(log n)

        Returns:
            True if the node was successfully enqueued; false if it already exists.
        """
        with self._lock:
            if item is None:
                if self._null_nodes_cache:
                    return False
                nodes = self._null_nodes_cache
            else:
                if item in self._item_to_nodes_cache:
                    return False
                nodes = self._item_to_nodes_cache.setdefault(item, [])

            node = self._enqueue_no_lock_or_cache(item, priority)
            nodes.append(node)
            return True

    # /// <summary>
    # /// Removes an item from the queue.
    # /// If the item is not in the queue, an exception is thrown.
    # /// If multiple copies of the item are enqueued, only the first one is removed.
    # /// O(log n)
    # /// </summary>
    # public void Remove(TItem item)
    def remove(self, item: TItem) -> None:
        """
        Removes an item from the queue. O(log n)
        """
        with self._lock:
            remove_me: Optional[SimplePriorityQueue._SimpleNode] = None
            nodes_list: Optional[List[SimplePriorityQueue._SimpleNode]] = None

            if item is None:
                if not self._null_nodes_cache:
                    raise RuntimeError(f"Cannot call remove() on a node which is not enqueued: {item}")
                remove_me = self._null_nodes_cache[0]
                nodes_list = self._null_nodes_cache
            else:
                nodes_list = self._item_to_nodes_cache.get(item)
                if not nodes_list:
                    raise RuntimeError(f"Cannot call remove() on a node which is not enqueued: {item}")
                remove_me = nodes_list[0]

            if remove_me is None: # Should not happen if nodes_list exists and has elements
                 raise RuntimeError("Node to remove is unexpectedly None")

            self._queue.remove(remove_me)
            # After removing from _queue, remove from _item_to_nodes_cache
            self._remove_from_node_cache(remove_me)


    # /// <summary>
    # /// Call this method to change the priority of an item.
    # /// Calling this method on a item not in the queue will throw an exception.
    # /// If the item is enqueued multiple times, only the first one will be updated.
    # /// O(log n)
    # /// </summary>
    # public void UpdatePriority(TItem item, TPriority priority)
    def update_priority(self, item: TItem, priority: TPriority) -> None:
        """
        Call this method to change the priority of an item. O(log n)
        """
        with self._lock:
            update_me = self._get_existing_node(item)
            if update_me is None:
                raise RuntimeError(f"Cannot call update_priority() on a node which is not enqueued: {item}")
            self._queue.update_priority(update_me, priority)

    # /// <summary>
    # /// Returns the priority of the given item.
    # /// Calling this method on a item not in the queue will throw an exception.
    # /// If the item is enqueued multiple times, only the priority of the first will be returned.
    # /// O(1)
    # /// </summary>
    # public TPriority GetPriority(TItem item)
    def get_priority(self, item: TItem) -> TPriority:
        """
        Returns the priority of the given item. O(1)
        """
        with self._lock:
            find_me = self._get_existing_node(item)
            if find_me is None:
                raise RuntimeError(f"Cannot call get_priority() on a node which is not enqueued: {item}")
            return find_me.Priority

    # #region Try* methods for multithreading
    # /// Get the head of the queue, without removing it (use TryDequeue() for that).
    # /// Returns true if successful, false otherwise
    # /// O(1)
    # public bool TryFirst(out TItem first)
    def try_first(self) -> tuple[bool, Optional[TItem]]:
        """
        Attempts to get the head of the queue without removing it. O(1)

        Returns:
            A tuple (success: bool, item: Optional[TItem]).
        """
        if self._queue.count > 0:
            with self._lock:
                if self._queue.count > 0:
                    return True, self._queue.first.Data
        return False, None

    # /// <summary>
    # /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and sets it to first.
    # /// Returns true if successful; false if queue was empty
    # /// O(log n)
    # /// </summary>
    # public bool TryDequeue(out TItem first)
    def try_dequeue(self) -> tuple[bool, Optional[TItem]]:
        """
        Attempts to remove the head of the queue and return it. O(log n)

        Returns:
            A tuple (success: bool, item: Optional[TItem]).
        """
        if self._queue.count > 0:
            with self._lock:
                if self._queue.count > 0:
                    node = self._queue.dequeue()
                    first = node.Data
                    self._remove_from_node_cache(node)
                    return True, first
        return False, None

    # /// <summary>
    # /// Attempts to remove an item from the queue.
    # /// Returns true if the item was successfully removed, false if it wasn't in the queue.
    # /// O(log n)
    # /// </summary>
    # public bool TryRemove(TItem item)
    def try_remove(self, item: TItem) -> bool:
        """
        Attempts to remove an item from the queue. O(log n)

        Returns:
            True if the item was successfully removed, false if it wasn't in the queue.
        """
        with self._lock:
            remove_me: Optional[SimplePriorityQueue._SimpleNode] = None
            nodes_list: Optional[List[SimplePriorityQueue._SimpleNode]] = None

            if item is None:
                if not self._null_nodes_cache:
                    return False
                remove_me = self._null_nodes_cache[0]
                nodes_list = self._null_nodes_cache
            else:
                nodes_list = self._item_to_nodes_cache.get(item)
                if not nodes_list:
                    return False
                remove_me = nodes_list[0]

            if remove_me is None: # Should not happen if nodes_list exists and has elements
                 return False

            self._queue.remove(remove_me)
            self._remove_from_node_cache(remove_me)
            return True


    # /// <summary>
    # /// Call this method to change the priority of an item.
    # /// Returns true if the item priority was updated, false otherwise.
    # /// O(log n)
    # /// </summary>
    # public bool TryUpdatePriority(TItem item, TPriority priority)
    def try_update_priority(self, item: TItem, priority: TPriority) -> bool:
        """
        Attempts to change the priority of an item. O(log n)

        Returns:
            True if the item priority was updated, false otherwise.
        """
        with self._lock:
            update_me = self._get_existing_node(item)
            if update_me is None:
                return False
            self._queue.update_priority(update_me, priority)
            return True

    # /// <summary>
    # /// Attempt to get the priority of the given item.
    # /// Returns true if the item was found in the queue, false otherwise
    # /// O(1)
    # /// </summary>
    # public bool TryGetPriority(TItem item, out TPriority priority)
    def try_get_priority(self, item: TItem) -> tuple[bool, Optional[TPriority]]:
        """
        Attempts to get the priority of the given item. O(1)

        Returns:
            A tuple (success: bool, priority: Optional[TPriority]).
        """
        with self._lock:
            find_me = self._get_existing_node(item)
            if find_me is None:
                return False, None
            return True, find_me.Priority
    # #endregion

    # public IEnumerator<TItem> GetEnumerator()
    def __iter__(self) -> Iterable[TItem]:
        """
        Returns an iterator over the items currently in the queue.
        """
        queue_data: List[TItem] = []
        with self._lock:
            for node in self._queue:
                queue_data.append(node.Data)
        return iter(queue_data)

    # public bool IsValidQueue()
    def is_valid_queue(self) -> bool:
        """
        Checks to make sure the queue is still in a valid state. Used for testing/debugging the queue.
        """
        with self._lock:
            # Check all items in cache are in the queue
            for nodes_list in self._item_to_nodes_cache.values():
                for node in nodes_list:
                    if not self._queue.contains(node):
                        return False
            for node in self._null_nodes_cache:
                 if not self._queue.contains(node):
                    return False

            # Check all items in queue are in cache (by checking if _get_existing_node works for them)
            # This check is a bit redundant if _item_to_nodes_cache is the source of truth,
            # but it validates cross-referencing.
            for node_in_queue in self._queue:
                if self._get_existing_node(node_in_queue.Data) is None:
                    # More rigorously, we should ensure the *specific* node_in_queue
                    # is present in the list associated with node_in_queue.Data
                    # This check is less direct than C# but works conceptually.
                    # For a truly verbatim match, we'd iterate through _item_to_nodes_cache
                    # and ensure all SimpleNodes point back to entries in _queue.
                    if node_in_queue.Data is None:
                        if node_in_queue not in self._null_nodes_cache:
                            return False
                    else:
                        nodes_for_item = self._item_to_nodes_cache.get(node_in_queue.Data)
                        if nodes_for_item is None or node_in_queue not in nodes_for_item:
                            return False

            # Check queue structure itself
            return self._queue.is_valid_queue()


# /// <summary>
# /// A simplified priority queue implementation with float priority.
# /// This class is kept here for backwards compatibility. It's recommended you use SimplePriorityQueue&lt;TItem, TPriority&gt;
# /// </summary>
# /// <typeparam name="TItem">The type to enqueue</typeparam>
# public class SimplePriorityQueue<TItem> : SimplePriorityQueue<TItem, float>
# {
#     /// <summary>
#     /// Instantiate a new Priority Queue
#     /// </summary>
#     public SimplePriorityQueue() { }
#
#     /// <summary>
#     /// Instantiate a new Priority Queue
#     /// </summary>
#     /// <param name="comparer">The comparer used to compare priority values. Defaults to Comparer&lt;float&gt;.default</param>
#     public SimplePriorityQueue(IComparer<float> comparer) : base(comparer) { }
#
#     /// <summary>
#     /// Instantiate a new Priority Queue
#     /// </summary>
#     /// <param name="comparer">The comparison function to use to compare priority values</param>
#     public SimplePriorityQueue(Comparison<float> comparer) : base(comparer) { }
# }
# This specialized class is not strictly necessary in Python due to default arguments and `float` being a basic type.
# Users can just instantiate `SimplePriorityQueue[TItem, float]` directly.
# However, for verbatim, we can provide a wrapper.

TItemFloat = TypeVar('TItemFloat')

class SimplePriorityQueueFloat(SimplePriorityQueue[TItemFloat, float]):
    """
    A simplified priority queue implementation with float priority for backward compatibility.
    """
    def __init__(self, priority_comparer: Optional[Union[Callable[[float, float], int], Any]] = None,
                 item_equality_comparer: Optional[Any] = None):
        super().__init__(priority_comparer, item_equality_comparer)

```

---

**MountainGoap/Internals/Utils.py**

```python
# // <copyright file="Utils.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Any, Optional, TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from ..BaseGoal import BaseGoal
    from ..Goal import Goal
    from ..ExtremeGoal import ExtremeGoal
    from ..ComparativeGoal import ComparativeGoal
    from ..ComparisonOperator import ComparisonOperator
    from .ActionNode import ActionNode

# /// <summary>
# /// Utilities for the MountainGoap library.
# /// </summary>
class Utils:
    """
    Utilities for the MountainGoap library.
    """

    # /// <summary>
    # /// Indicates whether a is lower than b.
    # /// </summary>
    # /// <param name="a">First element to be compared.</param>
    # /// <param name="b">Second element to be compared.</param>
    # /// <returns>True if lower, false otherwise.</returns>
    # internal static bool IsLowerThan(object a, object b) {
    #     if (a == null || b == null) return false;
    #     if (a is int intA && b is int intB) return intA < intB;
    #     if (a is long longA && b is long longB) return longA < longB;
    #     if (a is float floatA && b is float floatB) return floatA < floatB;
    #     if (a is double doubleA && b is double doubleB) return doubleA < doubleB;
    #     if (a is decimal decimalA && b is decimal decimalB) return decimalA < decimalB;
    #     if (a is DateTime dateTimeA && b is DateTime dateTimeB) return dateTimeA < dateTimeB;
    #     return false;
    # }
    @staticmethod
    def is_lower_than(a: Any, b: Any) -> bool:
        """
        Indicates whether a is lower than b.
        """
        if a is None or b is None:
            return False
        # Python's comparison operators work for various numeric types and datetime objects directly
        # and handle mixed types if they are compatible (e.g., int vs float).
        # For explicit type checking like C#, we can use isinstance.
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a < b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a < b
        # Add other type comparisons if needed, following the C# logic.
        # Python's native comparison is generally more flexible.
        try:
            return a < b
        except TypeError:
            return False


    # /// <summary>
    # /// Indicates whether a is higher than b.
    # /// </summary>
    # /// <param name="a">First element to be compared.</param>
    # /// <param name="b">Second element to be compared.</param>
    # /// <returns>True if higher, false otherwise.</returns>
    # internal static bool IsHigherThan(object a, object b) {
    #     ... similar logic ...
    # }
    @staticmethod
    def is_higher_than(a: Any, b: Any) -> bool:
        """
        Indicates whether a is higher than b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a > b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a > b
        try:
            return a > b
        except TypeError:
            return False

    # /// <summary>
    # /// Indicates whether a is lower than or equal to b.
    # /// </summary>
    # /// <param name="a">First element to be compared.</param>
    # /// <param name="b">Second element to be compared.</param>
    # /// <returns>True if lower or equal, false otherwise.</returns>
    # internal static bool IsLowerThanOrEquals(object a, object b) {
    #     ... similar logic ...
    # }
    @staticmethod
    def is_lower_than_or_equals(a: Any, b: Any) -> bool:
        """
        Indicates whether a is lower than or equal to b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a <= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a <= b
        try:
            return a <= b
        except TypeError:
            return False

    # /// <summary>
    # /// Indicates whether a is higher than or equal to b.
    # /// </summary>
    # /// <param name="a">First element to be compared.</param>
    # /// <param name="b">Second element to be compared.</param>
    # /// <returns>True if higher or equal, false otherwise.</returns>
    # internal static bool IsHigherThanOrEquals(object a, object b) {
    #     ... similar logic ...
    # }
    @staticmethod
    def is_higher_than_or_equals(a: Any, b: Any) -> bool:
        """
        Indicates whether a is higher than or equal to b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a >= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a >= b
        try:
            return a >= b
        except TypeError:
            return False

    # /// <summary>
    # /// Indicates whether or not a goal is met by an action node.
    # /// </summary>
    # /// <param name="goal">Goal to be met.</param>
    # /// <param name="actionNode">Action node being tested.</param>
    # /// <param name="current">Prior node in the action chain.</param>
    # /// <returns>True if the goal is met, otherwise false.</returns>
    # internal static bool MeetsGoal(BaseGoal goal, ActionNode actionNode, ActionNode current) {
    #     ... logic ...
    # }
    @staticmethod
    def meets_goal(goal: 'BaseGoal', action_node: 'ActionNode', current: 'ActionNode') -> bool:
        """
        Indicates whether or not a goal is met by an action node.
        """
        from ..Goal import Goal # Import locally to avoid circular dependency issues
        from ..ExtremeGoal import ExtremeGoal
        from ..ComparativeGoal import ComparativeGoal
        from ..ComparisonOperator import ComparisonOperator

        if isinstance(goal, Goal):
            for key, desired_value in goal.DesiredState.items():
                if key not in action_node.State:
                    return False
                current_value = action_node.State[key]
                if current_value is None and desired_value is not None:
                    return False
                elif current_value is not None and current_value != desired_value:
                    return False
            return True
        elif isinstance(goal, ExtremeGoal):
            if action_node.Action is None:
                return False
            for key, maximize in goal.DesiredState.items():
                if key not in action_node.State or key not in current.State:
                    return False

                current_value = action_node.State[key]
                previous_value = current.State[key]

                if maximize:
                    if not Utils.is_higher_than_or_equals(current_value, previous_value):
                        return False
                else: # minimize
                    if not Utils.is_lower_than_or_equals(current_value, previous_value):
                        return False
            return True
        elif isinstance(goal, ComparativeGoal):
            if action_node.Action is None:
                return False
            for key, comparison_value_pair in goal.DesiredState.items():
                if key not in action_node.State or key not in current.State: # C# checks against current.State, not necessarily needed for meeting goal, but for consistency.
                    return False

                current_value = action_node.State[key]
                desired_value = comparison_value_pair.Value
                operator = comparison_value_pair.Operator

                if operator == ComparisonOperator.Undefined:
                    return False
                elif operator == ComparisonOperator.Equals:
                    if current_value != desired_value:
                        return False
                elif operator == ComparisonOperator.LessThan:
                    if not Utils.is_lower_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThan:
                    if not Utils.is_higher_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if not Utils.is_lower_than_or_equals(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if not Utils.is_higher_than_or_equals(current_value, desired_value):
                        return False
            return True
        return False

```

---

**MountainGoap/Internals/ActionNode.py**

```python
# // <copyright file="ActionNode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, TYPE_CHECKING
from ..PriorityQueue.FastPriorityQueueNode import FastPriorityQueueNode
from .DictionaryExtensionMethods import DictionaryExtensionMethods

if TYPE_CHECKING:
    from ..Action import Action

# /// <summary>
# /// Represents an action node in an action graph.
# /// </summary>
class ActionNode(FastPriorityQueueNode):
    """
    Represents an action node in an action graph.
    """

    # /// <summary>
    # /// Gets or sets the state of the world for this action node.
    # /// </summary>
    # public ConcurrentDictionary<string, object?> State { get; set; }
    State: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Gets or sets parameters to be passed to the action.
    # /// </summary>
    # public Dictionary<string, object?> Parameters { get; set; }
    Parameters: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Gets or sets the action to be executed when the world is in the defined <see cref="State"/>.
    # /// </summary>
    # public Action? Action { get; set; }
    Action: Optional['Action']

    # /// <summary>
    # /// Initializes a new instance of the <see cref="ActionNode"/> class.
    # /// </summary>
    # /// <param name="action">Action to be assigned to the node.</param>
    # /// <param name="state">State to be assigned to the node.</param>
    # /// <param name="parameters">Parameters to be passed to the action in the node.</param>
    # internal ActionNode(Action? action, ConcurrentDictionary<string, object?> state, Dictionary<string, object?> parameters) {
    #     if (action != null) Action = action.Copy();
    #     State = state.Copy();
    #     Parameters = parameters.Copy();
    #     Action?.SetParameters(Parameters);
    # }
    def __init__(self, action: Optional['Action'], state: Dict[str, Optional[Any]], parameters: Dict[str, Optional[Any]]):
        """
        Initializes a new instance of the ActionNode class.
        """
        super().__init__()
        self.Action = action.copy() if action is not None else None
        self.State = DictionaryExtensionMethods.copy_concurrent_dict(state) # Simulating ConcurrentDictionary copy
        self.Parameters = DictionaryExtensionMethods.copy_dict(parameters)

        if self.Action is not None:
            self.Action.set_parameters(self.Parameters)

    # #pragma warning disable S3875 // "operator==" should not be overloaded on reference types
    # /// <summary>
    # /// Overrides the equality operator on ActionNodes.
    # /// </summary>
    # /// <param name="node1">First node to be compared.</param>
    # /// <param name="node2">Second node to be compared.</param>
    # /// <returns>True if equal, otherwise false.</returns>
    # public static bool operator ==(ActionNode? node1, ActionNode? node2) {
    #     if (node1 is null) return node2 is null;
    #     if (node2 is null) return node1 is null;
    #     if (node1.Action == null || node2.Action == null) return (node1.Action == node2.Action) && node1.StateMatches(node2);
    #     return node1.Action.Equals(node2.Action) && node1.StateMatches(node2);
    # }
    def __eq__(self, other: object) -> bool:
        """
        Overrides the equality operator on ActionNodes.
        """
        if not isinstance(other, ActionNode):
            return NotImplemented # Or return False directly if strict type comparison is desired

        if self is other: # Optimization: if same object
            return True

        # Check Action equality
        if self.Action is None:
            if other.Action is not None:
                return False
        elif other.Action is None:
            return False
        elif not self.Action.__eq__(other.Action): # Assuming Action class implements __eq__
            return False

        # Check State equality
        return self._state_matches(other)


    # /// <summary>
    # /// Overrides the inequality operator on ActionNodes.
    # /// </summary>
    # /// <param name="node1">First node to be compared.</param>
    # /// <param name="node2">Second node to be compared.</param>
    # /// <returns>True if unequal, otherwise false.</returns>
    # public static bool operator !=(ActionNode? node1, ActionNode? node2) {
    #     if (node1 is null) return node2 is not null;
    #     if (node2 is null) return node1 is not null;
    #     if (node1.Action is not null) return !node1.Action.Equals(node2.Action) || !node1.StateMatches(node2);
    #     return node2.Action is null;
    # }
    def __ne__(self, other: object) -> bool:
        """
        Overrides the inequality operator on ActionNodes.
        """
        return not self.__eq__(other)

    # /// <inheritdoc/>
    # public override bool Equals(object? obj) {
    #     if (obj is not ActionNode item) return false;
    #     return this == item;
    # }
    # This is handled by __eq__ in Python directly.

    # /// <inheritdoc/>
    # public override int GetHashCode() {
    #     var hashCode = 629302477;
    #     if (Action != null) hashCode = (hashCode * -1521134295) + EqualityComparer<Action>.Default.GetHashCode(Action);
    #     else hashCode *= -1521134295;
    #     hashCode = (hashCode * -1521134295) + EqualityComparer<ConcurrentDictionary<string, object?>>.Default.GetHashCode(State);
    #     return hashCode;
    # }
    def __hash__(self) -> int:
        """
        Overrides the hash code generation for ActionNodes.
        A hashable representation of the state is needed.
        """
        # For hashing, dictionaries are not hashable by default.
        # We need a canonical representation of the state dictionary.
        # Convert dictionary to a sorted tuple of (key, value) pairs.
        state_tuple = tuple(sorted(self.State.items()))
        
        # Ensure action is hashable, or use its hash directly if it has one.
        # If Action is a custom object and not hashable, we'd need to define its __hash__
        # For now, if Action.Name is unique enough, we can use that, or a default hash.
        action_hash = hash(self.Action) if self.Action is not None else hash(None)
        
        return hash((action_hash, state_tuple))

    # /// <summary>
    # /// Cost to traverse this node.
    # /// </summary>
    # /// <param name="currentState">Current state after previous node is executed.</param>
    # /// <returns>The cost of the action to be executed.</returns>
    # internal float Cost(ConcurrentDictionary<string, object?> currentState) {
    #     if (Action == null) return float.MaxValue;
    #     return Action.GetCost(currentState);
    # }
    def cost(self, current_state: Dict[str, Optional[Any]]) -> float:
        """
        Cost to traverse this node.
        """
        if self.Action is None:
            return float('inf') # float.MaxValue in C#
        return self.Action.get_cost(current_state)

    # private bool StateMatches(ActionNode otherNode) {
    #     foreach (var kvp in State) {
    #         if (!otherNode.State.ContainsKey(kvp.Key)) return false;
    #         if (otherNode.State[kvp.Key] == null && otherNode.State[kvp.Key] != kvp.Value) return false;
    #         else if (otherNode.State[kvp.Key] == null && otherNode.State[kvp.Key] == kvp.Value) continue;
    #         if (otherNode.State[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
    #     }
    #     foreach (var kvp in otherNode.State) {
    #         if (!State.ContainsKey(kvp.Key)) return false;
    #         if (State[kvp.Key] == null && State[kvp.Key] != kvp.Value) return false;
    #         else if (State[kvp.Key] == null && State[kvp.Key] == kvp.Value) continue;
    #         if (otherNode.State[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
    #     }
    #     return true;
    # }
    def _state_matches(self, other_node: 'ActionNode') -> bool:
        """
        Compares the state of this node with another node for equality.
        """
        # A simpler way to check if two dictionaries have the same keys and values
        # This handles cases where values might be None correctly.
        # It also handles different types (int vs float) correctly if Python's `==` allows it.
        return self.State == other_node.State

```

---

**MountainGoap/Action.py**

```python
# // <copyright file="Action.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Dict, Any, Optional, List, Callable, Tuple, cast
from datetime import datetime, timedelta

from .CallbackDelegates.CostCallback import CostCallback
from .CallbackDelegates.ExecutorCallback import ExecutorCallback
from .CallbackDelegates.PermutationSelectorCallback import PermutationSelectorCallback
from .CallbackDelegates.StateCheckerCallback import StateCheckerCallback
from .CallbackDelegates.StateCostDeltaMultiplierCallback import StateCostDeltaMultiplierCallback
from .CallbackDelegates.StateMutatorCallback import StateMutatorCallback

from .ComparisonOperator import ComparisonOperator
from .ComparisonValuePair import ComparisonValuePair
from .ExecutionStatus import ExecutionStatus
from .Internals.DictionaryExtensionMethods import DictionaryExtensionMethods
from .Internals.Utils import Utils

from .Events.BeginExecuteActionEvent import BeginExecuteActionEvent
from .Events.FinishExecuteActionEvent import FinishExecuteActionEvent

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

# /// <summary>
# /// Represents an action in a GOAP system.
# /// </summary>
class Action:
    """
    Represents an action in a GOAP system.
    """

    # /// <summary>
    # /// Name of the action.
    # /// </summary>
    # public readonly string Name;
    Name: str

    # /// <summary>
    # /// Cost of the action.
    # /// </summary>
    # private readonly float cost;
    _cost_base: float

    # /// <summary>
    # /// The permutation selector callbacks for the action.
    # /// </summary>
    # private readonly Dictionary<string, PermutationSelectorCallback> permutationSelectors;
    _permutation_selectors: Dict[str, PermutationSelectorCallback]

    # /// <summary>
    # /// The executor callback for the action.
    # /// </summary>
    # private readonly ExecutorCallback executor;
    _executor: ExecutorCallback

    # /// <summary>
    # /// The cost callback for the action.
    # /// </summary>
    # private readonly CostCallback costCallback;
    _cost_callback: CostCallback

    # /// <summary>
    # /// Preconditions for the action. These things are required for the action to execute.
    # /// </summary>
    # private readonly Dictionary<string, object?> preconditions = new();
    _preconditions: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Comparative preconditions for the action. Indicates that a value must be greater than or less than a certain value for the action to execute.
    # /// </summary>
    # private readonly Dictionary<string, ComparisonValuePair> comparativePreconditions = new();
    _comparative_preconditions: Dict[str, ComparisonValuePair]

    # /// <summary>
    # /// Postconditions for the action. These will be set when the action has executed.
    # /// </summary>
    # private readonly Dictionary<string, object?> postconditions = new();
    _postconditions: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Arithmetic postconditions for the action. These will be added to the current value when the action has executed.
    # /// </summary>
    # private readonly Dictionary<string, object> arithmeticPostconditions = new();
    _arithmetic_postconditions: Dict[str, Any] # Non-nullable in C#

    # /// <summary>
    # /// Parameter postconditions for the action. When the action has executed, the value of the parameter given in the key will be copied to the state with the name given in the value.
    # /// </summary>
    # private readonly Dictionary<string, string> parameterPostconditions = new();
    _parameter_postconditions: Dict[str, str]

    # /// <summary>
    # /// State mutator for modifying state programmatically after action execution or evaluation.
    # /// </summary>
    # private readonly StateMutatorCallback? stateMutator;
    _state_mutator: Optional[StateMutatorCallback]

    # /// <summary>
    # /// State checker for checking state programmatically before action execution or evaluation.
    # /// </summary>
    # private readonly StateCheckerCallback? stateChecker;
    _state_checker: Optional[StateCheckerCallback]

    # /// <summary>
    # /// Parameters to be passed to the action.
    # /// </summary>
    # private Dictionary<string, object?> parameters = new();
    _parameters: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Multiplier for delta value to provide delta cost.
    # /// </summary>
    # public StateCostDeltaMultiplierCallback? StateCostDeltaMultiplier { get; set; }
    StateCostDeltaMultiplier: Optional[StateCostDeltaMultiplierCallback]

    # Events (static in C#)
    OnBeginExecuteAction: BeginExecuteActionEvent
    OnFinishExecuteAction: FinishExecuteActionEvent

    # /// <summary>
    # /// Gets or sets the execution status of the action.
    # /// </summary>
    # internal ExecutionStatus ExecutionStatus { get; set; } = ExecutionStatus.NotYetExecuted;
    ExecutionStatus: ExecutionStatus = ExecutionStatus.NotYetExecuted

    # /// <summary>
    # /// Initializes a new instance of the <see cref="Action"/> class.
    # /// </summary>
    # public Action(string? name = null, Dictionary<string, PermutationSelectorCallback>? permutationSelectors = null, ExecutorCallback? executor = null, float cost = 1f, CostCallback? costCallback = null, Dictionary<string, object?>? preconditions = null, Dictionary<string, ComparisonValuePair>? comparativePreconditions = null, Dictionary<string, object?>? postconditions = null, Dictionary<string, object>? arithmeticPostconditions = null, Dictionary<string, string>? parameterPostconditions = null, StateMutatorCallback? stateMutator = null, StateCheckerCallback? stateChecker = null, StateCostDeltaMultiplierCallback? stateCostDeltaMultiplier = null) {
    #     if (permutationSelectors == null) this.permutationSelectors = new();
    #     else this.permutationSelectors = permutationSelectors;
    #     if (executor == null) this.executor = DefaultExecutorCallback;
    #     else this.executor = executor;
    #     Name = name ?? $"Action {Guid.NewGuid()} ({this.executor.GetMethodInfo().Name})";
    #     this.cost = cost;
    #     this.costCallback = costCallback ?? DefaultCostCallback;
    #     if (preconditions != null) this.preconditions = preconditions;
    #     if (comparativePreconditions != null) this.comparativePreconditions = comparativePreconditions;
    #     if (postconditions != null) this.postconditions = postconditions;
    #     if (arithmeticPostconditions != null) this.arithmeticPostconditions = arithmeticPostconditions;
    #     if (parameterPostconditions != null) this.parameterPostconditions = parameterPostconditions;
    #     if (stateMutator != null) this.stateMutator = stateMutator;
    #     if (stateChecker != null) this.stateChecker = stateChecker;
    #     StateCostDeltaMultiplier = stateCostDeltaMultiplier ?? DefaultStateCostDeltaMultiplier;
    # }
    def __init__(self,
                 name: Optional[str] = None,
                 permutation_selectors: Optional[Dict[str, PermutationSelectorCallback]] = None,
                 executor: Optional[ExecutorCallback] = None,
                 cost: float = 1.0,
                 cost_callback: Optional[CostCallback] = None,
                 preconditions: Optional[Dict[str, Optional[Any]]] = None,
                 comparative_preconditions: Optional[Dict[str, ComparisonValuePair]] = None,
                 postconditions: Optional[Dict[str, Optional[Any]]] = None,
                 arithmetic_postconditions: Optional[Dict[str, Any]] = None,
                 parameter_postconditions: Optional[Dict[str, str]] = None,
                 state_mutator: Optional[StateMutatorCallback] = None,
                 state_checker: Optional[StateCheckerCallback] = None,
                 state_cost_delta_multiplier: Optional[StateCostDeltaMultiplierCallback] = None):
        """
        Initializes a new instance of the Action class.
        """
        self._permutation_selectors = permutation_selectors if permutation_selectors is not None else {}
        self._executor = executor if executor is not None else Action._default_executor_callback
        
        # In C#, GetMethodInfo().Name is used for default name.
        # In Python, we can get the function's __name__ attribute.
        executor_name = self._executor.__name__ if hasattr(self._executor, '__name__') else str(self._executor)
        self.Name = name if name is not None else f"Action {uuid.uuid4()} ({executor_name})"
        
        self._cost_base = cost
        self._cost_callback = cost_callback if cost_callback is not None else Action._default_cost_callback
        
        self._preconditions = preconditions if preconditions is not None else {}
        self._comparative_preconditions = comparative_preconditions if comparative_preconditions is not None else {}
        self._postconditions = postconditions if postconditions is not None else {}
        self._arithmetic_postconditions = arithmetic_postconditions if arithmetic_postconditions is not None else {}
        self._parameter_postconditions = parameter_postconditions if parameter_postconditions is not None else {}
        
        self._state_mutator = state_mutator
        self._state_checker = state_checker
        self.StateCostDeltaMultiplier = state_cost_delta_multiplier if state_cost_delta_multiplier is not None else Action.default_state_cost_delta_multiplier

        self._parameters = {}

        # Initialize static events (class attributes in Python)
        # Note: Event handling in Python is often done via simple callable lists or a custom Event class.
        # Here, we'll use a callable that calls into a list of registered handlers.
        # This setup needs to be done once, typically at the module level or by a dedicated event manager.
        # For simplicity, we'll make them static/class methods and handle registration.
        # In C#, `+= (agent, action, parameters) => { }` means if no handler is registered, it's an empty anonymous method.
        # In Python, an empty list of handlers implies no action, or a dummy default handler.

    # Static event-like attributes (class variables)
    _on_begin_execute_action_handlers: List[BeginExecuteActionEvent] = []
    _on_finish_execute_action_handlers: List[FinishExecuteActionEvent] = []

    @classmethod
    def OnBeginExecuteAction(cls, agent: 'Agent', action: 'Action', parameters: Dict[str, Optional[Any]]) -> None:
        for handler in cls._on_begin_execute_action_handlers:
            handler(agent, action, parameters)

    @classmethod
    def OnFinishExecuteAction(cls, agent: 'Agent', action: 'Action', status: ExecutionStatus, parameters: Dict[str, Optional[Any]]) -> None:
        for handler in cls._on_finish_execute_action_handlers:
            handler(agent, action, status, parameters)

    # Static registration methods for events
    @classmethod
    def register_on_begin_execute_action(cls, handler: BeginExecuteActionEvent):
        cls._on_begin_execute_action_handlers.append(handler)

    @classmethod
    def register_on_finish_execute_action(cls, handler: FinishExecuteActionEvent):
        cls._on_finish_execute_action_handlers.append(handler)

    # Default callbacks (static in C#)
    @staticmethod
    def default_state_cost_delta_multiplier(action: Optional['Action'], state_key: str) -> float:
        return 1.0

    @staticmethod
    def _default_executor_callback(agent: 'Agent', action: 'Action') -> ExecutionStatus:
        # from ..Agent import Agent # Local import to avoid circular dependency if not TYPE_CHECKING
        return ExecutionStatus.Failed

    @staticmethod
    def _default_cost_callback(action: 'Action', current_state: StateDictionary) -> float:
        # #pragma warning disable S1172 // Unused method parameters should be removed
        return action._cost_base
        # #pragma warning restore S1172 // Unused method parameters should be removed


    # /// <summary>
    # /// Makes a copy of the action.
    # /// </summary>
    # public Action Copy() {
    #     var newAction = new Action(Name, permutationSelectors, executor, cost, costCallback, preconditions.Copy(), comparativePreconditions.Copy(), postconditions.Copy(), arithmeticPostconditions.CopyNonNullable(), parameterPostconditions.Copy(), stateMutator, stateChecker, StateCostDeltaMultiplier) {
    #         parameters = parameters.Copy()
    #     };
    #     return newAction;
    # }
    def copy(self) -> 'Action':
        """
        Makes a copy of the action.
        """
        new_action = Action(
            name=self.Name,
            permutation_selectors=self._permutation_selectors.copy(),
            executor=self._executor,
            cost=self._cost_base,
            cost_callback=self._cost_callback,
            preconditions=DictionaryExtensionMethods.copy_dict(self._preconditions),
            comparative_preconditions=DictionaryExtensionMethods.copy_comparison_value_pair_dict(self._comparative_preconditions),
            postconditions=DictionaryExtensionMethods.copy_dict(self._postconditions),
            arithmetic_postconditions=DictionaryExtensionMethods.copy_non_nullable_dict(self._arithmetic_postconditions),
            parameter_postconditions=DictionaryExtensionMethods.copy_string_dict(self._parameter_postconditions),
            state_mutator=self._state_mutator,
            state_checker=self._state_checker,
            state_cost_delta_multiplier=self.StateCostDeltaMultiplier
        )
        new_action._parameters = DictionaryExtensionMethods.copy_dict(self._parameters) # Set after init
        return new_action

    # /// <summary>
    # /// Sets a parameter to the action.
    # /// </summary>
    # public void SetParameter(string key, object value) {
    #     parameters[key] = value;
    # }
    def set_parameter(self, key: str, value: Any) -> None:
        """
        Sets a parameter to the action.
        """
        self._parameters[key] = value

    # /// <summary>
    # /// Gets a parameter to the action.
    # /// </summary>
    # public object? GetParameter(string key) {
    #     if (parameters.ContainsKey(key)) return parameters[key];
    #     return null;
    # }
    def get_parameter(self, key: str) -> Optional[Any]:
        """
        Gets a parameter to the action.
        """
        return self._parameters.get(key)

    # /// <summary>
    # /// Gets the cost of the action.
    # /// </summary>
    # public float GetCost(ConcurrentDictionary<string, object?> currentState) {
    #     try {
    #         return costCallback(this, currentState);
    #     }
    #     catch {
    #         return float.MaxValue;
    #     }
    # }
    def get_cost(self, current_state: StateDictionary) -> float:
        """
        Gets the cost of the action.
        """
        try:
            return self._cost_callback(self, current_state)
        except Exception:
            return float('inf') # float.MaxValue in C#

    # /// <summary>
    # /// Executes a step of work for the agent.
    # /// </summary>
    # internal ExecutionStatus Execute(Agent agent) {
    #     OnBeginExecuteAction(agent, this, parameters);
    #     if (IsPossible(agent.State)) {
    #         var newState = executor(agent, this);
    #         if (newState == ExecutionStatus.Succeeded) ApplyEffects(agent.State);
    #         ExecutionStatus = newState;
    #         OnFinishExecuteAction(agent, this, ExecutionStatus, parameters);
    #         return newState;
    #     }
    #     else {
    #         OnFinishExecuteAction(agent, this, ExecutionStatus.NotPossible, parameters);
    #         return ExecutionStatus.NotPossible;
    #     }
    # }
    def execute(self, agent: 'Agent') -> ExecutionStatus:
        """
        Executes a step of work for the agent.
        """
        # Local import to avoid circular dependency
        from .Agent import Agent

        Action.OnBeginExecuteAction(agent, self, self._parameters)
        if self.is_possible(agent.State):
            new_status = self._executor(agent, self)
            if new_status == ExecutionStatus.Succeeded:
                self.apply_effects(agent.State)
            self.ExecutionStatus = new_status
            Action.OnFinishExecuteAction(agent, self, self.ExecutionStatus, self._parameters)
            return new_status
        else:
            self.ExecutionStatus = ExecutionStatus.NotPossible
            Action.OnFinishExecuteAction(agent, self, self.ExecutionStatus, self._parameters)
            return ExecutionStatus.NotPossible

    # /// <summary>
    # /// Determines whether or not an action is possible.
    # /// </summary>
    # internal bool IsPossible(ConcurrentDictionary<string, object?> state) {
    #     foreach (var kvp in preconditions) {
    #         if (!state.ContainsKey(kvp.Key)) return false;
    #         if (state[kvp.Key] == null && state[kvp.Key] != kvp.Value) return false;
    #         else if (state[kvp.Key] == null && state[kvp.Key] == kvp.Value) continue;
    #         if (state[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
    #     }
    #     foreach (var kvp in comparativePreconditions) {
    #         if (!state.ContainsKey(kvp.Key)) return false;
    #         if (state[kvp.Key] == null) return false;
    #         if (state[kvp.Key] is object obj && kvp.Value.Value is object obj2) {
    #             if (kvp.Value.Operator == ComparisonOperator.LessThan && !Utils.IsLowerThan(obj, obj2)) return false;
    #             else if (kvp.Value.Operator == ComparisonOperator.GreaterThan && !Utils.IsHigherThan(obj, obj2)) return false;
    #             else if (kvp.Value.Operator == ComparisonOperator.LessThanOrEquals && !Utils.IsLowerThanOrEquals(obj, obj2)) return false;
    #             else if (kvp.Value.Operator == ComparisonOperator.GreaterThanOrEquals && !Utils.IsHigherThanOrEquals(obj, obj2)) return false;
    #         }
    #         else return false;
    #     }
    #     if (stateChecker?.Invoke(this, state) == false) return false;
    #     return true;
    # }
    def is_possible(self, state: StateDictionary) -> bool:
        """
        Determines whether or not an action is possible.
        """
        for key, value in self._preconditions.items():
            if key not in state:
                return False
            # C# `state[kvp.Key] == null && state[kvp.Key] != kvp.Value` is a bit redundant if kvp.Key refers to a key that exists.
            # It simplifies to: if the current state value for this key is not equal to the required precondition value.
            if state[key] != value:
                return False

        for key, comp_value_pair in self._comparative_preconditions.items():
            if key not in state or state[key] is None:
                return False
            
            current_val = state[key]
            desired_val = comp_value_pair.Value
            operator = comp_value_pair.Operator

            # C# `is object obj && kvp.Value.Value is object obj2` check:
            # In Python, we rely on type hints and runtime checks for actual values.
            # If desired_val is None, it implies a malformed comparison pair if operator is not Undefined,
            # or if it's a numeric comparison.
            if desired_val is None and operator != ComparisonOperator.Undefined:
                # If the desired value for comparison is None, but the operator implies a comparison
                # that requires a non-None value, then it's not possible.
                # Example: checking if 'x < None' won't work numerically.
                # This could be made more robust by checking if current_val and desired_val are comparable types.
                # For now, following the C# logic.
                return False

            if operator == ComparisonOperator.LessThan:
                if not Utils.is_lower_than(current_val, desired_val):
                    return False
            elif operator == ComparisonOperator.GreaterThan:
                if not Utils.is_higher_than(current_val, desired_val):
                    return False
            elif operator == ComparisonOperator.LessThanOrEquals:
                if not Utils.is_lower_than_or_equals(current_val, desired_val):
                    return False
            elif operator == ComparisonOperator.GreaterThanOrEquals:
                if not Utils.is_higher_than_or_equals(current_val, desired_val):
                    return False
            # For ComparisonOperator.Equals, it's covered by the regular preconditions loop if `ComparisonValuePair`
            # had an "Equals" equivalent. But in C# `ComparisonOperator.Equals` is separate.
            # However, the `is_possible` only checks `comparativePreconditions` for `<`, `<=`, `>`, `>=`.
            # A direct equality check would be `state[key] != desired_val` which is already in the first loop.

        if self._state_checker is not None and not self._state_checker(self, state):
            return False
        return True

    # /// <summary>
    # /// Gets all permutations of parameters possible for an action.
    # /// </summary>
    # internal List<Dictionary<string, object?>> GetPermutations(ConcurrentDictionary<string, object?> state) {
    #     List<Dictionary<string, object?>> combinedOutputs = new();
    #     Dictionary<string, List<object>> outputs = new();
    #     foreach (var kvp in permutationSelectors) outputs[kvp.Key] = kvp.Value(state);
    #     var permutationParameters = outputs.Keys.ToList();
    #     List<int> indices = new();
    #     List<int> counts = new();
    #     foreach (var parameter in permutationParameters) {
    #         indices.Add(0);
    #         if (outputs[parameter].Count == 0) return combinedOutputs;
    #         counts.Add(outputs[parameter].Count);
    #     }
    #     while (true) {
    #         var singleOutput = new Dictionary<string, object?>();
    #         for (int i = 0; i < indices.Count; i++) {
    #             if (indices[i] >= outputs[permutationParameters[i]].Count) continue;
    #             singleOutput[permutationParameters[i]] = outputs[permutationParameters[i]][indices[i]];
    #         }
    #         combinedOutputs.Add(singleOutput);
    #         if (IndicesAtMaximum(indices, counts)) return combinedOutputs;
    #         IncrementIndices(indices, counts);
    #     }
    # }
    def get_permutations(self, state: StateDictionary) -> List[Dict[str, Optional[Any]]]:
        """
        Gets all permutations of parameters possible for an action.
        """
        combined_outputs: List[Dict[str, Optional[Any]]] = []
        outputs: Dict[str, List[Any]] = {}

        for key, selector_callback in self._permutation_selectors.items():
            outputs[key] = selector_callback(state)

        permutation_parameters = list(outputs.keys())
        indices = [0] * len(permutation_parameters)
        counts = [len(outputs[param]) for param in permutation_parameters]

        # If any parameter list is empty, no permutations are possible.
        if any(c == 0 for c in counts):
            return combined_outputs

        while True:
            single_output: Dict[str, Optional[Any]] = {}
            for i in range(len(indices)):
                if indices[i] >= counts[i]:
                    # This 'continue' from C# logic would mean skipping this parameter,
                    # which is usually not desired in a permutation, but verbatim implies this.
                    # A more common permutation generation would stop if indices[i] is out of bounds.
                    # For verbatim translation, we'll keep the continue.
                    continue
                param_key = permutation_parameters[i]
                single_output[param_key] = outputs[param_key][indices[i]]
            
            combined_outputs.append(single_output)

            if Action._indices_at_maximum(indices, counts):
                return combined_outputs
            
            Action._increment_indices(indices, counts)

    # /// <summary>
    # /// Applies the effects of the action.
    # /// </summary>
    # internal void ApplyEffects(ConcurrentDictionary<string, object?> state) {
    #     foreach (var kvp in postconditions) state[kvp.Key] = kvp.Value;
    #     foreach (var kvp in arithmeticPostconditions) {
    #         if (!state.ContainsKey(kvp.Key)) continue;
    #         if (state[kvp.Key] is int stateInt && kvp.Value is int conditionInt) state[kvp.Key] = stateInt + conditionInt;
    #         else if (state[kvp.Key] is float stateFloat && kvp.Value is float conditionFloat) state[kvp.Key] = stateFloat + conditionFloat;
    #         else if (state[kvp.Key] is double stateDouble && kvp.Value is double conditionDouble) state[kvp.Key] = stateDouble + conditionDouble;
    #         else if (state[kvp.Key] is long stateLong && kvp.Value is long conditionLong) state[kvp.Key] = stateLong + conditionLong;
    #         else if (state[kvp.Key] is decimal stateDecimal && kvp.Value is decimal conditionDecimal) state[kvp.Key] = stateDecimal + conditionDecimal;
    #         else if (state[kvp.Key] is DateTime stateDateTime && kvp.Value is TimeSpan conditionTimeSpan) state[kvp.Key] = stateDateTime + conditionTimeSpan;
    #     }
    #     foreach (var kvp in parameterPostconditions) {
    #         if (!parameters.ContainsKey(kvp.Key)) continue;
    #         state[kvp.Value] = parameters[kvp.Key];
    #     }
    #     stateMutator?.Invoke(this, state);
    # }
    def apply_effects(self, state: StateDictionary) -> None:
        """
        Applies the effects of the action.
        """
        for key, value in self._postconditions.items():
            state[key] = value

        for key, value_to_add in self._arithmetic_postconditions.items():
            if key not in state:
                continue

            current_value = state[key]

            # Python handles arithmetic operations for mixed numeric types automatically.
            # For datetime + timedelta, we need specific handling.
            if isinstance(current_value, (int, float)) and isinstance(value_to_add, (int, float)):
                state[key] = current_value + value_to_add
            elif isinstance(current_value, datetime) and isinstance(value_to_add, timedelta):
                state[key] = current_value + value_to_add
            # Add other specific type combinations if they exist in C# (e.g. long, decimal not native in Python as distinct types)
            # Python's `int` handles arbitrary precision integers, so it covers `long`.
            # `float` covers `double`. `decimal` would require `Decimal` type from `decimal` module.
            else:
                # If types are not directly addable or known, skip.
                # For more strict verbatim, convert to float if possible for addition.
                try:
                    state[key] = cast(Any, current_value) + cast(Any, value_to_add)
                except TypeError:
                    pass # Or log a warning/error

        for param_key, state_key in self._parameter_postconditions.items():
            if param_key not in self._parameters:
                continue
            state[state_key] = self._parameters[param_key]

        if self._state_mutator is not None:
            self._state_mutator(self, state)

    # /// <summary>
    # /// Sets all parameters to the action.
    # /// </summary>
    # internal void SetParameters(Dictionary<string, object?> parameters) {
    #     this.parameters = parameters;
    # }
    def set_parameters(self, parameters: Dict[str, Optional[Any]]) -> None:
        """
        Sets all parameters to the action.
        """
        self._parameters = parameters

    # private static bool IndicesAtMaximum(List<int> indices, List<int> counts) {
    #     for (int i = 0; i < indices.Count; i++) if (indices[i] < counts[i] - 1) return false;
    #     return true;
    # }
    @staticmethod
    def _indices_at_maximum(indices: List[int], counts: List[int]) -> bool:
        """
        Checks if all indices are at their maximum allowed value (last element of their respective list).
        """
        for i in range(len(indices)):
            if indices[i] < counts[i] - 1:
                return False
        return True

    # private static void IncrementIndices(List<int> indices, List<int> counts) {
    #     if (IndicesAtMaximum(indices, counts)) return;
    #     for (int i = 0; i < indices.Count; i++) {
    #         if (indices[i] == counts[i] - 1) indices[i] = 0;
    #         else {
    #             indices[i]++;
    #             return;
    #         }
    #     }
    # }
    @staticmethod
    def _increment_indices(indices: List[int], counts: List[int]) -> None:
        """
        Increments indices to generate the next permutation.
        """
        if Action._indices_at_maximum(indices, counts):
            return # All combinations exhausted

        for i in range(len(indices)):
            if indices[i] == counts[i] - 1:
                indices[i] = 0 # Wrap around
            else:
                indices[i] += 1
                return # Found the position to increment, done for this step

    def __hash__(self) -> int:
        """
        Provides a hash for the Action instance.
        Necessary for ActionNode equality and hashing.
        """
        # Hash based on Name, which should be unique enough for most purposes.
        return hash(self.Name)

    def __eq__(self, other: object) -> bool:
        """
        Provides equality comparison for Action instances.
        Necessary for ActionNode equality.
        """
        if not isinstance(other, Action):
            return NotImplemented
        return self.Name == other.Name

```

---

**MountainGoap/Agent.py**

```python
# // <copyright file="Agent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Dict, Any, Optional, List
import threading # For Thread and ConcurrentDictionary behavior (though we use plain dict)

from .BaseGoal import BaseGoal
from .Action import Action
from .Sensor import Sensor
from .StepMode import StepMode
from .ExecutionStatus import ExecutionStatus
from .Internals.Planner import Planner
from .Internals.ActionNode import ActionNode # For event type hints

from .Events.AgentActionSequenceCompletedEvent import AgentActionSequenceCompletedEvent
from .Events.AgentStepEvent import AgentStepEvent
from .Events.PlanningStartedEvent import PlanningStartedEvent
from .Events.PlanningStartedForSingleGoalEvent import PlanningStartedForSingleGoalEvent
from .Events.PlanningFinishedForSingleGoalEvent import PlanningFinishedForSingleGoalEvent
from .Events.PlanningFinishedEvent import PlanningFinishedEvent
from .Events.PlanUpdatedEvent import PlanUpdatedEvent
from .Events.EvaluatedActionNodeEvent import EvaluatedActionNodeEvent

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

# /// <summary>
# /// GOAP agent.
# /// </summary>
class Agent:
    """
    GOAP agent.
    """

    # /// <summary>
    # /// Name of the agent.
    # /// </summary>
    # public readonly string Name;
    Name: str

    # /// <summary>
    # /// Gets the chains of actions currently being performed by the agent.
    # /// </summary>
    # public List<List<Action>> CurrentActionSequences { get; } = new();
    CurrentActionSequences: List[List[Action]]

    # /// <summary>
    # /// Gets or sets the current world state from the agent perspective.
    # /// </summary>
    # public ConcurrentDictionary<string, object?> State { get; set; } = new();
    State: StateDictionary

    # /// <summary>
    # /// Gets or sets the memory storage object for the agent.
    # /// </summary>
    # public Dictionary<string, object?> Memory { get; set; } = new();
    Memory: Dict[str, Optional[Any]]

    # /// <summary>
    # /// Gets or sets the list of active goals for the agent.
    # /// </summary>
    # public List<BaseGoal> Goals { get; set; } = new();
    Goals: List[BaseGoal]

    # /// <summary>
    # /// Gets or sets the actions available to the agent.
    # /// </summary>
    # public List<Action> Actions { get; set; } = new();
    Actions: List[Action]

    # /// <summary>
    # /// Gets or sets the sensors available to the agent.
    # /// </summary>
    # public List<Sensor> Sensors { get; set; } = new();
    Sensors: List[Sensor]

    # /// <summary>
    # /// Gets or sets the plan cost maximum for the agent.
    # /// </summary>
    # public float CostMaximum { get; set; }
    CostMaximum: float

    # /// <summary>
    # /// Gets or sets the step maximum for the agent.
    # /// </summary>
    # public int StepMaximum { get; set; }
    StepMaximum: int

    # /// <summary>
    # /// Gets or sets a value indicating whether the agent is currently executing one or more actions.
    # /// </summary>
    # public bool IsBusy { get; set; } = false;
    IsBusy: bool = False

    # /// <summary>
    # /// Gets or sets a value indicating whether the agent is currently planning.
    # /// </summary>
    # public bool IsPlanning { get; set; } = false;
    IsPlanning: bool = False

    # Events (class attributes, handlers stored in lists)
    _on_agent_step_handlers: List[AgentStepEvent] = []
    _on_agent_action_sequence_completed_handlers: List[AgentActionSequenceCompletedEvent] = []
    _on_planning_started_handlers: List[PlanningStartedEvent] = []
    _on_planning_started_for_single_goal_handlers: List[PlanningStartedForSingleGoalEvent] = []
    _on_planning_finished_for_single_goal_handlers: List[PlanningFinishedForSingleGoalEvent] = []
    _on_planning_finished_handlers: List[PlanningFinishedEvent] = []
    _on_plan_updated_handlers: List[PlanUpdatedEvent] = []
    _on_evaluated_action_node_handlers: List[EvaluatedActionNodeEvent] = []

    # C# events are public static, Python equivalent is a classmethod that invokes handlers
    @classmethod
    def OnAgentStep(cls, agent: 'Agent'):
        for handler in cls._on_agent_step_handlers:
            handler(agent)

    @classmethod
    def OnAgentActionSequenceCompleted(cls, agent: 'Agent'):
        for handler in cls._on_agent_action_sequence_completed_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStarted(cls, agent: 'Agent'):
        for handler in cls._on_planning_started_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStartedForSingleGoal(cls, agent: 'Agent', goal: BaseGoal):
        for handler in cls._on_planning_started_for_single_goal_handlers:
            handler(agent, goal)

    @classmethod
    def OnPlanningFinishedForSingleGoal(cls, agent: 'Agent', goal: BaseGoal, utility: float):
        for handler in cls._on_planning_finished_for_single_goal_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanningFinished(cls, agent: 'Agent', goal: Optional[BaseGoal], utility: float):
        for handler in cls._on_planning_finished_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanUpdated(cls, agent: 'Agent', action_list: List[Action]):
        for handler in cls._on_plan_updated_handlers:
            handler(agent, action_list)

    @classmethod
    def OnEvaluatedActionNode(cls, node: ActionNode, nodes: Dict[ActionNode, ActionNode]):
        for handler in cls._on_evaluated_action_node_handlers:
            handler(node, nodes)
    
    # Registration methods for external logging/monitoring to attach handlers
    @classmethod
    def register_on_agent_step(cls, handler: AgentStepEvent): cls._on_agent_step_handlers.append(handler)
    @classmethod
    def register_on_agent_action_sequence_completed(cls, handler: AgentActionSequenceCompletedEvent): cls._on_agent_action_sequence_completed_handlers.append(handler)
    @classmethod
    def register_on_planning_started(cls, handler: PlanningStartedEvent): cls._on_planning_started_handlers.append(handler)
    @classmethod
    def register_on_planning_started_for_single_goal(cls, handler: PlanningStartedForSingleGoalEvent): cls._on_planning_started_for_single_goal_handlers.append(handler)
    @classmethod
    def register_on_planning_finished_for_single_goal(cls, handler: PlanningFinishedForSingleGoalEvent): cls._on_planning_finished_for_single_goal_handlers.append(handler)
    @classmethod
    def register_on_planning_finished(cls, handler: PlanningFinishedEvent): cls._on_planning_finished_handlers.append(handler)
    @classmethod
    def register_on_plan_updated(cls, handler: PlanUpdatedEvent): cls._on_plan_updated_handlers.append(handler)
    @classmethod
    def register_on_evaluated_action_node(cls, handler: EvaluatedActionNodeEvent): cls._on_evaluated_action_node_handlers.append(handler)


    # /// <summary>
    # /// Initializes a new instance of the <see cref="Agent"/> class.
    # /// </summary>
    # public Agent(string? name = null, ConcurrentDictionary<string, object?>? state = null, Dictionary<string, object?>? memory = null, List<BaseGoal>? goals = null, List<Action>? actions = null, List<Sensor>? sensors = null, float costMaximum = float.MaxValue, int stepMaximum = int.MaxValue) {
    #     Name = name ?? $"Agent {Guid.NewGuid()}";
    #     if (state != null) State = state;
    #     if (memory != null) Memory = memory;
    #     if (goals != null) Goals = goals;
    #     if (actions != null) Actions = actions;
    #     if (sensors != null) Sensors = sensors;
    #     CostMaximum = costMaximum;
    #     StepMaximum = stepMaximum;
    # }
    def __init__(self,
                 name: Optional[str] = None,
                 state: Optional[StateDictionary] = None,
                 memory: Optional[Dict[str, Optional[Any]]] = None,
                 goals: Optional[List[BaseGoal]] = None,
                 actions: Optional[List[Action]] = None,
                 sensors: Optional[List[Sensor]] = None,
                 cost_maximum: float = float('inf'), # float.MaxValue in C#
                 step_maximum: int = float('inf') # int.MaxValue in C# (using float('inf') for consistency, though int limit is high)
                 ):
        """
        Initializes a new instance of the Agent class.
        """
        self.Name = name if name is not None else f"Agent {uuid.uuid4()}"
        self.State = state if state is not None else {}
        self.Memory = memory if memory is not None else {}
        self.Goals = goals if goals is not None else []
        self.Actions = actions if actions is not None else []
        self.Sensors = sensors if sensors is not None else []
        self.CostMaximum = cost_maximum
        self.StepMaximum = step_maximum

        self.CurrentActionSequences = []
        self.IsBusy = False
        self.IsPlanning = False


    # /// <summary>
    # /// You should call this every time your game state updates.
    # /// </summary>
    # public void Step(StepMode mode = StepMode.Default) {
    #     OnAgentStep(this);
    #     foreach (var sensor in Sensors) sensor.Run(this);
    #     if (mode == StepMode.Default) {
    #         StepAsync();
    #         return;
    #     }
    #     if (!IsBusy) Planner.Plan(this, CostMaximum, StepMaximum);
    #     if (mode == StepMode.OneAction) Execute();
    #     else if (mode == StepMode.AllActions) while (IsBusy) Execute();
    # }
    def step(self, mode: StepMode = StepMode.Default) -> None:
        """
        You should call this every time your game state updates.
        """
        Agent.OnAgentStep(self)
        for sensor in self.Sensors:
            sensor.run(self)

        if mode == StepMode.Default:
            self._step_async()
            return

        if not self.IsBusy:
            Planner.plan(self, self.CostMaximum, self.StepMaximum)
        
        if mode == StepMode.OneAction:
            self._execute()
        elif mode == StepMode.AllActions:
            while self.IsBusy: # Loop until plan is fully executed or becomes impossible
                self._execute()
                # Important: After each execute, re-check IsBusy, which is updated by _execute itself.
                # Also, if a plan becomes impossible, it will stop setting IsBusy to True.
                # If a plan is exhausted, IsBusy will be False.


    # /// <summary>
    # /// Clears the current action sequences (also known as plans).
    # /// </summary>
    # public void ClearPlan() {
    #     CurrentActionSequences.Clear();
    # }
    def clear_plan(self) -> None:
        """
        Clears the current action sequences (also known as plans).
        """
        self.CurrentActionSequences.clear()

    # /// <summary>
    # /// Makes a plan.
    # /// </summary>
    # public void Plan() {
    #     if (!IsBusy && !IsPlanning) {
    #         IsPlanning = true;
    #         Planner.Plan(this, CostMaximum, StepMaximum);
    #     }
    # }
    def plan(self) -> None:
        """
        Makes a plan.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            Planner.plan(self, self.CostMaximum, self.StepMaximum)

    # /// <summary>
    # /// Makes a plan asynchronously.
    # /// </summary>
    # public void PlanAsync() {
    #     if (!IsBusy && !IsPlanning) {
    #         IsPlanning = true;
    #         var t = new Thread(new ThreadStart(() => { Planner.Plan(this, CostMaximum, StepMaximum); }));
    #         t.Start();
    #     }
    # }
    def plan_async(self) -> None:
        """
        Makes a plan asynchronously.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum))
            thread.start()

    # /// <summary>
    # /// Executes the current plan.
    # /// </summary>
    # public void ExecutePlan() {
    #     if (!IsPlanning) Execute();
    # }
    def execute_plan(self) -> None:
        """
        Executes the current plan.
        """
        if not self.IsPlanning:
            self._execute()

    # /// <summary>
    # /// Triggers OnPlanningStarted event.
    # /// </summary>
    # internal static void TriggerOnPlanningStarted(Agent agent) {
    #     OnPlanningStarted(agent);
    # }
    # These static trigger methods are replaced by direct calls to the classmethod On... methods.
    # For external modules, they would call Agent.OnPlanningStarted(agent) etc.

    # /// <summary>
    # /// Executes an asynchronous step of agent work.
    # /// </summary>
    # private void StepAsync() {
    #     if (!IsBusy && !IsPlanning) {
    #         IsPlanning = true;
    #         var t = new Thread(new ThreadStart(() => { Planner.Plan(this, CostMaximum, StepMaximum); }));
    #         t.Start();
    #     }
    #     else if (!IsPlanning) Execute();
    # }
    def _step_async(self) -> None:
        """
        Executes an asynchronous step of agent work.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum))
            thread.start()
        elif not self.IsPlanning:
            self._execute()

    # /// <summary>
    # /// Executes the current action sequences.
    # /// </summary>
    # private void Execute() {
    #     if (CurrentActionSequences.Count > 0) {
    #         List<List<Action>> cullableSequences = new();
    #         foreach (var sequence in CurrentActionSequences) {
    #             if (sequence.Count > 0) {
    #                 var executionStatus = sequence[0].Execute(this);
    #                 if (executionStatus != ExecutionStatus.Executing) sequence.RemoveAt(0);
    #             }
    #             else cullableSequences.Add(sequence);
    #         }
    #         foreach (var sequence in cullableSequences) {
    #             CurrentActionSequences.Remove(sequence);
    #             OnAgentActionSequenceCompleted(this);
    #         }
    #     }
    #     else IsBusy = false;
    # }
    def _execute(self) -> None:
        """
        Executes the current action sequences.
        """
        if len(self.CurrentActionSequences) > 0:
            cullable_sequences = []
            for sequence in self.CurrentActionSequences:
                if len(sequence) > 0:
                    action_to_execute = sequence[0]
                    execution_status = action_to_execute.execute(self) # Pass self (agent) to action's execute method
                    if execution_status != ExecutionStatus.Executing:
                        sequence.pop(0) # Remove the action if it's done (succeeded, failed, not possible)
                else:
                    cullable_sequences.append(sequence) # Mark sequence as empty for removal

            for sequence in cullable_sequences:
                self.CurrentActionSequences.remove(sequence)
                Agent.OnAgentActionSequenceCompleted(self) # Trigger event for completed sequence

            # If after execution, all sequences are empty, agent is no longer busy.
            # Otherwise, it might still be busy.
            self.IsBusy = any(len(seq) > 0 for seq in self.CurrentActionSequences)
        else:
            self.IsBusy = False # No current action sequences, so not busy

```

---

**MountainGoap/Sensor.py**

```python
# // <copyright file="Sensor.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Optional, List
from .CallbackDelegates.SensorRunCallback import SensorRunCallback
from .Events.SensorRunningEvent import SensorRunEvent # Changed name from SensorRunningEvent.cs to match usage

# /// <summary>
# /// Sensor for getting information about world state.
# /// </summary>
class Sensor:
    """
    Sensor for getting information about world state.
    """

    # /// <summary>
    # /// Name of the sensor.
    # /// </summary>
    # public readonly string Name;
    Name: str

    # /// <summary>
    # /// Callback to be executed when the sensor runs.
    # /// </summary>
    # private readonly SensorRunCallback runCallback;
    _run_callback: SensorRunCallback

    # Events (static in C#)
    _on_sensor_run_handlers: List[SensorRunEvent] = []

    @classmethod
    def OnSensorRun(cls, agent: 'Agent', sensor: 'Sensor'):
        for handler in cls._on_sensor_run_handlers:
            handler(agent, sensor)

    @classmethod
    def register_on_sensor_run(cls, handler: SensorRunEvent):
        cls._on_sensor_run_handlers.append(handler)


    # /// <summary>
    # /// Initializes a new instance of the <see cref="Sensor"/> class.
    # /// </summary>
    # public Sensor(SensorRunCallback runCallback, string? name = null) {
    #     Name = name ?? $"Sensor {Guid.NewGuid()} ({runCallback.GetMethodInfo().Name})";
    #     this.runCallback = runCallback;
    # }
    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
        """
        Initializes a new instance of the Sensor class.
        """
        # In C#, GetMethodInfo().Name is used for default name.
        # In Python, we can get the function's __name__ attribute.
        callback_name = run_callback.__name__ if hasattr(run_callback, '__name__') else str(run_callback)
        self.Name = name if name is not None else f"Sensor {uuid.uuid4()} ({callback_name})"
        self._run_callback = run_callback

    # /// <summary>
    # /// Runs the sensor during a game loop.
    # /// </summary>
    # public void Run(Agent agent) {
    #     OnSensorRun(agent, this);
    #     runCallback(agent);
    # }
    def run(self, agent: 'Agent') -> None:
        """
        Runs the sensor during a game loop.
        """
        from .Agent import Agent # Local import to avoid circular dependency

        Sensor.OnSensorRun(agent, self) # Call the classmethod event
        self._run_callback(agent)

```

---

**MountainGoap/PermutationSelectorGenerators.py**

```python
# // <copyright file="PermutationSelectorGenerators.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable S3267 // Loops should be simplified with "LINQ" expressions

from typing import Iterable, List, Any, TypeVar, Callable, Dict, Optional
from .CallbackDelegates.PermutationSelectorCallback import PermutationSelectorCallback

T = TypeVar('T')

# A type alias for the state dictionary (from CallbackDelegates.py)
StateDictionary = Dict[str, Optional[Any]]


# /// <summary>
# /// Generators for default permutation selectors for convenience.
# /// </summary>
class PermutationSelectorGenerators:
    """
    Generators for default permutation selectors for convenience.
    """

    # /// <summary>
    # /// Generates a permutation selector that returns all elements of an enumerable.
    # /// </summary>
    # public static PermutationSelectorCallback SelectFromCollection<T>(IEnumerable<T> values) {
    #     return (ConcurrentDictionary<string, object?> state) => {
    #         List<object> output = new();
    #         foreach (var item in values) if (item is not null) output.Add(item);
    #         return output;
    #     };
    # }
    @staticmethod
    def select_from_collection(values: Iterable[T]) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all elements of an enumerable.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for item in values:
                if item is not None:
                    output.append(item)
            return output
        return selector

    # /// <summary>
    # /// Generates a permutation selector that returns all elements of an enumerable within the agent state.
    # /// </summary>
    # public static PermutationSelectorCallback SelectFromCollectionInState<T>(string key) {
    #     return (ConcurrentDictionary<string, object?> state) => {
    #         List<object> output = new();
    #         if (state[key] is not IEnumerable<T> values) return output;
    #         foreach (var item in values) if (item is not null) output.Add(item);
    #         return output;
    #     };
    # }
    @staticmethod
    def select_from_collection_in_state(key: str) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all elements of an enumerable within the agent state.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            if key in state and isinstance(state[key], Iterable):
                values = state[key]
                for item in values:
                    if item is not None:
                        output.append(item)
            return output
        return selector

    # /// <summary>
    # /// Generates a permutation selector that returns all integer elements in a range.
    # /// </summary>
    # public static PermutationSelectorCallback SelectFromIntegerRange(int lowerBound, int upperBound) {
    #     return (ConcurrentDictionary<string, object?> state) => {
    #         List<object> output = new();
    #         for (int i = lowerBound; i < upperBound; i++) output.Add(i);
    #         return output;
    #     };
    # }
    @staticmethod
    def select_from_integer_range(lower_bound: int, upper_bound: int) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all integer elements in a range.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for i in range(lower_bound, upper_bound):
                output.append(i)
            return output
        return selector

```

---

**MountainGoap/Internals/ActionGraph.py**

```python
# // <copyright file="ActionGraph.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import List, Any, Optional, Dict, Iterable, TYPE_CHECKING
from .DictionaryExtensionMethods import DictionaryExtensionMethods
from .ActionNode import ActionNode

if TYPE_CHECKING:
    from ..Action import Action

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

# /// <summary>
# /// Represents a traversable action graph.
# /// </summary>
class ActionGraph:
    """
    Represents a traversable action graph.
    """

    # /// <summary>
    # /// The set of actions for the graph.
    # /// </summary>
    # internal List<ActionNode> ActionNodes = new();
    ActionNodes: List[ActionNode]

    # /// <summary>
    # /// Initializes a new instance of the <see cref="ActionGraph"/> class.
    # /// </summary>
    # internal ActionGraph(List<Action> actions, ConcurrentDictionary<string, object?> state) {
    #     foreach (var action in actions) {
    #         var permutations = action.GetPermutations(state);
    #         foreach (var permutation in permutations) ActionNodes.Add(new(action, state, permutation));
    #     }
    # }
    def __init__(self, actions: List['Action'], state: StateDictionary):
        """
        Initializes a new instance of the ActionGraph class.
        """
        self.ActionNodes = []
        for action in actions:
            permutations = action.get_permutations(state)
            # If no permutations are returned (e.g., empty selector lists),
            # the action with that permutation context isn't added.
            # If permutations are always expected to return at least one empty dict if no params,
            # then this logic is fine.
            # In C#, `GetPermutations` returns an empty list if any selector yields no values,
            # so the outer loop over `permutations` will skip.
            for permutation in permutations:
                # Create a new ActionNode for each action-permutation combination.
                # Important: Pass a *copy* of the action and initial state to the node.
                # The ActionNode constructor already handles copying the action.
                self.ActionNodes.append(ActionNode(action, state, permutation))

    # /// <summary>
    # /// Gets the list of neighbors for a node.
    # /// </summary>
    # internal IEnumerable<ActionNode> Neighbors(ActionNode node) {
    #     foreach (var otherNode in ActionNodes) {
    #         if (otherNode.Action is not null && otherNode.Action.IsPossible(node.State)) {
    #             var newNode = new ActionNode(otherNode.Action.Copy(), node.State.Copy(), otherNode.Parameters.Copy());
    #             newNode.Action?.ApplyEffects(newNode.State);
    #             yield return newNode;
    #         }
    #     }
    # }
    def neighbors(self, node: ActionNode) -> Iterable[ActionNode]:
        """
        Gets the list of neighbors for a node.
        """
        for other_node_template in self.ActionNodes:
            # `other_node_template` here refers to the initial ActionNodes created based on the agent's initial state.
            # When we generate neighbors, we are essentially looking for actions that can be applied
            # given the `node.State` (which is the state *after* the current node's action is applied).

            if other_node_template.Action is not None and \
               other_node_template.Action.is_possible(node.State): # Check possibility against the current node's resulting state
                
                # Create a new ActionNode representing the *next* state after applying `other_node_template.Action`
                # Its action is a copy of the other_node_template's action
                # Its initial state is a copy of the *current* node's state
                # Its parameters are a copy of the other_node_template's parameters (which were determined for the base state or for general use)
                new_action = other_node_template.Action.copy()
                new_state = DictionaryExtensionMethods.copy_concurrent_dict(node.State)
                new_parameters = DictionaryExtensionMethods.copy_dict(other_node_template.Parameters)

                new_node = ActionNode(new_action, new_state, new_parameters)
                
                # Apply the effects of the new action to the new node's state
                if new_node.Action is not None:
                    new_node.Action.apply_effects(new_node.State)

                yield new_node

```

---

**MountainGoap/Internals/ActionAStar.py**

```python
# // <copyright file="ActionAStar.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List, cast
from math import inf
from datetime import datetime, timedelta

from ..PriorityQueue.FastPriorityQueue import FastPriorityQueue
from ..PriorityQueue.FastPriorityQueueNode import FastPriorityQueueNode # To derive ActionNode from this.
from .ActionNode import ActionNode
from .ActionGraph import ActionGraph
from ..BaseGoal import BaseGoal
from ..Goal import Goal
from ..ExtremeGoal import ExtremeGoal
from ..ComparativeGoal import ComparativeGoal
from ..ComparisonOperator import ComparisonOperator
from .Utils import Utils

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

# /// <summary>
# /// AStar calculator for an action graph.
# /// </summary>
class ActionAStar:
    """
    AStar calculator for an action graph.
    """

    # /// <summary>
    # /// Final point at which the calculation arrived.
    # /// </summary>
    # internal readonly ActionNode? FinalPoint = null;
    FinalPoint: Optional[ActionNode] = None

    # /// <summary>
    # /// Cost so far to get to each node.
    # /// </summary>
    # internal readonly ConcurrentDictionary<ActionNode, float> CostSoFar = new();
    CostSoFar: Dict[ActionNode, float] = {} # Using standard dict for simplicity in Python

    # /// <summary>
    # /// Steps so far to get to each node.
    # /// </summary>
    # internal readonly ConcurrentDictionary<ActionNode, int> StepsSoFar = new();
    StepsSoFar: Dict[ActionNode, int] = {} # Using standard dict for simplicity in Python

    # /// <summary>
    # /// Dictionary giving the path from start to goal.
    # /// </summary>
    # internal readonly ConcurrentDictionary<ActionNode, ActionNode> CameFrom = new();
    CameFrom: Dict[ActionNode, ActionNode] = {} # Using standard dict for simplicity in Python

    # /// <summary>
    # /// Goal state that AStar is trying to achieve.
    # /// </summary>
    # private readonly BaseGoal goal;
    _goal: BaseGoal

    # /// <summary>
    # /// Initializes a new instance of the <see cref="ActionAStar"/> class.
    # /// </summary>
    # internal ActionAStar(ActionGraph graph, ActionNode start, BaseGoal goal, float costMaximum, int stepMaximum) {
    #     this.goal = goal;
    #     FastPriorityQueue<ActionNode> frontier = new(100000);
    #     frontier.Enqueue(start, 0);
    #     CameFrom[start] = start;
    #     CostSoFar[start] = 0;
    #     StepsSoFar[start] = 0;
    #     while (frontier.Count > 0) {
    #         var current = frontier.Dequeue();
    #         if (MeetsGoal(current, start)) {
    #             FinalPoint = current;
    #             break;
    #         }
    #         foreach (var next in graph.Neighbors(current)) {
    #             float newCost = CostSoFar[current] + next.Cost(current.State);
    #             int newStepCount = StepsSoFar[current] + 1;
    #             if (newCost > costMaximum || newStepCount > stepMaximum) continue;
    #             if (!CostSoFar.ContainsKey(next) || newCost < CostSoFar[next]) {
    #                 CostSoFar[next] = newCost;
    #                 StepsSoFar[next] = newStepCount;
    #                 float priority = newCost + Heuristic(next, goal, current);
    #                 frontier.Enqueue(next, priority);
    #                 CameFrom[next] = current;
    #                 Agent.TriggerOnEvaluatedActionNode(next, CameFrom);
    #             }
    #         }
    #     }
    # }
    def __init__(self, graph: ActionGraph, start: ActionNode, goal: BaseGoal, cost_maximum: float, step_maximum: int):
        """
        Initializes a new instance of the ActionAStar class.
        """
        from ..Agent import Agent # Local import to avoid circular dependency

        self._goal = goal
        # The C# FastPriorityQueue expects nodes to inherit from FastPriorityQueueNode.
        # ActionNode already does, so this is consistent.
        frontier = FastPriorityQueue[ActionNode](100000) # Max nodes for queue
        frontier.enqueue(start, 0.0)

        self.CameFrom[start] = start # A* uses start to point to itself to signify the beginning
        self.CostSoFar[start] = 0.0
        self.StepsSoFar[start] = 0

        while frontier.count > 0:
            current = frontier.dequeue()

            if self._meets_goal(current, start): # Note: C# original passes 'start' as 'current' to MeetsGoal, which is the prior state.
                                                  # This is a bit confusing but implies current is the state *before* `current.Action` is applied.
                                                  # Let's adjust `_meets_goal` to take `previous_node` appropriately.
                                                  # For the start node, `current` is the `previous_node` for its subsequent actions.
                                                  # The goal condition should be checked on `current.State` (state *after* current action is done).
                self.FinalPoint = current
                break
            
            for next_node in graph.neighbors(current): # graph.neighbors generates nodes where the action's effects are *already applied*
                # The cost of 'next_node' is the cost of its action given the state *before* that action (which is `current.State`)
                action_cost = next_node.cost(current.State) # Cost of the action in `next_node` when taken from `current.State`
                new_cost = self.CostSoFar[current] + action_cost
                new_step_count = self.StepsSoFar[current] + 1

                if new_cost > cost_maximum or new_step_count > step_maximum:
                    continue

                # If `next_node` is not in `CostSoFar` OR a cheaper path to `next_node` is found
                if next_node not in self.CostSoFar or new_cost < self.CostSoFar[next_node]:
                    self.CostSoFar[next_node] = new_cost
                    self.StepsSoFar[next_node] = new_step_count
                    
                    # Heuristic needs to estimate cost from `next_node.State` to goal.
                    # The `current` argument to Heuristic in C# appears to be the *previous* node in the path (e.g., `current` here).
                    # So, `Heuristic(next, goal, current)` means heuristic from `next.State` towards goal, influenced by `current.State` as the immediate prior state.
                    priority = new_cost + self._heuristic(next_node, goal, current)
                    
                    # If next_node is already in frontier but with higher priority, UpdatePriority is called.
                    if frontier.contains(next_node):
                        frontier.update_priority(next_node, priority)
                    else:
                        frontier.enqueue(next_node, priority)
                    
                    self.CameFrom[next_node] = current
                    Agent.OnEvaluatedActionNode(next_node, self.CameFrom) # Trigger static event

    # private static float Heuristic(ActionNode actionNode, BaseGoal goal, ActionNode current) {
    #     var cost = 0f;
    #     if (goal is Goal normalGoal) {
    #         normalGoal.DesiredState.Select(kvp => kvp.Key).ToList().ForEach(key => {
    #             if (!actionNode.State.ContainsKey(key)) cost++;
    #             else if (actionNode.State[key] == null && actionNode.State[key] != normalGoal.DesiredState[key]) cost++;
    #             else if (actionNode.State[key] is object obj && !obj.Equals(normalGoal.DesiredState[key])) cost++;
    #         });
    #     }
    #     else if (goal is ExtremeGoal extremeGoal) {
    #         foreach (var kvp in extremeGoal.DesiredState) {
    #             var valueDiff = 0f;
    #             var valueDiffMultiplier = (actionNode?.Action?.StateCostDeltaMultiplier ?? Action.DefaultStateCostDeltaMultiplier).Invoke(actionNode?.Action, kvp.Key);
    #             if (actionNode.State.ContainsKey(kvp.Key) && actionNode.State[kvp.Key] == null) {
    #                 cost += float.PositiveInfinity;
    #                 continue;
    #             }
    #             if (actionNode.State.ContainsKey(kvp.Key) && extremeGoal.DesiredState.ContainsKey(kvp.Key)) valueDiff = Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]);
    #             if (!actionNode.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
    #             else if (!current.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
    #             else if (!kvp.Value && actionNode.State[kvp.Key] is object a && current.State[kvp.Key] is object b && IsLowerThanOrEquals(a, b)) cost += valueDiff * valueDiffMultiplier;
    #             else if (kvp.Value && actionNode.State[kvp.Key] is object a2 && current.State[kvp.Key] is object b2 && IsHigherThanOrEquals(a2, b2)) cost -= valueDiff * valueDiffMultiplier;
    #         }
    #     }
    #     else if (goal is ComparativeGoal comparativeGoal) {
    #         foreach (var kvp in comparativeGoal.DesiredState) {
    #             var valueDiff2 = 0f;
    #             var valueDiffMultiplier = (actionNode?.Action?.StateCostDeltaMultiplier ?? Action.DefaultStateCostDeltaMultiplier).Invoke(actionNode?.Action, kvp.Key);
    #             if (actionNode.State.ContainsKey(kvp.Key) && comparativeGoal.DesiredState.ContainsKey(kvp.Key)) valueDiff2 = Math.Abs(Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]));
    #             if (!actionNode.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
    #             else if (!current.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
    #             else if (kvp.Value.Operator == ComparisonOperator.Undefined) cost += float.PositiveInfinity;
    #             else if (kvp.Value.Operator == ComparisonOperator.Equals && actionNode.State[kvp.Key] is object obj && !obj.Equals(comparativeGoal.DesiredState[kvp.Key].Value)) cost += valueDiff2 * valueDiffMultiplier;
    #             else if (kvp.Value.Operator == ComparisonOperator.LessThan && actionNode.State[kvp.Key] is object a && comparativeGoal.DesiredState[kvp.Key].Value is object b && !IsLowerThan(a, b)) cost += valueDiff2 * valueDiffMultiplier;
    #             else if (kvp.Value.Operator == ComparisonOperator.GreaterThan && actionNode.State[kvp.Key] is object a2 && comparativeGoal.DesiredState[kvp.Key].Value is object b2 && !IsHigherThan(a2, b2)) cost += valueDiff2 * valueDiffMultiplier;
    #             else if (kvp.Value.Operator == ComparisonOperator.LessThanOrEquals && actionNode.State[kvp.Key] is object a3 && comparativeGoal.DesiredState[kvp.Key].Value is object b3 && !IsLowerThanOrEquals(a3, b3)) cost += valueDiff2 * valueDiffMultiplier;
    #             else if (kvp.Value.Operator == ComparisonOperator.GreaterThanOrEquals && actionNode.State[kvp.Key] is object a4 && comparativeGoal.DesiredState[kvp.Key].Value is object b4 && !IsHigherThanOrEquals(a4, b4)) cost += valueDiff2 * valueDiffMultiplier;
    #         }
    #     }
    #     return cost;
    # }
    def _heuristic(self, action_node: ActionNode, goal: BaseGoal, previous_node_in_path: ActionNode) -> float:
        """
        Calculates the heuristic cost from actionNode.State to the goal.
        """
        from ..Action import Action # Local import

        cost = 0.0
        
        if isinstance(goal, Goal):
            # For a normal goal, count how many desired state keys are NOT met
            # This is a simple count-mismatch heuristic.
            for key, desired_value in goal.DesiredState.items():
                if key not in action_node.State or action_node.State[key] != desired_value:
                    cost += 1.0 # Each unmet condition adds 1 to heuristic cost
        elif isinstance(goal, ExtremeGoal):
            # For extreme goals, heuristic encourages movement towards the extreme.
            # Reward: subtract cost if moving in desired direction.
            # Penalty: add cost if moving in undesired direction or not moving enough.
            for key, maximize in goal.DesiredState.items():
                value_diff_multiplier = (action_node.Action.StateCostDeltaMultiplier if action_node.Action else Action.default_state_cost_delta_multiplier)(action_node.Action, key)
                
                if key not in action_node.State or key not in previous_node_in_path.State:
                    cost += inf # Cannot determine progress without both states
                    continue

                current_val = action_node.State[key]
                prev_val = previous_node_in_path.State[key]
                
                if current_val is None or prev_val is None:
                    # If any value is None, it's hard to compare numerically, consider it a high cost.
                    cost += inf
                    continue
                
                # Convert to float for numeric comparison, similar to C# Convert.ToSingle
                try:
                    current_val_f = float(current_val)
                    prev_val_f = float(prev_val)
                except (ValueError, TypeError):
                    cost += inf # Not a comparable numeric type
                    continue
                
                value_diff = current_val_f - prev_val_f

                if maximize:
                    if Utils.is_lower_than_or_equals(current_val, prev_val):
                        # Not improving or getting worse, penalize.
                        # C# `cost -= valueDiff * valueDiffMultiplier;` for maximize when is_higher_than_or_equals
                        # This seems to be `current_val >= prev_val` then cost -= (current-prev)*mult,
                        # which means if current > prev, (current-prev) is positive, so cost reduces.
                        # If current == prev, (current-prev) is 0, no change.
                        # If current < prev, (current-prev) is negative, so cost increases.
                        # This means it's a "reward" for moving in the right direction.
                        # For a heuristic, we want to estimate *remaining* cost.
                        # If we're not moving positively (or maximizing), the "remaining" cost is higher.
                        # So, if not moving toward max, we add penalty proportional to how much we didn't move.
                        # The C# heuristic here is actually a negative "reward" which reduces the priority.
                        # To reflect this, if we're maximizing and the value increased, we subtract, meaning it's "closer".
                        # If we're maximizing and the value decreased, we add, meaning it's "further".
                        cost -= value_diff * value_diff_multiplier # Encourage increase
                    else: # current_val < prev_val
                        # Moving away from the goal, this path is worse.
                        cost += abs(value_diff) * value_diff_multiplier # Penalize decrease
                else: # minimize
                    if Utils.is_higher_than_or_equals(current_val, prev_val):
                        # Not improving or getting worse, penalize.
                        # C# `cost += valueDiff * valueDiffMultiplier;` for minimize when is_lower_than_or_equals
                        # This means if current < prev, (current-prev) is negative, cost reduces.
                        # If current == prev, (current-prev) is 0, no change.
                        # If current > prev, (current-prev) is positive, cost increases.
                        cost += value_diff * value_diff_multiplier # Encourage decrease
                    else: # current_val > prev_val
                        # Moving away from the goal, this path is worse.
                        cost += abs(value_diff) * value_diff_multiplier # Penalize increase


        elif isinstance(goal, ComparativeGoal):
            # For comparative goals, heuristic encourages movement towards meeting the comparison.
            # Penalize by how far away it is or if moving in wrong direction.
            for key, comp_value_pair in goal.DesiredState.items():
                value_diff_multiplier = (action_node.Action.StateCostDeltaMultiplier if action_node.Action else Action.default_state_cost_delta_multiplier)(action_node.Action, key)

                if key not in action_node.State or key not in previous_node_in_path.State:
                    cost += inf
                    continue

                current_val = action_node.State[key]
                desired_val = comp_value_pair.Value
                operator = comp_value_pair.Operator

                if current_val is None or desired_val is None:
                    if operator != ComparisonOperator.Undefined:
                        cost += inf # Cannot compare if values are None
                        continue

                # Ensure values are comparable for arithmetic difference
                try:
                    current_val_f = float(current_val)
                    desired_val_f = float(desired_val) if desired_val is not None else float('nan') # Handle None case for desired_val
                except (ValueError, TypeError):
                    current_val_f = float('nan') # Mark as non-numeric if conversion fails

                # This valueDiff2 in C# is Math.Abs(Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]))
                # It's the absolute change from previous state. This seems more like a penalty for *change* rather than *distance to goal*.
                # Let's re-interpret this as a "cost" of not meeting the goal from the new state.
                # If the goal is NOT met, then add a penalty.
                # The valueDiff2 calculation in C# seems to be about the magnitude of change *between* states, not distance to goal.
                # Replicating this strictly for verbatim.
                value_diff_from_previous_step = 0.0
                if current_val is not None and previous_node_in_path.State.get(key) is not None:
                    try:
                        value_diff_from_previous_step = abs(float(current_val) - float(previous_node_in_path.State[key]))
                    except (ValueError, TypeError):
                        pass # Cannot calculate numeric diff, leave as 0 or handle as error

                # If the comparison isn't met, add a cost.
                # The C# heuristic adds `valueDiff2 * valueDiffMultiplier` when the goal is NOT met.
                # This suggests the heuristic is a measure of "how much work is still needed, or how badly this step moved away".
                # For `Equals`, if not equal, it penalizes.
                if operator == ComparisonOperator.Undefined:
                    cost += inf
                elif operator == ComparisonOperator.Equals:
                    if current_val != desired_val:
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.LessThan:
                    if not Utils.is_lower_than(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.GreaterThan:
                    if not Utils.is_higher_than(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if not Utils.is_lower_than_or_equals(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if not Utils.is_higher_than_or_equals(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
        return cost

    # Private helper methods from Utils in C# are directly called by Utils.method_name
    # private static bool IsLowerThan(object a, object b) { ... } -> Utils.is_lower_than(a,b)
    # private static bool IsHigherThan(object a, object b) { ... } -> Utils.is_higher_than(a,b)
    # private static bool IsLowerThanOrEquals(object a, object b) { ... } -> Utils.is_lower_than_or_equals(a,b)
    # private static bool IsHigherThanOrEquals(object a, object b) { ... } -> Utils.is_higher_than_or_equals(a,b)
    # private bool MeetsGoal(ActionNode actionNode, ActionNode current) { ... } -> self._meets_goal(action_node, current)
    def _meets_goal(self, action_node: ActionNode, previous_node_in_path: ActionNode) -> bool:
        """
        Indicates whether or not a goal is met by an action node.
        This is the terminal condition for A*.
        """
        return Utils.meets_goal(self._goal, action_node, previous_node_in_path)

```

---

**MountainGoap/Internals/Planner.py**

```python
# // <copyright file="Planner.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import List, Optional, Dict
from .ActionAStar import ActionAStar
from .ActionGraph import ActionGraph
from .ActionNode import ActionNode
from ..Agent import Agent # Circular import, handled by local import/type checking
from ..Action import Action
from ..BaseGoal import BaseGoal

# /// <summary>
# /// Planner for an agent.
# /// </summary>
class Planner:
    """
    Planner for an agent.
    """

    # /// <summary>
    # /// Makes a plan to achieve the agent's goals.
    # /// </summary>
    # internal static void Plan(Agent agent, float costMaximum, int stepMaximum) {
    #     Agent.TriggerOnPlanningStarted(agent);
    #     float bestPlanUtility = 0;
    #     ActionAStar? astar;
    #     ActionNode? cursor;
    #     ActionAStar? bestAstar = null;
    #     BaseGoal? bestGoal = null;
    #     foreach (var goal in agent.Goals) {
    #         Agent.TriggerOnPlanningStartedForSingleGoal(agent, goal);
    #         ActionGraph graph = new(agent.Actions, agent.State);
    #         ActionNode start = new(null, agent.State, new());
    #         astar = new(graph, start, goal, costMaximum, stepMaximum);
    #         cursor = astar.FinalPoint;
    #         if (cursor is not null && astar.CostSoFar[cursor] == 0) Agent.TriggerOnPlanningFinishedForSingleGoal(agent, goal, 0);
    #         else if (cursor is not null) Agent.TriggerOnPlanningFinishedForSingleGoal(agent, goal, goal.Weight / astar.CostSoFar[cursor]);
    #         if (cursor is not null && cursor.Action is not null && astar.CostSoFar.ContainsKey(cursor) && goal.Weight / astar.CostSoFar[cursor] > bestPlanUtility) {
    #             bestPlanUtility = goal.Weight / astar.CostSoFar[cursor];
    #             bestAstar = astar;
    #             bestGoal = goal;
    #         }
    #     }
    #     if (bestPlanUtility > 0 && bestAstar is not null && bestGoal is not null && bestAstar.FinalPoint is not null) {
    #         UpdateAgentActionList(bestAstar.FinalPoint, bestAstar, agent);
    #         agent.IsBusy = true;
    #         Agent.TriggerOnPlanningFinished(agent, bestGoal, bestPlanUtility);
    #     }
    #     else Agent.TriggerOnPlanningFinished(agent, null, 0);
    #     agent.IsPlanning = false;
    # }
    @staticmethod
    def plan(agent: 'Agent', cost_maximum: float, step_maximum: int) -> None:
        """
        Makes a plan to achieve the agent's goals.
        """
        # Ensure agent is imported to access its static event methods
        # from ..Agent import Agent # Already imported at module level for type hints.

        Agent.OnPlanningStarted(agent) # Trigger static event

        best_plan_utility = 0.0
        best_astar: Optional[ActionAStar] = None
        best_goal: Optional[BaseGoal] = None

        for goal in agent.Goals:
            Agent.OnPlanningStartedForSingleGoal(agent, goal) # Trigger static event

            # Create an ActionGraph based on the current agent's state and available actions
            graph = ActionGraph(agent.Actions, agent.State)
            
            # The A* start node represents the initial state with no action yet taken.
            # Its action is None, but its state is the agent's current state.
            start_node = ActionNode(None, agent.State, {})
            
            astar_result = ActionAStar(graph, start_node, goal, cost_maximum, step_maximum)
            
            cursor = astar_result.FinalPoint

            current_goal_utility = 0.0
            if cursor is not None:
                # Calculate utility for this goal's plan
                # Utility = GoalWeight / PlanCost (if cost is not zero)
                plan_cost = astar_result.CostSoFar.get(cursor, 0.0) # Get cost to final point
                if plan_cost == 0.0 and cursor != start_node: # If cost is 0 but it's not the start node (meaning a path exists with 0 cost actions)
                    current_goal_utility = float('inf') # Effectively infinite utility for a free plan
                elif plan_cost > 0.0:
                    current_goal_utility = goal.Weight / plan_cost
                # If plan_cost is 0 and it's just the start_node, it implies goal is already met with 0 cost, so utility should be high.
                # If plan_cost is 0 but path exists (cursor is not start_node), also effectively infinite utility.
                # If plan_cost is 0 and cursor is start_node, meaning goal already met.
                
                # C# logic: if cost is 0, utility is 0. This seems like a simplification.
                # let's follow C# verbatim
                if cursor is not None and plan_cost == 0:
                    current_goal_utility = 0.0 # Strict verbatim for this line
                elif cursor is not None:
                    current_goal_utility = goal.Weight / plan_cost

                # Trigger event for finishing planning for single goal
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, current_goal_utility)

                # Update best plan if current one has higher utility
                if current_goal_utility > best_plan_utility:
                    best_plan_utility = current_goal_utility
                    best_astar = astar_result
                    best_goal = goal
            else:
                # If cursor is None, no path was found for this goal.
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, 0.0) # Utility 0 for no path

        # After checking all goals, finalize the best plan
        if best_plan_utility > 0 and best_astar is not None and best_goal is not None and best_astar.FinalPoint is not None:
            Planner._update_agent_action_list(best_astar.FinalPoint, best_astar, agent)
            agent.IsBusy = True
            Agent.OnPlanningFinished(agent, best_goal, best_plan_utility)
        else:
            Agent.OnPlanningFinished(agent, None, 0.0) # No valid plan found

        agent.IsPlanning = False # Planning is complete

    # /// <summary>
    # /// Updates the agent action list with the new plan. Only supports executing one sequence of events at a time for now.
    # /// </summary>
    # private static void UpdateAgentActionList(ActionNode start, ActionAStar astar, Agent agent) {
    #     ActionNode? cursor = start;
    #     List<Action> actionList = new();
    #     while (cursor != null && cursor.Action != null && astar.CameFrom.ContainsKey(cursor)) {
    #         actionList.Add(cursor.Action);
    #         cursor = astar.CameFrom[cursor];
    #     }
    #     actionList.Reverse();
    #     agent.CurrentActionSequences.Add(actionList);
    #     Agent.TriggerOnPlanUpdated(agent, actionList);
    # }
    @staticmethod
    def _update_agent_action_list(start_node: ActionNode, astar: ActionAStar, agent: 'Agent') -> None:
        """
        Updates the agent action list with the new plan.
        """
        # from ..Agent import Agent # Already imported at module level for type hints.

        cursor: Optional[ActionNode] = start_node
        action_list: List[Action] = []

        # Reconstruct path by traversing CameFrom dictionary backwards from FinalPoint
        # Stop when cursor is the initial 'start' node (which has a None action)
        while cursor is not None and cursor != astar.CameFrom[cursor]: # astar.CameFrom[start_node] == start_node
            if cursor.Action is not None:
                action_list.append(cursor.Action)
            cursor = astar.CameFrom.get(cursor)
            # If a cycle is detected or path breaks before start_node,
            # this loop might become infinite or stop prematurely.
            # astar.CameFrom guarantees a path back to 'start_node' if 'FinalPoint' is reachable.
            
        action_list.reverse() # Reverse to get actions in chronological order

        agent.CurrentActionSequences.clear() # Clear any existing plans
        agent.CurrentActionSequences.append(action_list)
        Agent.OnPlanUpdated(agent, action_list) # Trigger static event

```

---

**MountainGoapLogging/DefaultLogger.py**

```python
# // <copyright file="DefaultLogger.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List
import logging
import sys

# Assume MountainGoap is installed or accessible via PYTHONPATH
# from MountainGoap import Agent, Action, Sensor, ExecutionStatus, BaseGoal
# from MountainGoap.Internals.ActionNode import ActionNode
# For this structure, we'll use relative imports assuming the project root is the base.
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Internals.ActionNode import ActionNode

# Instead of Serilog, we'll use Python's built-in `logging` module.
# Serilog's structured logging features can be mimicked using f-strings or extra dict in Python's logging.
class DefaultLogger:
    def __init__(self, log_to_console: bool = True, logging_file: Optional[str] = None):
        # Configure basic logging. In a real application, you might want more sophisticated setup.
        # Python's logging.Logger is not directly analogous to Serilog.Core.Logger
        # Serilog.Core.Logger configures sinks, while Python's Logger manages handlers.
        self.logger = logging.getLogger("MountainGoapLogger")
        self.logger.setLevel(logging.INFO)
        # Prevent adding handlers multiple times if instantiated repeatedly
        if not self.logger.handlers:
            if log_to_console:
                console_handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter('%(levelname)s: %(message)s')
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            if logging_file is not None:
                file_handler = logging.FileHandler(logging_file)
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        
        # Register Python methods to C# static events
        Agent.register_on_agent_action_sequence_completed(self._on_agent_action_sequence_completed)
        Agent.register_on_agent_step(self._on_agent_step)
        Agent.register_on_planning_started(self._on_planning_started)
        Agent.register_on_planning_started_for_single_goal(self._on_planning_started_for_single_goal)
        Agent.register_on_planning_finished(self._on_planning_finished)
        Agent.register_on_planning_finished_for_single_goal(self._on_planning_finished_for_single_goal)
        Agent.register_on_plan_updated(self._on_plan_updated)
        Agent.register_on_evaluated_action_node(self._on_evaluated_action_node)
        
        Action.register_on_begin_execute_action(self._on_begin_execute_action)
        Action.register_on_finish_execute_action(self._on_finish_execute_action)
        
        Sensor.register_on_sensor_run(self._on_sensor_run)


    def _on_evaluated_action_node(self, node: ActionNode, nodes: Dict[ActionNode, ActionNode]) -> None:
        came_from_list: List[ActionNode] = []
        traceback_node: Optional[ActionNode] = node
        
        # Reconstruct path. The C# logic `traceback.Action != nodes[traceback].Action` is tricky.
        # In astar.CameFrom, `CameFrom[start] = start`.
        # So we trace back until we hit the start node (where its predecessor is itself).
        # Or until the action is None (for the conceptual start node).
        while traceback_node is not None and traceback_node in nodes and traceback_node != nodes[traceback_node]:
            came_from_list.append(traceback_node)
            traceback_node = nodes[traceback_node]
        
        # Add the start node itself if it was the origin of the path
        if traceback_node is not None and traceback_node not in came_from_list:
            came_from_list.append(traceback_node)

        came_from_list.reverse() # Order from start to current node
        
        # C# logs count - 1, likely excluding the 'start' node or the evaluated node itself.
        # If came_from_list includes start and end, path length is len - 1.
        # If 'node' itself is counted as the end, and we're looking at steps leading *to* it.
        # The start node itself has 0 steps leading to it.
        # Example: start -> A -> B. Evaluating B. Path [start, A, B]. Count is 3. Path steps: 2.
        num_steps_leading_to_it = len(came_from_list) - 1
        
        self.logger.info(f"Evaluating node {node.Action.Name if node.Action else 'No Action'} with {num_steps_leading_to_it} nodes leading to it.")


    def _on_plan_updated(self, agent: Agent, action_list: List[Action]) -> None:
        self.logger.info(f"Agent {agent.Name} has a new plan:")
        for i, action in enumerate(action_list):
            self.logger.info(f"\tStep #{i+1}: {action.Name}")

    def _on_agent_action_sequence_completed(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} completed action sequence.")

    def _on_agent_step(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} is working.")

    def _on_begin_execute_action(self, agent: Agent, action: Action, parameters: Dict[str, Optional[Any]]) -> None:
        self.logger.info(f"Agent {agent.Name} began executing action {action.Name}.")
        if parameters:
            self.logger.info("\tAction parameters:")
            for key, value in parameters.items():
                self.logger.info(f"\t\t{key}: {value}")

    def _on_finish_execute_action(self, agent: Agent, action: Action, status: ExecutionStatus, parameters: Dict[str, Optional[Any]]) -> None:
        self.logger.info(f"Agent {agent.Name} finished executing action {action.Name} with status {status.name}.")

    def _on_planning_finished(self, agent: Agent, goal: Optional[BaseGoal], utility: float) -> None:
        if goal is None:
            self.logger.warning(f"Agent {agent.Name} finished planning and found no possible goal.")
        else:
            self.logger.info(f"Agent {agent.Name} finished planning with goal {goal.Name}, utility value {utility}.")

    def _on_planning_started_for_single_goal(self, agent: Agent, goal: BaseGoal) -> None:
        self.logger.info(f"Agent {agent.Name} started planning for goal {goal.Name}.")

    def _on_planning_finished_for_single_goal(self, agent: Agent, goal: BaseGoal, utility: float) -> None:
        self.logger.info(f"Agent {agent.Name} finished planning for goal {goal.Name}, utility value {utility}.")

    def _on_planning_started(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} started planning.")

    def _on_sensor_run(self, agent: Agent, sensor: Sensor) -> None:
        self.logger.info(f"Agent {agent.Name} ran sensor {sensor.Name}.")

```

---

**MountainGoapTest/conftest.py**

```python
# conftest.py can be used for global fixtures or imports in pytest.
# This replaces the C# `Usings.cs` which adds global `using` directives.

import pytest
import sys
import os

# Add the project root to sys.path to allow relative imports
# Assuming 'MountainGoap' and 'MountainGoapTest' are siblings
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Global imports for tests, similar to C# Usings.cs
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoap.Sensor import Sensor

# You might want to define fixtures here for common test setup
@pytest.fixture(autouse=True)
def setup_teardown_events():
    """
    Fixture to clear event handlers before and after each test
    to prevent cross-test interference.
    """
    # Before test: Clear all handlers
    Agent._on_agent_step_handlers.clear()
    Agent._on_agent_action_sequence_completed_handlers.clear()
    Agent._on_planning_started_handlers.clear()
    Agent._on_planning_started_for_single_goal_handlers.clear()
    Agent._on_planning_finished_for_single_goal_handlers.clear()
    Agent._on_planning_finished_handlers.clear()
    Agent._on_plan_updated_handlers.clear()
    Agent._on_evaluated_action_node_handlers.clear()
    Action._on_begin_execute_action_handlers.clear()
    Action._on_finish_execute_action_handlers.clear()
    Sensor._on_sensor_run_handlers.clear()

    yield # This runs the test

    # After test: Clear again, just in case (though pytest runs fixtures per test usually)
    Agent._on_agent_step_handlers.clear()
    Agent._on_agent_action_sequence_completed_handlers.clear()
    Agent._on_planning_started_handlers.clear()
    Agent._on_planning_started_for_single_goal_handlers.clear()
    Agent._on_planning_finished_for_single_goal_handlers.clear()
    Agent._on_planning_finished_handlers.clear()
    Agent._on_plan_updated_handlers.clear()
    Agent._on_evaluated_action_node_handlers.clear()
    Action._on_begin_execute_action_handlers.clear()
    Action._on_finish_execute_action_handlers.clear()
    Sensor._on_sensor_run_handlers.clear()

```

---

**MountainGoapTest/ActionContinuationTests.py**

```python
# // <copyright file="ActionContinuationTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode
from typing import Dict, Any

class ActionContinuationTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void ItCanContinueActions() {
    #     var timesExecuted = 0;
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", false },
    #             { "progress", 0 }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", true }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", false }
    #                 },
    #                 postconditions: new() {
    #                     { "key", true }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     timesExecuted++;
    #                     if (agent.State["progress"] is int progress && progress < 3) {
    #                         agent.State["progress"] = progress + 1;
    #                         return ExecutionStatus.Executing;
    #                     }
    #                     else return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     if (agent.State["key"] is bool value) Assert.False(value);
    #     else Assert.False(true);
    #     agent.Step(StepMode.OneAction);
    #     if (agent.State["key"] is bool value2) Assert.False(value2);
    #     else Assert.False(true);
    #     agent.Step(StepMode.OneAction);
    #     if (agent.State["key"] is bool value3) Assert.False(value3);
    #     else Assert.False(true);
    #     agent.Step(StepMode.OneAction);
    #     if (agent.State["key"] is bool value4) Assert.True(value4);
    #     else Assert.False(true);
    #     Assert.Equal(4, timesExecuted);
    # }
    def test_it_can_continue_actions(self):
        times_executed = 0

        def custom_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
            nonlocal times_executed
            times_executed += 1
            if isinstance(agent_instance.State.get("progress"), int) and agent_instance.State["progress"] < 3:
                agent_instance.State["progress"] = agent_instance.State["progress"] + 1
                return ExecutionStatus.Executing
            else:
                return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": False,
                "progress": 0
            },
            goals=[
                Goal(
                    desired_state={
                        "key": True
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": False
                    },
                    postconditions={
                        "key": True # This is applied only when the action SUCCEEDS, not when it's Executing
                    },
                    executor=custom_executor
                )
            ]
        )

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 1
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 2
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 3
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is True # Now it should be True as the action successfully completed
        assert times_executed == 4
        assert not agent.CurrentActionSequences # Plan should be empty now
        assert not agent.IsBusy # Agent should no longer be busy

```

---

**MountainGoapTest/ActionNodeTests.py**

```python
# // <copyright file="ActionNodeTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode
from typing import Dict, Any, Optional

class AgentTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void ItHandlesInitialNullStateValuesCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", null }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "non-null value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", null }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "non-null value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     Assert.NotNull(agent.State["key"]);
    # }
    def test_it_handles_initial_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": None
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "non-null value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": None
                    },
                    postconditions={
                        "key": "non-null value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is not None
        assert agent.State["key"] == "non-null value"

    # [Fact]
    # public void ItHandlesNullGoalsCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "non-null value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", null }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "non-null value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", null }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     Assert.Null(agent.State["key"]);
    # }
    def test_it_handles_null_goals_correctly(self):
        agent = Agent(
            state={
                "key": "non-null value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": None
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "non-null value"
                    },
                    postconditions={
                        "key": None
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is None

    # [Fact]
    # public void ItHandlesNonNullStateValuesCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "new value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "new value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     object? value = agent.State["key"];
    #     Assert.NotNull(value);
    #     if (value is not null) Assert.Equal("new value", (string)value);
    # }
    def test_it_handles_non_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        value = agent.State["key"]
        assert value is not None
        assert value == "new value"

    # [Fact]
    # public void ItExecutesOneActionInOneActionStepMode() {
    #     var actionCount = 0;
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "value" }
    
    
```python
# // <copyright file="ActionNodeTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode
from typing import Dict, Any, Optional

class AgentTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void ItHandlesInitialNullStateValuesCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", null }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "non-null value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", null }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "non-null value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     Assert.NotNull(agent.State["key"]);
    # }
    def test_it_handles_initial_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": None
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "non-null value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": None
                    },
                    postconditions={
                        "key": "non-null value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is not None
        assert agent.State["key"] == "non-null value"

    # [Fact]
    # public void ItHandlesNullGoalsCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "non-null value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", null }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "non-null value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", None }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     Assert.Null(agent.State["key"]);
    # }
    def test_it_handles_null_goals_correctly(self):
        agent = Agent(
            state={
                "key": "non-null value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": None
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "non-null value"
                    },
                    postconditions={
                        "key": None
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is None

    # [Fact]
    # public void ItHandlesNonNullStateValuesCorrectly() {
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "new value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "new value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     object? value = agent.State["key"];
    #     Assert.NotNull(value);
    #     if (value is not null) Assert.Equal("new value", (string)value);
    # }
    def test_it_handles_non_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        value = agent.State["key"]
        assert value is not None
        assert value == "new value"

    # [Fact]
    # public void ItExecutesOneActionInOneActionStepMode() {
    #     var actionCount = 0;
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "new value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "new value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     actionCount++;
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.OneAction);
    #     Assert.Equal(1, actionCount);
    # }
    def test_it_executes_one_action_in_one_action_step_mode(self):
        action_count = 0

        def custom_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=custom_executor
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert action_count == 1
        assert agent.State["key"] == "new value"
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences # Plan should be completed

    # [Fact]
    # public void ItExecutesAllActionsInAllActionsStepMode() {
    #     var actionCount = 0;
    #     var agent = new Agent(
    #         state: new() {
    #             { "key", "value" }
    #         },
    #         goals: new List<BaseGoal> {
    #             new Goal(
    #                 desiredState: new() {
    #                     { "key", "new value" }
    #                 }
    #             )
    #         },
    #         actions: new List<Action> {
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "intermediate value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     actionCount++;
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             ),
    #             new Action(
    #                 preconditions: new() {
    #                     { "key", "intermediate value" }
    #                 },
    #                 postconditions: new() {
    #                     { "key", "new value" }
    #                 },
    #                 executor: (Agent agent, Action action) => {
    #                     actionCount++;
    #                     return ExecutionStatus.Succeeded;
    #                 }
    #             )
    #         }
    #     );
    #     agent.Step(StepMode.AllActions);
    #     Assert.Equal(2, actionCount);
    # }
    def test_it_executes_all_actions_in_all_actions_step_mode(self):
        action_count = 0

        def first_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        def second_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "intermediate value"
                    },
                    executor=first_executor
                ),
                Action(
                    preconditions={
                        "key": "intermediate value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=second_executor
                )
            ]
        )
        agent.step(StepMode.AllActions)
        assert action_count == 2
        assert agent.State["key"] == "new value"
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences # Plan should be completed

```

---

**MountainGoapTest/ArithmeticPostconditionsTests.py**

```python
# // <copyright file="ArithmeticPostconditionsTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode

class ArithmeticPostconditionsTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void MinimalExampleTest()
    # {
    #
    #     List<BaseGoal> goals = new() {
    #         new ComparativeGoal(
    #             name: "Goal1",
    #             desiredState: new() {
    #                 { "i", new ComparisonValuePair {
    #                     Value = 100,
    #                     Operator = ComparisonOperator.GreaterThan
    #                 } }
    #             },
    #             weight: 1f
    #         ),
    #     };
    #
    #     List<MountainGoap.Action> actions = new() {
    #         new MountainGoap.Action(
    #             name: "Action1",
    #             executor: (Agent agent, MountainGoap.Action action) => {
    #                 return ExecutionStatus.Succeeded;
    #             },
    #             arithmeticPostconditions: new Dictionary<string, object> {
    #                 { "i", 10 }
    #             },
    #             cost: 0.5f
    #         ),
    #     };
    #
    #     Agent agent = new(
    #         goals: goals,
    #         actions: actions,
    #         state: new() {
    #             { "i", 0 }
    #         }
    #     );
    #
    #     agent.Step(StepMode.OneAction);
    #     Assert.Equal(10, agent.State["i"]);
    #     agent.Step(StepMode.OneAction);
    #     Assert.Equal(20, agent.State["i"]);
    # }
    def test_minimal_example_test(self):
        goals = [
            ComparativeGoal(
                name="Goal1",
                desired_state={
                    "i": ComparisonValuePair(
                        value=100,
                        operator=ComparisonOperator.GreaterThan
                    )
                },
                weight=1.0
            ),
        ]

        actions = [
            Action(
                name="Action1",
                executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded,
                arithmetic_postconditions={
                    "i": 10
                },
                cost=0.5
            ),
        ]

        agent = Agent(
            goals=goals,
            actions=actions,
            state={
                "i": 0
            }
        )

        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 10
        assert not agent.IsBusy # Should not be busy after one step as goal not met and it keeps planning

        # Agent should re-plan and execute again
        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 20
        assert not agent.IsBusy

        # Keep stepping until goal is met
        for _ in range(8): # From 20 to 100 requires 8 more steps of +10
            agent.step(StepMode.OneAction)

        assert agent.State["i"] == 100
        # The goal is "greater than 100", so 100 is not enough. It will need one more.
        assert not agent.CurrentActionSequences # Should be empty as it planned to 100 but not > 100

        # Plan and execute one more step to reach > 100
        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 110
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences

```

---

**MountainGoapTest/PermutationSelectorGeneratorTests.py**

```python
# // <copyright file="PermutationSelectorGeneratorTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from typing import Dict, Any, List, Optional

class PermutationSelectorGeneratorTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void ItSelectsFromACollection() {
    #     var collection = new List<int> { 1, 2, 3 };
    #     var selector = PermutationSelectorGenerators.SelectFromCollection(collection);
    #     List<object> permutations = selector(new ConcurrentDictionary<string, object?>());
    #     Assert.Equal(3, permutations.Count);
    # }
    def test_it_selects_from_a_collection(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection(collection)
        permutations = selector({}) # Empty state dict
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

    # [Fact]
    # public void ItSelectsFromACollectionInState() {
    #     var collection = new List<int> { 1, 2, 3 };
    #     var selector = PermutationSelectorGenerators.SelectFromCollectionInState<int>("collection");
    #     List<object> permutations = selector(new ConcurrentDictionary<string, object?> { { "collection", collection } });
    #     Assert.Equal(3, permutations.Count);
    # }
    def test_it_selects_from_a_collection_in_state(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection_in_state("collection")
        permutations = selector({"collection": collection})
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

    # [Fact]
    # public void ItSelectsFromAnIntegerRange() {
    #     var selector = PermutationSelectorGenerators.SelectFromIntegerRange(1, 4);
    #     List<object> permutations = selector(new ConcurrentDictionary<string, object?>());
    #     Assert.Equal(3, permutations.Count);
    # }
    def test_it_selects_from_an_integer_range(self):
        selector = PermutationSelectorGenerators.select_from_integer_range(1, 4)
        permutations = selector({}) # Empty state dict
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

```

---

**MountainGoapTest/PermutationSelectorTests.py**

```python
# // <copyright file="PermutationSelectorTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoap.Sensor import Sensor
from MountainGoap.StepMode import StepMode
from typing import Dict, Any, List, Optional

class PermutationSelectorTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    # [Fact]
    # public void ItSelectsFromADynamicallyGeneratedCollectionInState() {
    #     var collection = new List<int> { 1, 2, 3 };
    #     var selector = PermutationSelectorGenerators.SelectFromCollectionInState<int>("collection");
    #     var agent = new Agent(
    #         name: "sample agent",
    #         state: new() {
    #             { "collection", collection },
    #             { "goalAchieved", false }
    #         },
    #         goals: new() {
    #             new Goal(
    #                 name: "sample goal",
    #                 desiredState: new Dictionary<string, object?> {
    #                     { "goalAchieved", true }
    #                 }
    #             )
    #         },
    #         actions: new() {
    #             new(
    #                 name: "sample action",
    #                 cost: 1f,
    #                 preconditions: new() {
    #                     { "goalAchieved", False }
    #                 },
    #                 postconditions: new() {
    #                     { "goalAchieved", True }
    #                 },
    #                 executor: (agent, action) => { return ExecutionStatus.Succeeded; }
    #             )
    #         },
    #         sensors: new() {
    #             new(
    #                 (agent) => {
    #                     if (agent.State["collection"] is List<int> collection) {
    #                         collection.Add(4);
    #                     }
    #                 },
    #                 name: "sample sensor"
    #             )
    #         }
    #     );
    #     List<object> permutations = selector(agent.State);
    #     Assert.Equal(3, permutations.Count);
    #     agent.Step(StepMode.OneAction);
    #     permutations = selector(agent.State);
    #     Assert.Equal(4, permutations.Count);
    #     agent.Step(StepMode.OneAction);
    #     permutations = selector(agent.State);
    #     Assert.Equal(5, permutations.Count);
    # }
    def test_it_selects_from_a_dynamically_generated_collection_in_state(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection_in_state("collection")

        def sample_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            return ExecutionStatus.Succeeded

        def sample_sensor_run(agent_inst: Agent) -> None:
            if isinstance(agent_inst.State.get("collection"), list):
                # Ensure it's a list of ints explicitly if needed, though Python is dynamic
                agent_inst.State["collection"].append(len(agent_inst.State["collection"]) + 1)

        agent = Agent(
            name="sample agent",
            state={
                "collection": collection,
                "goalAchieved": False
            },
            goals=[
                Goal(
                    name="sample goal",
                    desired_state={
                        "goalAchieved": True
                    }
                )
            ],
            actions=[
                Action(
                    name="sample action",
                    cost=1.0,
                    preconditions={
                        "goalAchieved": False
                    },
                    postconditions={
                        "goalAchieved": True
                    },
                    executor=sample_executor
                )
            ],
            sensors=[
                Sensor(
                    run_callback=sample_sensor_run,
                    name="sample sensor"
                )
            ]
        )

        # Before any steps, the selector should see the initial collection size
        permutations = selector(agent.State)
        assert len(permutations) == 3
        assert agent.State["collection"] == [1, 2, 3]

        # Step 1: Agent plans and executes 'sample action'. Sensor runs BEFORE planning.
        # So, the collection should be updated by the sensor before the planner uses it.
        agent.step(StepMode.OneAction) # Sensor runs, then plan, then 1 action executed
        
        # After step 1, the sensor should have added an item.
        # The plan for step 1 was based on the state *before* the sensor run in this step.
        # But for the *next* planning cycle (after this step is done), the new state is visible.
        # Let's re-evaluate permutations (which reads current agent.State)
        permutations = selector(agent.State)
        assert len(permutations) == 4
        assert agent.State["collection"] == [1, 2, 3, 4]
        assert agent.State["goalAchieved"] is True # The action should have completed the goal

        # Step 2: Agent tries to plan again, but goal is met, so no new plan.
        # Sensor will still run.
        agent.step(StepMode.OneAction)
        
        permutations = selector(agent.State)
        assert len(permutations) == 5
        assert agent.State["collection"] == [1, 2, 3, 4, 5]
        # goalAchieved remains true, no new action from planning.

```