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

