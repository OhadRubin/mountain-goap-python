import { PriorityQueueNode } from './types.js';
import { Goal, ExtremeGoal, ComparativeGoal, ComparisonOperator } from './goals.js';

/**
 * Simple priority queue for GOAP algorithms.
 * Not optimized for huge data sets but sufficient for tests.
 */
export class PriorityQueue {
  constructor() {
    this._heap = [];
    this._entryMap = new Map();
    this._counter = 0;
  }

  enqueue(item, priority) {
    if (this._entryMap.has(item)) {
      const entry = this._entryMap.get(item);
      entry.removed = true;
    }
    const entry = { priority, index: this._counter++, item, removed: false };
    this._entryMap.set(item, entry);
    this._heap.push(entry);
    this._heap.sort((a, b) => a.priority - b.priority || a.index - b.index);
  }

  dequeue() {
    while (this._heap.length > 0) {
      const entry = this._heap.shift();
      if (!entry.removed) {
        this._entryMap.delete(entry.item);
        return entry.item;
      }
    }
    throw new Error('Cannot dequeue from an empty priority queue.');
  }

  updatePriority(item, newPriority) {
    this.enqueue(item, newPriority);
  }

  contains(item) {
    return this._entryMap.has(item) && !this._entryMap.get(item).removed;
  }

  get count() {
    let c = 0;
    for (const entry of this._heap) {
      if (!entry.removed) c++;
    }
    return c;
  }
}

export class DictionaryExtensionMethods {
  static copyDict(obj) {
    return { ...obj };
  }

  static copyConcurrentDict(obj) {
    return { ...obj };
  }

  static copyComparisonValuePairDict(obj) {
    return { ...obj };
  }

  static copyStringDict(obj) {
    return { ...obj };
  }

  static copyNonNullableDict(obj) {
    return { ...obj };
  }
}

export class Utils {
  static isLowerThan(a, b) {
    return typeof a === 'number' && typeof b === 'number' ? a < b : false;
  }

  static isHigherThan(a, b) {
    return typeof a === 'number' && typeof b === 'number' ? a > b : false;
  }

  static isLowerThanOrEquals(a, b) {
    return typeof a === 'number' && typeof b === 'number' ? a <= b : false;
  }

  static isHigherThanOrEquals(a, b) {
    return typeof a === 'number' && typeof b === 'number' ? a >= b : false;
  }

  static meetsGoal(goal, node, prev) {
    if (goal instanceof Goal) {
      for (const [k, v] of Object.entries(goal.desiredState)) {
        if (!(k in node.state)) return false;
        const cur = node.state[k];
        if (cur === null && v !== null) return false;
        if (cur !== null && cur !== v) return false;
      }
      return true;
    } else if (goal instanceof ExtremeGoal) {
      if (!node.action) return false;
      for (const [k, maximize] of Object.entries(goal.desiredState)) {
        if (!(k in node.state) || !(k in prev.state)) return false;
        const cur = node.state[k];
        const prevVal = prev.state[k];
        if (cur == null || prevVal == null) return false;
        if (maximize) {
          if (!Utils.isHigherThanOrEquals(cur, prevVal)) return false;
        } else {
          if (!Utils.isLowerThanOrEquals(cur, prevVal)) return false;
        }
      }
      return true;
    } else if (goal instanceof ComparativeGoal) {
      for (const [k, pair] of Object.entries(goal.desiredState)) {
        if (!(k in node.state) || !(k in prev.state)) return false;
        const cur = node.state[k];
        const desired = pair.value;
        const op = pair.operator;
        if (op === ComparisonOperator.Undefined) return false;
        if (op === ComparisonOperator.Equals && cur !== desired) return false;
        if (op === ComparisonOperator.LessThan) {
          if (cur == null || desired == null) return false;
          if (!Utils.isLowerThan(cur, desired)) return false;
        } else if (op === ComparisonOperator.GreaterThan) {
          if (cur == null || desired == null) return false;
          if (!Utils.isHigherThan(cur, desired)) return false;
        } else if (op === ComparisonOperator.LessThanOrEquals) {
          if (cur == null || desired == null) return false;
          if (!Utils.isLowerThanOrEquals(cur, desired)) return false;
        } else if (op === ComparisonOperator.GreaterThanOrEquals) {
          if (cur == null || desired == null) return false;
          if (!Utils.isHigherThanOrEquals(cur, desired)) return false;
        }
      }
      return true;
    }
    return false;
  }
}

export class PermutationSelectorGenerators {
  static selectFromCollection(values) {
    return (state) => values.filter((v) => v != null);
  }

  static selectFromCollectionInState(key) {
    return (state) => {
      const output = [];
      const values = state[key];
      if (Array.isArray(values)) {
        for (const item of values) {
          if (item != null) output.push(item);
        }
      }
      return output;
    };
  }

  static selectFromIntegerRange(lower, upper) {
    return (state) => {
      const out = [];
      for (let i = lower; i < upper; i++) out.push(i);
      return out;
    };
  }
}

export { PriorityQueueNode };
