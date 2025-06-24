
# --- Priority Queue Implementation (Only FastPriorityQueue and its Node are kept) ---
class FastPriorityQueueNode:
    Priority: float
    QueueIndex: int

    def __init__(self):
        self.Priority = 0.0
        self.QueueIndex = 0


T = TypeVar("T", bound=FastPriorityQueueNode)


class FastPriorityQueue:
    _num_nodes: int
    _nodes: List[T]

    def __init__(self, max_nodes: int):
        if max_nodes <= 0:
            raise ValueError("New queue size cannot be smaller than 1")
        self._num_nodes = 0
        self._nodes = [cast(T, None)] * (max_nodes + 1)

    @property
    def count(self) -> int:
        return self._num_nodes

    @property
    def max_size(self) -> int:
        return len(self._nodes) - 1

    def clear(self) -> None:
        # Mimic C#'s Array.Clear by setting elements to None in place.
        # Also, reset node's internal state to indicate it's no longer in a queue.
        # Starting from index 1 as the 0th element is unused in this heap implementation.
        for i in range(1, self._num_nodes + 1):
            node_to_clear = self._nodes[i]
            if node_to_clear is not None:
                # Reset the node's internal queue state, as if it was removed/reset
                node_to_clear.QueueIndex = 0
            self._nodes[i] = cast(T, None)  # Set the array slot to None
        self._num_nodes = 0

    def contains(self, node: T) -> bool:
        if node is None:
            raise ValueError("node cannot be None")
        # C# only checks: return (_nodes[node.QueueIndex] == node);
        # Python should rely only on node.QueueIndex being valid and pointing to itself in _nodes
        is_at_correct_index = (
            0 < node.QueueIndex <= self._num_nodes  # Ensure index is within bounds of active nodes
            and self._nodes[node.QueueIndex] == node
        )
        return is_at_correct_index  # Direct check, no dict lookup

    def enqueue(self, node: T, priority: float) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        if self._num_nodes >= self.max_size:
            raise RuntimeError("Queue is full - node cannot be added")
        node.Priority = priority
        self._num_nodes += 1
        node.QueueIndex = self._num_nodes
        self._nodes[self._num_nodes] = node
        self._cascade_up(node)

    def _cascade_up(self, node: T) -> None:
        current_index = node.QueueIndex
        while current_index > 1:
            parent_index = current_index // 2
            parent_node = self._nodes[parent_index]
            if self._has_higher_or_equal_priority(parent_node, node):
                break
            self._nodes[current_index] = parent_node
            if parent_node is not None:
                parent_node.QueueIndex = current_index
            self._nodes[parent_index] = node
            node.QueueIndex = parent_index
            current_index = parent_index

    def _cascade_down(self, node: T) -> None:
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
                if swap_index == 0:
                    if self._has_higher_priority(child_right, node):
                        swap_index = child_right_index
                else:
                    child_to_compare = self._nodes[swap_index]
                    if self._has_higher_priority(child_right, child_to_compare):
                        swap_index = child_right_index
            if swap_index == 0:
                break
            swap_node = self._nodes[swap_index]
            self._nodes[current_index] = swap_node
            if swap_node is not None:
                swap_node.QueueIndex = current_index
            self._nodes[swap_index] = node
            node.QueueIndex = swap_index
            current_index = swap_index

    def _has_higher_priority(self, higher: T, lower: T) -> bool:
        return higher.Priority < lower.Priority

    def _has_higher_or_equal_priority(self, higher: T, lower: T) -> bool:
        return higher.Priority <= lower.Priority

    def dequeue(self) -> T:
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call dequeue() on an empty queue")
        return_me = self._nodes[1]
        if return_me is None:
            raise RuntimeError("Heap root is unexpectedly None")
        if self._num_nodes == 1:
            self._nodes[1] = None
            self._num_nodes = 0
            return_me.QueueIndex = 0
            return return_me
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node is unexpectedly None")
        self._nodes[1] = former_last_node
        former_last_node.QueueIndex = 1
        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1
        return_me.QueueIndex = 0
        self._cascade_down(former_last_node)
        return return_me

    def resize(self, max_nodes: int) -> None:
        if max_nodes <= 0:
            raise ValueError("Queue size cannot be smaller than 1")
        if max_nodes < self._num_nodes:
            raise ValueError(
                f"Called Resize({max_nodes}), but current queue contains {self._num_nodes} nodes"
            )
        new_nodes = [None] * (max_nodes + 1)
        for i in range(1, self._num_nodes + 1):
            new_nodes[i] = self._nodes[i]
        self._nodes = new_nodes

    @property
    def first(self) -> T:
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call .first on an empty queue")
        if self._nodes[1] is None:
            raise RuntimeError("First element in heap is unexpectedly None")
        return self._nodes[1]

    def update_priority(self, node: T, priority: float) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        old_priority = node.Priority
        node.Priority = priority
        self._on_node_updated(node)

    def _on_node_updated(self, node: T) -> None:
        parent_index = node.QueueIndex // 2
        if parent_index > 0 and self._has_higher_priority(node, self._nodes[parent_index]):
            self._cascade_up(node)
        else:
            self._cascade_down(node)

    def remove(self, node: T) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        if node.QueueIndex == self._num_nodes:
            self._nodes[self._num_nodes] = None
            self._num_nodes -= 1
            node.QueueIndex = 0
            return
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError(
                "Last node in heap is unexpectedly None during remove operation"
            )
        old_priority_of_former_last_node = former_last_node.Priority
        self._nodes[node.QueueIndex] = former_last_node
        former_last_node.QueueIndex = node.QueueIndex
        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1
        node.QueueIndex = 0
        self._on_node_updated(former_last_node)

    def reset_node(self, node: T) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        node.QueueIndex = 0

    def __iter__(self) -> Iterable[T]:
        active_nodes = []
        for i in range(1, self._num_nodes + 1):
            node = self._nodes[i]
            if node is not None:
                active_nodes.append(node)
        return iter(active_nodes)

    def is_valid_queue(self) -> bool:
        for i in range(1, self._num_nodes + 1):
            current_node = self._nodes[i]
            if current_node is None:
                return False
            if current_node.QueueIndex != i:
                return False
            child_left_index = 2 * i
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if child_left is None or self._has_higher_priority(
                    child_left, current_node
                ):
                    return False
            child_right_index = 2 * i + 1
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if child_right is None or self._has_higher_priority(
                    child_right, current_node
                ):
                    return False
        return True