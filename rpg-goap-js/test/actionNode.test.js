import { test } from 'node:test';
import assert from 'assert';
import { Action } from '../src/goap/actions.js';
import { ActionNode } from '../src/goap/planning.js';

test('ActionNode equality and hash', () => {
  const a1 = new Action({ name: 'a' });
  const n1 = new ActionNode(a1, { v: 1 }, {});
  const a2 = new Action({ name: 'a' });
  const n2 = new ActionNode(a2, { v: 1 }, {});
  assert.ok(n1.equals(n2));
  assert.strictEqual(n1.hashCode(), n2.hashCode());
});
