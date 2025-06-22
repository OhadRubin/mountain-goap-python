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

