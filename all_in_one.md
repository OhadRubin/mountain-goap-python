```python
# // <copyright file="CostCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

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

class BaseGoal:
    """
    Represents an abstract class for a goal to be achieved for an agent.
    """

    Name: str

    Weight: float

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

class ComparisonOperator(Enum):
    """
    List of operators that can be used for comparison.
    """

    Undefined = 0

    Equals = 1

    LessThan = 2

    LessThanOrEquals = 3

    GreaterThan = 4

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

class ComparisonValuePair:
    """
    List of operators that can be used for comparison.
    """

    Value: Optional[Any] = None

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

class ComparativeGoal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    DesiredState: Dict[str, ComparisonValuePair]

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

class ExecutionStatus(Enum):
    """
    Possible execution status for an action.
    """

    NotYetExecuted = 1

    Executing = 2

    Succeeded = 3

    Failed = 4

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

class ExtremeGoal(BaseGoal):
    """
    Represents a goal requiring an extreme value to be achieved for an agent.
    """

    DesiredState: Dict[str, bool]

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

class Goal(BaseGoal):
    """
    Represents a goal to be achieved for an agent.
    """

    DesiredState: Dict[str, Optional[Any]]

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

class StepMode(Enum):
    """
    Different modes with which MountainGoap can execute an agent step.
    """

    Default = 1

    OneAction = 2

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

class DictionaryExtensionMethods:
    """
    Extension method to copy a dictionary of strings and objects.
    In Python, this will be implemented as static methods since there are no true extension methods.
    """

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

class FastPriorityQueueNode:
    """
    Base class for nodes in FastPriorityQueue.
    """

    Priority: float

    QueueIndex: int

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

class GenericPriorityQueueNode(FastPriorityQueueNode): # Inherit from FastPriorityQueueNode (or a common base)
    """
    Base class for nodes in GenericPriorityQueue.
    """
    Priority: TPriority

    QueueIndex: int # Inherited from FastPriorityQueueNode

    InsertionIndex: int # Using int for simplicity instead of long

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

class StablePriorityQueueNode(FastPriorityQueueNode):
    """
    Base class for nodes in StablePriorityQueue.
    """

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

class IPriorityQueue(ABC, Generic[TItem, TPriority], Iterable[TItem]):
    """
    The IPriorityQueue interface.
    """

    @abstractmethod
    def enqueue(self, node: TItem, priority: TPriority) -> None:
        """
        Enqueue a node to the priority queue. Lower values are placed in front.
        """
        pass

    @abstractmethod
    def dequeue(self) -> TItem:
        """
        Removes the head of the queue (node with minimum priority), and returns it.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Removes every node from the queue.
        """
        pass

    @abstractmethod
    def contains(self, node: TItem) -> bool:
        """
        Returns whether the given node is in the queue.
        """
        pass

    @abstractmethod
    def remove(self, node: TItem) -> None:
        """
        Removes a node from the queue.
        """
        pass

    @abstractmethod
    def update_priority(self, node: TItem, priority: TPriority) -> None:
        """
        Call this method to change the priority of a node.
        """
        pass

    @property
    @abstractmethod
    def first(self) -> TItem:
        """
        Returns the head of the queue, without removing it.
        """
        pass

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

class IFixedSizePriorityQueue(IPriorityQueue[TItem, TPriority], Generic[TItem, TPriority]):
    """
    A helper-interface for fixed-size priority queues.
    """

    @abstractmethod
    def resize(self, max_nodes: int) -> None:
        """
        Resize the queue so it can accept more nodes.
        """
        pass

    @property
    @abstractmethod
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue.
        """
        pass

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

class FastPriorityQueue(IFixedSizePriorityQueue[T, float]):
    """
    An implementation of a min-Priority Queue using a heap.
    This is a simplified Python implementation using heapq.
    """

    _num_nodes: int
    _nodes: List[Optional[T]] # Using a list as the heap
    _node_to_index: Dict[T, int] # For O(1) contains and fast updates
    _insertion_order: int # Counter for tie-breaking in stable queues

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

    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

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

    def _has_higher_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        """
        if higher is None or lower is None:
            return False
        return higher.Priority < lower.Priority

    def _has_higher_or_equal_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher or equal priority than 'lower', false otherwise.
        """
        if higher is None or lower is None:
            return False
        return higher.Priority <= lower.Priority

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

    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

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

    def _has_higher_priority(self, higher: Optional[TItem], lower: Optional[TItem]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        Includes tie-breaking by InsertionIndex.
        """
        if higher is None or lower is None:
            return False

        cmp = self._comparer(higher.Priority, lower.Priority)
        return (cmp < 0) or (cmp == 0 and higher.InsertionIndex < lower.InsertionIndex)


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

class StablePriorityQueue(IFixedSizePriorityQueue[T, float]):
    """
    A stable priority queue implementation.
    This is a simplified Python implementation using heapq.
    """

    _num_nodes: int
    _nodes: List[Optional[T]] # Using a list as the heap (1-indexed conceptually)
    _node_to_index: Dict[T, int] # For O(1) contains and fast updates
    _num_nodes_ever_enqueued: int # For tie-breaking (insertion order)

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

    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        return self._num_nodes

    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be enqueued at once in this queue. O(1)
        """
        return len(self._nodes) - 1

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

    def _has_higher_priority(self, higher: Optional[T], lower: Optional[T]) -> bool:
        """
        Returns true if 'higher' has higher priority than 'lower', false otherwise.
        Includes tie-breaking by InsertionIndex.
        """
        if higher is None or lower is None:
            return False
        return (higher.Priority < lower.Priority) or \
               (higher.Priority == lower.Priority and higher.InsertionIndex < lower.InsertionIndex)

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

        self._on_node_updated(former_last_node, old_priority_of_former_last_node)
        return return_me

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

class SimplePriorityQueue(IPriorityQueue[TItem, TPriority]):
    """
    A simplified priority queue implementation. Is stable, auto-resizes, and thread-safe.
    """

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

    def _get_existing_node(self, item: TItem) -> Optional[_SimpleNode]:
        """
        Given an item of type T, returns the existing SimpleNode in the queue.
        Assumes lock is already held.
        """
        if item is None:
            return self._null_nodes_cache[0] if self._null_nodes_cache else None

        nodes = self._item_to_nodes_cache.get(item)
        return nodes[0] if nodes else None

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

    @property
    def count(self) -> int:
        """
        Returns the number of nodes in the queue. O(1)
        """
        with self._lock:
            return self._queue.count

    @property
    def first(self) -> TItem:
        """
        Returns the head of the queue, without removing it. O(1)
        """
        with self._lock:
            if self._queue.count <= 0:
                raise RuntimeError("Cannot call .first on an empty queue")
            return self._queue.first.Data

    def clear(self) -> None:
        """
        Removes every node from the queue. O(n)
        """
        with self._lock:
            self._queue.clear()
            self._item_to_nodes_cache.clear()
            self._null_nodes_cache.clear()

    def contains(self, item: TItem) -> bool:
        """
        Returns whether the given item is in the queue. O(1)
        """
        with self._lock:
            if item is None:
                return len(self._null_nodes_cache) > 0
            return item in self._item_to_nodes_cache

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

    def _enqueue_no_lock_or_cache(self, item: TItem, priority: TPriority) -> _SimpleNode:
        """
        Internal helper: Enqueue the item without external locking/caching logic.
        """
        node = self._SimpleNode(item)
        if self._queue.count == self._queue.max_size:
            self._queue.resize(self._queue.max_size * 2 + 1) # Auto-resize
        self._queue.enqueue(node, priority)
        return node

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


    def update_priority(self, item: TItem, priority: TPriority) -> None:
        """
        Call this method to change the priority of an item. O(log n)
        """
        with self._lock:
            update_me = self._get_existing_node(item)
            if update_me is None:
                raise RuntimeError(f"Cannot call update_priority() on a node which is not enqueued: {item}")
            self._queue.update_priority(update_me, priority)

    def get_priority(self, item: TItem) -> TPriority:
        """
        Returns the priority of the given item. O(1)
        """
        with self._lock:
            find_me = self._get_existing_node(item)
            if find_me is None:
                raise RuntimeError(f"Cannot call get_priority() on a node which is not enqueued: {item}")
            return find_me.Priority

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

    def __iter__(self) -> Iterable[TItem]:
        """
        Returns an iterator over the items currently in the queue.
        """
        queue_data: List[TItem] = []
        with self._lock:
            for node in self._queue:
                queue_data.append(node.Data)
        return iter(queue_data)

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

class Utils:
    """
    Utilities for the MountainGoap library.
    """

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

class ActionNode(FastPriorityQueueNode):
    """
    Represents an action node in an action graph.
    """

    State: Dict[str, Optional[Any]]

    Parameters: Dict[str, Optional[Any]]

    Action: Optional['Action']

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


    def __ne__(self, other: object) -> bool:
        """
        Overrides the inequality operator on ActionNodes.
        """
        return not self.__eq__(other)

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

    def cost(self, current_state: Dict[str, Optional[Any]]) -> float:
        """
        Cost to traverse this node.
        """
        if self.Action is None:
            return float('inf') # float.MaxValue in C#
        return self.Action.get_cost(current_state)

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

class Action:
    """
    Represents an action in a GOAP system.
    """

    Name: str

    _cost_base: float

    _permutation_selectors: Dict[str, PermutationSelectorCallback]

    _executor: ExecutorCallback

    _cost_callback: CostCallback

    _preconditions: Dict[str, Optional[Any]]

    _comparative_preconditions: Dict[str, ComparisonValuePair]

    _postconditions: Dict[str, Optional[Any]]

    _arithmetic_postconditions: Dict[str, Any] # Non-nullable in C#

    _parameter_postconditions: Dict[str, str]

    _state_mutator: Optional[StateMutatorCallback]

    _state_checker: Optional[StateCheckerCallback]

    _parameters: Dict[str, Optional[Any]]

    StateCostDeltaMultiplier: Optional[StateCostDeltaMultiplierCallback]

    # Events (static in C#)
    OnBeginExecuteAction: BeginExecuteActionEvent
    OnFinishExecuteAction: FinishExecuteActionEvent

    ExecutionStatus: ExecutionStatus = ExecutionStatus.NotYetExecuted

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

    def set_parameter(self, key: str, value: Any) -> None:
        """
        Sets a parameter to the action.
        """
        self._parameters[key] = value

    def get_parameter(self, key: str) -> Optional[Any]:
        """
        Gets a parameter to the action.
        """
        return self._parameters.get(key)

    def get_cost(self, current_state: StateDictionary) -> float:
        """
        Gets the cost of the action.
        """
        try:
            return self._cost_callback(self, current_state)
        except Exception:
            return float('inf') # float.MaxValue in C#

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

    def set_parameters(self, parameters: Dict[str, Optional[Any]]) -> None:
        """
        Sets all parameters to the action.
        """
        self._parameters = parameters

    @staticmethod
    def _indices_at_maximum(indices: List[int], counts: List[int]) -> bool:
        """
        Checks if all indices are at their maximum allowed value (last element of their respective list).
        """
        for i in range(len(indices)):
            if indices[i] < counts[i] - 1:
                return False
        return True

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

class Agent:
    """
    GOAP agent.
    """

    Name: str

    CurrentActionSequences: List[List[Action]]

    State: StateDictionary

    Memory: Dict[str, Optional[Any]]

    Goals: List[BaseGoal]

    Actions: List[Action]

    Sensors: List[Sensor]

    CostMaximum: float

    StepMaximum: int

    IsBusy: bool = False

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


    def clear_plan(self) -> None:
        """
        Clears the current action sequences (also known as plans).
        """
        self.CurrentActionSequences.clear()

    def plan(self) -> None:
        """
        Makes a plan.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            Planner.plan(self, self.CostMaximum, self.StepMaximum)

    def plan_async(self) -> None:
        """
        Makes a plan asynchronously.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum))
            thread.start()

    def execute_plan(self) -> None:
        """
        Executes the current plan.
        """
        if not self.IsPlanning:
            self._execute()

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

class Sensor:
    """
    Sensor for getting information about world state.
    """

    Name: str

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


    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
        """
        Initializes a new instance of the Sensor class.
        """
        # In C#, GetMethodInfo().Name is used for default name.
        # In Python, we can get the function's __name__ attribute.
        callback_name = run_callback.__name__ if hasattr(run_callback, '__name__') else str(run_callback)
        self.Name = name if name is not None else f"Sensor {uuid.uuid4()} ({callback_name})"
        self._run_callback = run_callback

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


class PermutationSelectorGenerators:
    """
    Generators for default permutation selectors for convenience.
    """

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

class ActionGraph:
    """
    Represents a traversable action graph.
    """

    ActionNodes: List[ActionNode]

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

class ActionAStar:
    """
    AStar calculator for an action graph.
    """

    FinalPoint: Optional[ActionNode] = None

    CostSoFar: Dict[ActionNode, float] = {} # Using standard dict for simplicity in Python

    StepsSoFar: Dict[ActionNode, int] = {} # Using standard dict for simplicity in Python

    CameFrom: Dict[ActionNode, ActionNode] = {} # Using standard dict for simplicity in Python

    _goal: BaseGoal

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
                        # This means if current > prev, (current-prev) is positive, so cost reduces.
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

class Planner:
    """
    Planner for an agent.
    """

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
        # Serilog's Logger configures sinks, while Python's Logger manages handlers.
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

    def test_it_selects_from_a_collection(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection(collection)
        permutations = selector({}) # Empty state dict
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

    def test_it_selects_from_a_collection_in_state(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection_in_state("collection")
        permutations = selector({"collection": collection})
        assert len(permutations) == 3
        assert sorted(permutations) == [1, 2, 3]

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

---

**Examples/ArithmeticHappinessIncrementer.py**

```python
# // <copyright file="ArithmeticHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
# or current directory structure allows direct relative imports
# For this example, assuming sys.path has been configured (e.g., via conftest.py or manual setup)
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ArithmeticHappinessIncrementer:
    """
    Simple goal to maximize happiness using arithmetic postconditions.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
            },
            goals=[
                Goal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": 10
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ArithmeticHappinessIncrementer._seek_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ArithmeticHappinessIncrementer._seek_greater_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                )
            ]
        )

        # The loop condition in C#: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        # `is int happiness` performs a type check and casts. In Python, we just check the value.
        while agent.State.get("happiness") != 10:
            agent.step()
            print(f"NEW HAPPINESS IS {agent.State.get('happiness')}")
            # Add a small delay to make output readable if running fast
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_greater_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking even greater happiness.")
        return ExecutionStatus.Succeeded

```

---

**Examples/CarDemo.py**

```python
# // <copyright file="CarDemo.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoapLogging.DefaultLogger import DefaultLogger

class CarDemo:
    """
    Simple goal to travel via walking or driving.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Driving Agent",
            state={
                "distanceTraveled": 0,
                "inCar": False
            },
            goals=[
                ComparativeGoal(
                    name="Travel 50 miles",
                    desired_state={
                        "distanceTraveled": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=50
                        )
                    })
            ],
            actions=[
                Action(
                    name="Walk",
                    cost=50.0,
                    postconditions={
                        "distanceTraveled": 50
                    },
                    executor=CarDemo._travel_executor
                ),
                Action(
                    name="Drive",
                    cost=5.0,
                    preconditions={
                        "inCar": True
                    },
                    postconditions={
                        "distanceTraveled": 50
                    },
                    executor=CarDemo._travel_executor
                ),
                Action(
                    name="Get in Car",
                    cost=1.0,
                    preconditions={
                        "inCar": False
                    },
                    postconditions={
                        "inCar": True
                    },
                    executor=CarDemo._get_in_car_executor
                )
            ]
        )

        # C# while loop condition: `while (agent.State["distanceTraveled"] is int distance && distance < 50)`
        while agent.State.get("distanceTraveled") is not None and agent.State["distanceTraveled"] < 50:
            agent.step()
            # Optional: Add print statement to see progress
            # print(f"Distance traveled: {agent.State.get('distanceTraveled')}, In car: {agent.State.get('inCar')}")
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _travel_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _get_in_car_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}")
        return ExecutionStatus.Succeeded

