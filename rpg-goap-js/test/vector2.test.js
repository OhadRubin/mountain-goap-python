import { test } from "node:test";
import assert from 'assert';
import { Vector2, RpgUtils } from '../src/rpg/utils.js';

test('Vector2 utilities', () => {
  const v1 = new Vector2(0, 0);
  const v2 = new Vector2(1, 0);
  assert.ok(RpgUtils.inDistance(v1, v2, 1));
  const moved = RpgUtils.moveTowardsOtherPosition(v1, v2);
  assert.ok(moved.equals(new Vector2(1, 0)));
});
