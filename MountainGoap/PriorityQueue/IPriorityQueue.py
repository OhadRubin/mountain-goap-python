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

