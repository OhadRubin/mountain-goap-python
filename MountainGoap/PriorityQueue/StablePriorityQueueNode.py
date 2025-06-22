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

