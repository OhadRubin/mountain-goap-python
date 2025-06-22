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