```

---

**Examples/ComparativeHappinessIncrementer.py**

```python
# // <copyright file="ComparativeHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ComparativeHappinessIncrementer:
    """
    Simple goal to maximize happiness using comparative goals.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
            },
            goals=[
                ComparativeGoal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=10
                        )
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ComparativeHappinessIncrementer._seek_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ComparativeHappinessIncrementer._seek_greater_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                )
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness < 10)`
        while agent.State.get("happiness") is not None and agent.State["happiness"] < 10:
            agent.step()
            print(f"NEW HAPPINESS IS {agent.State.get('happiness')}")
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_greater_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking even greater happiness.")
        return ExecutionStatus.Succeeded

```

---

**Examples/ConsumerDemo.py**

```python
# // <copyright file="ConsumerDemo.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional, List

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ConsumerDemo:
    """
    Goal to create enough food to eat by working and grocery shopping.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        locations = ["home", "work", "store"]
        
        agent = Agent(
            name="Consumer Agent",
            state={
                "food": 0,
                "energy": 100,
                "money": 0,
                "inCar": False,
                "location": "home",
                "justTraveled": False
            },
            goals=[
                ComparativeGoal(
                    name="Get at least 5 food",
                    desired_state={
                        "food": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=5
                        )
                    })
            ],
            actions=[
                Action(
                    name="Walk",
                    cost=6.0,
                    executor=ConsumerDemo._generic_executor,
                    preconditions={
                        "inCar": False
                    },
                    permutation_selectors={
                        "location": PermutationSelectorGenerators.select_from_collection(locations)
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    parameter_postconditions={
                        "location": "location" # Parameter 'location' (from permutation selector) copied to state 'location'
                    }
                ),
                Action(
                    name="Drive",
                    cost=1.0,
                    preconditions={
                        "inCar": True,
                        "justTraveled": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    executor=ConsumerDemo._generic_executor,
                    permutation_selectors={
                        "location": PermutationSelectorGenerators.select_from_collection(locations)
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    parameter_postconditions={
                        "location": "location"
                    },
                    postconditions={
                        "justTraveled": True # Prevent repeated driving in one logical "turn" if the action implies a single move
                    }
                ),
                Action(
                    name="Get in car",
                    cost=1.0,
                    preconditions={
                        "inCar": False,
                        "justTraveled": False # Cannot get in car if just traveled implies it's part of same "turn"
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    postconditions={
                        "inCar": True
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Get out of car",
                    cost=1.0,
                    preconditions={
                        "inCar": True
                    },
                    comparative_preconditions={
                        "energy": ComparisonOperator.GreaterThan, value=0 # C# code is missing ComparisonValuePair() here.
                                                                           # Assuming it should be `ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)`
                    },
                    postconditions={
                        "inCar": False
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Work",
                    cost=1.0,
                    preconditions={
                        "location": "work",
                        "inCar": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1,
                        "money": 1
                    },
                    postconditions={
                        "justTraveled": False # Reset justTraveled after arriving and working
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Shop",
                    cost=1.0,
                    preconditions={
                        "location": "store",
                        "inCar": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0),
                        "money": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1,
                        "money": -1, # Spend money to buy food
                        "food": 1
                    },
                    postconditions={
                        "justTraveled": False # Reset justTraveled after arriving and shopping
                    },
                    executor=ConsumerDemo._generic_executor
                )
            ]
        )

        # C# while loop condition: `while (agent.State["food"] is int food && food < 5)`
        step_count = 0
        max_steps = 100 # Safety break to prevent infinite loops in demos
        while agent.State.get("food") is not None and agent.State["food"] < 5 and step_count < max_steps:
            agent.step()
            step_count += 1
            print(f"--- Step {step_count} ---")
            print(f"Food: {agent.State.get('food')}, Energy: {agent.State.get('energy')}, Money: {agent.State.get('money')}, Location: {agent.State.get('location')}, In Car: {agent.State.get('inCar')}, Just Traveled: {agent.State.get('justTraveled')}")
            # import time
            # time.sleep(0.1)

        if step_count >= max_steps:
            print(f"ConsumerDemo stopped after {max_steps} steps without reaching goal.")
        else:
            print(f"ConsumerDemo finished in {step_count} steps. Food: {agent.State.get('food')}")


    @staticmethod
    def _generic_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}. Params: {action_instance._parameters}")
        return ExecutionStatus.Succeeded

```

---

**Examples/ExtremeHappinessIncrementer.py**

```python
# // <copyright file="ExtremeHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ExtremeGoal import ExtremeGoal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ExtremeHappinessIncrementer:
    """
    Simple goal to maximize happiness using extreme goals.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
                "health": False,
            },
            goals=[
                ExtremeGoal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": True # True to maximize, False to minimize
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ExtremeHappinessIncrementer._seek_happiness_action,
                    preconditions={
                        "health": True # Requires health to seek happiness
                    },
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ExtremeHappinessIncrementer._seek_greater_happiness_action,
                    preconditions={
                        "health": True # Requires health to seek greater happiness
                    },
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                ),
                Action(
                    name="Seek Health",
                    executor=ExtremeHappinessIncrementer._seek_health,
                    postconditions={
                        "health": True # Sets health to true
                    }
                ),
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        while agent.State.get("happiness") != 10:
            agent.step()
            print(f"NEW HAPPINESS IS {agent.State.get('happiness')}")
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_greater_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking even greater happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_health(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking health.")
        return ExecutionStatus.Succeeded

```

---

**Examples/HappinessIncrementer.py**

```python
# // <copyright file="HappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class HappinessIncrementer:
    """
    Simple goal to increment happiness using normal goals and a sensor.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
                "happinessRecentlyIncreased": False
            },
            goals=[
                Goal(
                    name="Maximize Happiness",
                    desired_state={
                        "happinessRecentlyIncreased": True
                    })
            ],
            sensors=[
                Sensor(HappinessIncrementer._ennui_sensor_handler, "Ennui Sensor")
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=HappinessIncrementer._seek_happiness_action,
                    preconditions={
                        "happinessRecentlyIncreased": False
                    },
                    postconditions={
                        "happinessRecentlyIncreased": True
                    }
                )
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        while agent.State.get("happiness") != 10:
            agent.step()
            # The Console.WriteLine for happiness is in SeekHappinessAction executor itself
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        happiness: Optional[int] = agent_instance.State.get("happiness")
        if happiness is not None and isinstance(happiness, int):
            happiness += 1
            agent_instance.State["happiness"] = happiness
            print("Seeking happiness.")
            print(f"NEW HAPPINESS IS {happiness}")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _ennui_sensor_handler(agent_instance: Agent) -> None:
        agent_instance.State["happinessRecentlyIncreased"] = False

```

---

**Examples/Program.py**

```python
# // <copyright file="Program.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import argparse # Standard Python library for command-line parsing

# Import demo runners
from .ArithmeticHappinessIncrementer import ArithmeticHappinessIncrementer
from .CarDemo import CarDemo
from .ComparativeHappinessIncrementer import ComparativeHappinessIncrementer
from .ConsumerDemo import ConsumerDemo
from .ExtremeHappinessIncrementer import ExtremeHappinessIncrementer
from .HappinessIncrementer import HappinessIncrementer
from .RpgExample.RpgExample import RpgExample

class Program:
    """
    Runs MountainGoap Demos.
    """

    @staticmethod
    def main(args: list[str]) -> int:
        parser = argparse.ArgumentParser(description="Run MountainGoap Demos.")
        subparsers = parser.add_subparsers(dest="command", help="Available demos")

        # Command: happiness
        happiness_parser = subparsers.add_parser("happiness", help="Run the happiness incrementer demo.")
        happiness_parser.set_defaults(func=Program._run_happiness_incrementer)

        # Command: rpg
        rpg_parser = subparsers.add_parser("rpg", help="Run the RPG enemy demo.")
        rpg_parser.set_defaults(func=Program._run_rpg_enemy_demo)

        # Command: arithmeticHappiness
        arithmetic_happiness_parser = subparsers.add_parser("arithmeticHappiness", help="Run the arithmetic happiness incrementer demo.")
        arithmetic_happiness_parser.set_defaults(func=Program._run_arithmetic_happiness_incrementer)

        # Command: extremeHappiness
        extreme_happiness_parser = subparsers.add_parser("extremeHappiness", help="Run the extreme happiness incrementer demo.")
        extreme_happiness_parser.set_defaults(func=Program._run_extreme_happiness_incrementer)

        # Command: comparativeHappiness
        comparative_happiness_parser = subparsers.add_parser("comparativeHappiness", help="Run the comparative happiness incrementer demo.")
        comparative_happiness_parser.set_defaults(func=Program._run_comparative_happiness_incrementer)

        # Command: car
        car_parser = subparsers.add_parser("car", help="Run the car demo.")
        car_parser.set_defaults(func=Program._run_car_demo)

        # Command: consumer
        consumer_parser = subparsers.add_parser("consumer", help="Run the consumer demo.")
        consumer_parser.set_defaults(func=Program._run_consumer_demo)

        if not args:
            parser.print_help()
            return 0

        parsed_args = parser.parse_args(args)

        if hasattr(parsed_args, 'func'):
            parsed_args.func()
            return 0
        else:
            parser.print_help()
            return 1 # Indicate an error or no command selected


    @staticmethod
    def _run_happiness_incrementer() -> None:
        HappinessIncrementer.run()

    @staticmethod
    def _run_rpg_enemy_demo() -> None:
        RpgExample.run()

    @staticmethod
    def _run_arithmetic_happiness_incrementer() -> None:
        ArithmeticHappinessIncrementer.run()

    @staticmethod
    def _run_extreme_happiness_incrementer() -> None:
        ExtremeHappinessIncrementer.run()

    @staticmethod
    def _run_comparative_happiness_incrementer() -> None:
        ComparativeHappinessIncrementer.run()

    @staticmethod
    def _run_car_demo() -> None:
        CarDemo.run()

    @staticmethod
    def _run_consumer_demo() -> None:
        ConsumerDemo.run()

# Standard Python entry point
if __name__ == "__main__":
    exit_code = Program.main(sys.argv[1:])
    sys.exit(exit_code)

```

---

**Examples/RpgExample/RpgUtils.py**

```python
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

```

---

**Examples/RpgExample/RpgCharacterFactory.py**

```python
# // <copyright file="RpgCharacterFactory.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and RpgUtils are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair

from .RpgUtils import RpgUtils, Vector2

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class RpgCharacterFactory:
    """
    Class for generating an RPG character.
    """

    @staticmethod
    def create(agents: List[Agent], name: str = "Player") -> Agent:
        """
        Returns an RPG character agent.
        """
        remove_enemies_goal = Goal(
            name="Remove Enemies",
            weight=1.0,
            desired_state={
                "canSeeEnemies": False
            }
        )

        see_enemies_sensor = Sensor(RpgCharacterFactory._see_enemies_sensor_handler, "Enemy Sight Sensor")
        enemy_proximity_sensor = Sensor(RpgCharacterFactory._enemy_proximity_sensor_handler, "Enemy Proximity Sensor")

        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=RpgCharacterFactory._go_to_enemy_executor,
            preconditions={
                "canSeeEnemies": True,
                "nearEnemy": False
            },
            postconditions={
                "nearEnemy": True
            },
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_enemy_cost
        )

        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=RpgCharacterFactory._kill_nearby_enemy_executor,
            preconditions={
                "nearEnemy": True
            },
            postconditions={
               "canSeeEnemies": False, # After killing, you might not see enemies immediately
               "nearEnemy": False      # And certainly not near this one
            }
        )

        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "hp": 10,
                "position": Vector2(10, 10), # Initial position
                "faction": "enemy" if "Monster" in name else "player", # Set default faction, will be overridden for player
                "agents": agents # Reference to the list of all agents in the world
            },
            goals=[
                remove_enemies_goal
            ],
            sensors=[
                see_enemies_sensor,
                enemy_proximity_sensor
            ],
            actions=[
                go_to_enemy_action,
                kill_nearby_enemy_action
            ]
        )
        return agent

    @staticmethod
    def _see_enemies_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 5.0)
            agent_instance.State["canSeeEnemies"] = (enemy_in_range is not None)

    @staticmethod
    def _enemy_proximity_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            agent_instance.State["nearEnemy"] = (enemy_in_range is not None)

    @staticmethod
    def _kill_nearby_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            target_enemy = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            if target_enemy is not None:
                current_hp = target_enemy.State.get("hp")
                if isinstance(current_hp, int):
                    current_hp -= 1
                    target_enemy.State["hp"] = current_hp
                    print(f"{agent_instance.Name} attacked {target_enemy.Name}. {target_enemy.Name} HP: {current_hp}")
                    if current_hp <= 0:
                        print(f"{target_enemy.Name} defeated!")
                        return ExecutionStatus.Succeeded # Action succeeds if enemy is defeated
        return ExecutionStatus.Failed # Action fails if no enemy or enemy not defeated

    @staticmethod
    def _go_to_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        target_agent = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(target_agent, Agent) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        target_position = target_agent.State.get("position")
        if not isinstance(target_position, Vector2):
            return ExecutionStatus.Failed
        
        # Move one step towards the target
        new_position = RpgUtils.move_towards_other_position(agent_position, target_position)
        agent_instance.State["position"] = new_position
        
        # Check if now within attacking distance (1 unit)
        if RpgUtils.in_distance(new_position, target_position, 1.0):
            return ExecutionStatus.Succeeded # Reached the proximity to engage
        else:
            return ExecutionStatus.Executing # Still moving, action continues next step

