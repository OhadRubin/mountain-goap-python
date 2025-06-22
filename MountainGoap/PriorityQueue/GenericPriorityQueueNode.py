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

