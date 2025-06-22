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

