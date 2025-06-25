import { test } from "node:test";
import assert from 'assert';
import { PriorityQueue, PriorityQueueNode } from '../src/goap/utils.js';

class Node extends PriorityQueueNode {}

test('priority queue ordering', () => {
  const pq = new PriorityQueue();
  const a = new Node();
  const b = new Node();
  pq.enqueue(a, 2);
  pq.enqueue(b, 1);
  assert.strictEqual(pq.dequeue(), b);
  assert.strictEqual(pq.dequeue(), a);
});
