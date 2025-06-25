/**
 * @typedef {Object.<string, any>} StateDictionary
 */
export const StateDictionary = Object;

/**
 * Base class for nodes stored in PriorityQueue.
 */
export class PriorityQueueNode {
  constructor() {
    this.priority = 0;
    this.queueIndex = 0;
  }
}
