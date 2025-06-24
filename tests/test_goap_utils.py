from goap_python.utils import PriorityQueue, PriorityQueueNode

class Node(PriorityQueueNode):
    pass

def test_priority_queue():
    pq = PriorityQueue()
    a = Node()
    b = Node()
    pq.enqueue(a, 2)
    pq.enqueue(b, 1)
    first = pq.dequeue()
    second = pq.dequeue()
    assert first is b
    assert second is a