```

---

**Examples/RpgExample/RpgMonsterFactory.py**

```python
# // <copyright file="RpgMonsterFactory.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import sys
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and RpgUtils are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair

from .RpgUtils import RpgUtils, Vector2
from .RpgCharacterFactory import RpgCharacterFactory
from .RpgExample import RpgExample # To access MaxX, MaxY


# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class RpgMonsterFactory:
    """
    Class for generating an RPG monster.
    """

    _rng = random.Random() # Static Random instance
    _counter = 1 # Static counter for naming monsters

    @staticmethod
    def create(agents: List[Agent], food_positions: List[Vector2]) -> Agent:
        """
        Returns an RPG monster agent.
        """
        monster_name = f"Monster {RpgMonsterFactory._counter}"
        RpgMonsterFactory._counter += 1
        
        # Monster is an RPG character, so create using RpgCharacterFactory and then customize
        agent = RpgCharacterFactory.create(agents, monster_name)
        agent.State["faction"] = "enemy" # Ensure monster has enemy faction

        eat_food_goal = Goal(
            name="Eat Food",
            weight=0.1, # Lower weight than 'Remove Enemies' (which is 1.0)
            desired_state={
                "eatingFood": True
            }
        )

        see_food_sensor = Sensor(RpgMonsterFactory._see_food_sensor_handler, "Food Sight Sensor")
        food_proximity_sensor = Sensor(RpgMonsterFactory._food_proximity_sensor_handler, "Food Proximity Sensor")

        look_for_food_action = Action(
            name="Look For Food",
            executor=RpgMonsterFactory._look_for_food_executor,
            preconditions={
                "canSeeFood": False,
                "canSeeEnemies": False # Don't look for food if enemies are visible
            },
            postconditions={
                "canSeeFood": True # This action attempts to see food by moving around
            }
        )

        go_to_food_action = Action(
            name="Go To Food",
            executor=RpgMonsterFactory._go_to_food_executor,
            preconditions={
                "canSeeFood": True,
                "canSeeEnemies": False # Don't go to food if enemies are visible
            },
            postconditions={
                "nearFood": True
            },
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_food_cost
        )

        eat_action = Action(
            name="Eat",
            executor=RpgMonsterFactory._eat_executor,
            preconditions={
                "nearFood": True,
                "canSeeEnemies": False # Don't eat if enemies are visible
            },
            postconditions={
                "eatingFood": True # This state means the food is consumed
            }
        )
        
        # Set initial monster-specific state
        agent.State["canSeeFood"] = False
        agent.State["nearFood"] = False
        agent.State["eatingFood"] = False
        agent.State["foodPositions"] = food_positions # Reference to global food positions
        agent.State["hp"] = 2 # Monsters have less HP than player

        # Add monster-specific goals, sensors, actions
        agent.Goals.append(eat_food_goal)
        agent.Sensors.append(see_food_sensor)
        agent.Sensors.append(food_proximity_sensor)
        agent.Actions.append(go_to_food_action)
        agent.Actions.append(look_for_food_action)
        agent.Actions.append(eat_action)
        
        return agent

    @staticmethod
    def _get_food_in_range(source: Vector2, food_positions: List[Vector2], range_val: float) -> Optional[Vector2]:
        """
        Gets the first food position within a given range of a source position.
        """
        # C# FirstOrDefault with a default value.
        # In Python, we can loop or use next with a generator expression.
        for position in food_positions:
            if RpgUtils.in_distance(source, position, range_val):
                return position
        return None # No food found in range

    @staticmethod
    def _see_food_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 5.0)
            if food_in_range is not None:
                agent_instance.State["canSeeFood"] = True
            else:
                agent_instance.State["canSeeFood"] = False
                agent_instance.State["eatingFood"] = False # Cannot be eating if no food is seen

    @staticmethod
    def _food_proximity_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            if food_in_range is not None:
                agent_instance.State["nearFood"] = True
            else:
                agent_instance.State["nearFood"] = False
                agent_instance.State["eatingFood"] = False # Cannot be eating if not near food

    @staticmethod
    def _look_for_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agent_position = agent_instance.State.get("position")
        if isinstance(agent_position, Vector2):
            new_x = agent_position.X + RpgMonsterFactory._rng.randint(-1, 1) # randint includes both ends
            new_y = agent_position.Y + RpgMonsterFactory._rng.randint(-1, 1)

            # Clamp position within world bounds
            from .RpgExample import RpgExample # Local import to get MaxX, MaxY
            new_x = max(0, min(new_x, RpgExample.MaxX - 1))
            new_y = max(0, min(new_y, RpgExample.MaxY - 1))

            agent_instance.State["position"] = Vector2(new_x, new_y) # Update position

        # Check if food is now seen *after* moving
        # The sensor would run *after* this executor in the agent.step cycle,
        # but this check needs to be against the *current* state of `canSeeFood` before executor.
        # This executor is designed to succeed if food becomes true *after* its application.
        # However, the current code checks it *before* sensor updates the state.
        # The C# original also checks `agent.State["canSeeFood"]` after modifying `position` but before agent.Step finishes.
        # The crucial part is that `agent.State["canSeeFood"]` would be updated by the sensor *after* this action executes.
        # So, this action's success is determined by whether it *enabled* the sensor to see food.
        # If agent.State["canSeeFood"] is true from a prior run of the sensor, it means it's seen.
        # The `is bool canSeeFood && canSeeFood` checks `canSeeFood` as it *currently* is.
        # This implies it returns Succeeded if food was seen *before* the action or if the action doesn't change it.
        # A more direct interpretation of "look for food" succeeding when food is *now visible* might require
        # checking the condition immediately after its own effects are applied but before sensors run again.
        # For strict verbatim, use the existing state value:
        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed # Continue searching

    @staticmethod
    def _go_to_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_position = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(food_position, Vector2) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        new_position = RpgUtils.move_towards_other_position(agent_position, food_position)
        agent_instance.State["position"] = new_position

        if RpgUtils.in_distance(new_position, food_position, 1.0):
            return ExecutionStatus.Succeeded # Reached the food
        else:
            return ExecutionStatus.Executing # Still moving towards food

    @staticmethod
    def _eat_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_positions_in_state = agent_instance.State.get("foodPositions")
        agent_position = agent_instance.State.get("position")

        if isinstance(food_positions_in_state, list) and isinstance(agent_position, Vector2):
            food_to_eat = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            if food_to_eat is not None:
                print(f"{agent_instance.Name} ate food at {food_to_eat}")
                # Remove the food from the global list
                food_positions_in_state.remove(food_to_eat)
                return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed

