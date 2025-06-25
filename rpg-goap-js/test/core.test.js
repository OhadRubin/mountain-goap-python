import { test } from 'node:test';
import assert from 'assert';
import { Agent } from '../src/goap/agent.js';
import { Action, StepMode } from '../src/goap/actions.js';
import { Goal } from '../src/goap/goals.js';

// Simple action that sets state.done = true
const action = new Action({
  name: 'finish',
  executor: (agent, act) => {
    agent.state.done = true;
    return 3; // ExecutionStatus.Succeeded
  },
  postconditions: { done: true },
});

const goal = new Goal('done', 1, { done: true });

test('agent executes simple plan', () => {
  const agent = new Agent({ actions: [action], goals: [goal], state: {} });
  agent.plan();
  agent.step(StepMode.AllActions);
  assert.strictEqual(agent.state.done, true);
});
