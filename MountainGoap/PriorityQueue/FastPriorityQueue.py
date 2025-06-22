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