```

---

**Examples/RpgExample/RpgExample.py**

```python
# // <copyright file="RpgExample.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import time
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.StepMode import StepMode
from MountainGoapLogging.DefaultLogger import DefaultLogger

from .RpgCharacterFactory import RpgCharacterFactory
from .RpgMonsterFactory import RpgMonsterFactory
from .RpgUtils import Vector2

# A helper function to clear the console (platform dependent)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class RpgExample:
    """
    RPG example demo.
    """

    MaxX: int = 20

    MaxY: int = 20

    @staticmethod
    def run() -> None:
        _ = DefaultLogger(log_to_console=False, logging_file="rpg-example.log")
        
        _random = random.Random() # Instance of Random
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = RpgCharacterFactory.create(agents)
        player.State["faction"] = "player" # Set player faction
        agents.append(player)

        # Create food positions
        for _ in range(20):
            food_positions.append(Vector2(_random.randint(0, RpgExample.MaxX - 1), _random.randint(0, RpgExample.MaxY - 1)))
        
        # Create monsters
        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(_random.randint(0, RpgExample.MaxX - 1), _random.randint(0, RpgExample.MaxY - 1))
            agents.append(monster)
        
        # Game loop
        for i in range(600): # 600 steps, each 200ms -> 120 seconds = 2 minutes
            print(f"--- Turn {i+1} ---")
            for agent in agents:
                agent.step(mode=StepMode.OneAction) # Each agent executes one action
            
            RpgExample._process_deaths(agents)
            RpgExample._print_grid(agents, food_positions)
            time.sleep(0.2) # 200ms delay

            # Check if player is still alive
            if player not in agents:
                print("Player defeated! Game Over.")
                break
            # Check if all monsters are defeated (goal met for player)
            monsters_alive = [a for a in agents if a.State.get("faction") == "enemy"]
            if not monsters_alive:
                print("All monsters defeated! You win!")
                break
            
        print("Game finished.")

    @staticmethod
    def _print_grid(agents: List[Agent], food_positions: List[Vector2]) -> None:
        clear_console() # Clear screen before printing new frame
        
        grid: List[List[str]] = [[" " for _ in range(RpgExample.MaxY)] for _ in range(RpgExample.MaxX)]

        for pos in food_positions:
            if 0 <= pos.X < RpgExample.MaxX and 0 <= pos.Y < RpgExample.MaxY:
                grid[int(pos.X)][int(pos.Y)] = "f"

        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")
            
            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < RpgExample.MaxX and 0 <= agent_pos.Y < RpgExample.MaxY:
                    if agent_faction == "player":
                        grid[int(agent_pos.X)][int(agent_pos.Y)] = "@"
                    else: # Monster
                        grid[int(agent_pos.X)][int(agent_pos.Y)] = "g"
        
        for row in grid:
            print("".join(row))

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

```