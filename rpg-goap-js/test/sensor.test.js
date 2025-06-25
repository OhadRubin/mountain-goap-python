import { test } from 'node:test';
import assert from 'assert';
import { Sensor } from '../src/goap/sensors.js';
import { Agent } from '../src/goap/agent.js';

test('sensor onSensorRun event fires', () => {
  let called = false;
  const sensor = new Sensor(() => {}, 's');
  Sensor.registerOnSensorRun(() => {
    called = true;
  });
  const agent = new Agent();
  sensor.run(agent);
  assert.ok(called);
});
