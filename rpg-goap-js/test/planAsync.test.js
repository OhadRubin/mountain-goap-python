import { test } from 'node:test';
import assert from 'assert';
import { Agent } from '../src/goap/agent.js';

// Plan async should set planning flag and eventually clear it when done.
// We just check the flag change immediately.

test('agent planAsync sets isPlanning', () => {
  const agent = new Agent({});
  agent.planAsync();
  assert.strictEqual(agent.isPlanning, true);
});
