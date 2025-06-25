// instructions how to run this
// npm init -y
// npm install uuid @datastructures-js/priority-queue
// then `timeout 5 node jsgoap_rpg.js` (otherwise you might hang)
// Verbatim port of the Python GOAP example to JavaScript.
// Note on threading: JS is single-threaded, so Python's `threading` and `locks` are
// handled differently. Agent steps run sequentially, removing the need for memory access locks.
// Note on Pygame: The `pygame` library is mocked to allow the simulation logic to run
// without a GUI. Output is logged to the console.
// Note on Hashing: Python's object hashing for dictionary keys is replicated by creating
// a `getHash()` method on `ActionNode` and using the resulting string as a key in JS `Map`s.

const { v4: uuidv4 } = require('uuid');
const { MinPriorityQueue } = require('@datastructures-js/priority-queue'); // Using a library for the simple PQ

// Python: import math -> JS: Math is built-in
// Python: import random -> JS: Custom random object
const random = {
    randint: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
    Random: function() { // Mimic random.Random() instance
        this.randint = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
        return this;
    }
};
// Python: import pygame -> JS: Mocking Pygame
const pygame = {
    init: () => console.log("Pygame mocked: init"),
    display: {
        set_mode: (size) => {
            console.log(`Pygame mocked: set_mode(${size})`);
            return {
                fill: (color) => {},
                get_rect: () => ({ center: [0, 0] })
            };
        },
        set_caption: (caption) => console.log(`Pygame mocked: set_caption("${caption}")`),
        flip: () => {},
    },
    time: {
        Clock: function() {
            this.tick = (fps) => {};
            return this;
        },
        get_ticks: () => Date.now(),
    },
    event: {
        get: () => [], // No events
    },
    QUIT: 'QUIT',
    draw: {
        line: () => {},
        ellipse: () => {},
        rect: () => {},
    },
    Rect: function(left, top, width, height) {
        this.left = left;
        this.top = top;
        this.width = width;
        this.height = height;
        return this;
    },
    Surface: class {}
};
// Python: import threading -> JS: Handled with async/await and boolean flags
// Python: import heapq -> JS: Implemented or using a library
// Python: import itertools -> JS: Custom implementation for `count`
const itertools = {
    count: (function*() {
        let i = 0;
        while (true) {
            yield i++;
        }
    })()
};
// Python: import decimal -> JS: Using standard Number
// Python: from datetime import datetime, timedelta -> JS: Using standard Date
// Python: from typing import ... -> JS: Using JSDoc for type hints
// Python: from typing import cast -> JS: No-op cast function
const cast = (type, value) => value;

// Type definitions
/** @typedef {Object.<string, any | null>} StateDictionary */

// Callback types
/** @typedef {(action: Action, state: StateDictionary) => number} CostCallback */
/** @typedef {(agent: Agent, action: Action) => ExecutionStatus} ExecutorCallback */
/** @typedef {(state: StateDictionary) => Array<any>} PermutationSelectorCallback */
/** @typedef {(agent: Agent) => void} SensorRunCallback */
/** @typedef {(action: Action, state: StateDictionary) => boolean} StateCheckerCallback */
/** @typedef {(action: Action | null, stateKey: string) => number} StateCostDeltaMultiplierCallback */
/** @typedef {(action: Action, state: StateDictionary) => void} StateMutatorCallback */

// Event types
/** @typedef {(agent: Agent) => void} AgentActionSequenceCompletedEvent */
/** @typedef {(agent: Agent) => void} AgentStepEvent */
/** @typedef {(agent: Agent, action: Action, params: Object.<string, any>) => void} BeginExecuteActionEvent */
/** @typedef {(node: any, nodes: Map<any, any>) => void} EvaluatedActionNodeEvent */
/** @typedef {(agent: Agent, action: Action, status: ExecutionStatus, params: Object.<string, any>) => void} FinishExecuteActionEvent */
/** @typedef {(agent: Agent, plan: Array<Action>) => void} PlanUpdatedEvent */
/** @typedef {(agent: Agent, goal: BaseGoal | null, utility: number) => void} PlanningFinishedEvent */
/** @typedef {(agent: Agent, goal: BaseGoal, utility: number) => void} PlanningFinishedForSingleGoalEvent */
/** @typedef {(agent: Agent) => void} PlanningStartedEvent */
/** @typedef {(agent: Agent, goal: BaseGoal) => void} PlanningStartedForSingleGoalEvent */
/** @typedef {(agent: Agent, sensor: Sensor) => void} SensorRunEvent */

// Type variables (conceptual)
// T = TypeVar("T", bound="PriorityQueueNode")

// Constants
const MaxX = 20;
const MaxY = 20;
const CELL_SIZE = 30;
const WIDTH = 20 * CELL_SIZE;
const HEIGHT = 20 * CELL_SIZE;
const BLACK = [0, 0, 0];
const WHITE = [255, 255, 255];
const GREEN = [0, 255, 0];
const RED = [255, 0, 0];
const YELLOW = [255, 255, 0];
const BLUE = [0, 0, 255];



// === ENUMS ===
const StepMode = Object.freeze({
    Default: 1,
    OneAction: 2,
    AllActions: 3,
});

const ComparisonOperator = Object.freeze({
    Undefined: 0,
    Equals: 1,
    LessThan: 2,
    LessThanOrEquals: 3,
    GreaterThan: 4,
    GreaterThanOrEquals: 5,
});

const ExecutionStatus = Object.freeze({
    NotYetExecuted: 1,
    Executing: 2,
    Succeeded: 3,
    Failed: 4,
    NotPossible: 5,
});

// === VALUE CLASSES ===
class ComparisonValuePair {
    Value = null;
    Operator = ComparisonOperator.Undefined;

    constructor(
        value = null,
        operator = ComparisonOperator.Undefined,
    ) {
        this.Value = value;
        this.Operator = operator;
    }
}

class Vector2 {
    constructor(x, y) {
        this.X = x;
        this.Y = y;
    }

    equals(other) {
        if (!(other instanceof Vector2)) {
            return false;
        }
        return this.X === other.X && this.Y === other.Y;
    }

    getHash() {
        return `Vector2(${this.X},${this.Y})`;
    }

    toString() {
        return `Vector2(${this.X}, ${this.Y})`;
    }
}

// === GOAL CLASSES ===
class BaseGoal {
    Name;
    Weight;

    constructor(name = null, weight = 1.0) {
        this.Name = name !== null ? name : `Goal ${uuidv4()}`;
        this.Weight = weight;
    }
}

class Goal extends BaseGoal {
    DesiredState;

    constructor(
        name = null,
        weight = 1.0,
        desired_state = null,
    ) {
        super(name, weight);
        this.DesiredState = desired_state !== null ? desired_state : {};
    }
}

class ComparativeGoal extends BaseGoal {
    DesiredState;

    constructor(
        name = null,
        weight = 1.0,
        desired_state = null,
    ) {
        super(name, weight);
        this.DesiredState = desired_state !== null ? desired_state : {};
    }
}

class ExtremeGoal extends BaseGoal {
    DesiredState;

    constructor(
        name = null,
        weight = 1.0,
        desired_state = null,
    ) {
        super(name, weight);
        this.DesiredState = desired_state !== null ? desired_state : {};
    }
}

// === UTILITY CLASSES ===
class DictionaryExtensionMethods {
    static copy_dict(dictionary) {
        return { ...dictionary };
    }

    static copy_concurrent_dict(dictionary) {
        return { ...dictionary };
    }

    static copy_comparison_value_pair_dict(
        dictionary,
    ) {
        return { ...dictionary };
    }

    static copy_string_dict(dictionary) {
        return { ...dictionary };
    }

    static copy_non_nullable_dict(dictionary) {
        return { ...dictionary };
    }
}

class Utils {
    static is_lower_than(a, b) {
        if (a === null || b === null) {
            return false;
        }
        if (typeof a === 'number' && typeof b === 'number') {
            return a < b;
        }
        if (a instanceof Date && b instanceof Date) {
            return a < b;
        }
        return false;
    }

    static is_higher_than(a, b) {
        if (a === null || b === null) {
            return false;
        }
        if (typeof a === 'number' && typeof b === 'number') {
            return a > b;
        }
        if (a instanceof Date && b instanceof Date) {
            return a > b;
        }
        return false;
    }

    static is_lower_than_or_equals(a, b) {
        if (a === null || b === null) {
            return false;
        }
        if (typeof a === 'number' && typeof b === 'number') {
            return a <= b;
        }
        if (a instanceof Date && b instanceof Date) {
            return a <= b;
        }
        return false;
    }

    static is_higher_than_or_equals(a, b) {
        if (a === null || b === null) {
            return false;
        }
        if (typeof a === 'number' && typeof b === 'number') {
            return a >= b;
        }
        if (a instanceof Date && b instanceof Date) {
            return a >= b;
        }
        return false;
    }

    static meets_goal(goal, action_node, current) {
        if (goal instanceof Goal) {
            for (const key in goal.DesiredState) {
                const desired_value = goal.DesiredState[key];
                if (!(key in action_node.State)) {
                    return false;
                }
                const current_value = action_node.State[key];
                if (current_value === null && desired_value !== null) {
                    return false;
                } else if (current_value !== null && current_value != desired_value) {
                    return false;
                }
            }
            return true;
        } else if (goal instanceof ExtremeGoal) {
            if (action_node.Action === null) {
                return false;
            }
            for (const key in goal.DesiredState) {
                const maximize = goal.DesiredState[key];
                if (!(key in action_node.State) || !(key in current.State)) {
                    return false;
                }
                const current_value = action_node.State[key];
                const previous_value = current.State[key];
                if (current_value !== null && previous_value !== null) {
                    if (maximize) {
                        if (!Utils.is_higher_than_or_equals(current_value, previous_value)) {
                            return false;
                        }
                    } else {
                        if (!Utils.is_lower_than_or_equals(current_value, previous_value)) {
                            return false;
                        }
                    }
                }
            }
            return true;
        } else if (goal instanceof ComparativeGoal) {
            for (const key in goal.DesiredState) {
                const comparison_value_pair = goal.DesiredState[key];
                if (!(key in action_node.State)) {
                    return false;
                }
                if (!(key in current.State)) {
                    return false;
                }
                const current_value = action_node.State[key];
                const desired_value = comparison_value_pair.Value;
                const operator = comparison_value_pair.Operator;
                if (operator === ComparisonOperator.Undefined) {
                    return false;
                }
                if (operator === ComparisonOperator.Equals) {
                    if (current_value != desired_value) {
                        return false;
                    }
                } else if (operator === ComparisonOperator.LessThan) {
                    if (current_value === null || desired_value === null) {
                        return false;
                    }
                    if (!Utils.is_lower_than(current_value, desired_value)) {
                        return false;
                    }
                } else if (operator === ComparisonOperator.GreaterThan) {
                    if (current_value === null || desired_value === null) {
                        return false;
                    }
                    if (!Utils.is_higher_than(current_value, desired_value)) {
                        return false;
                    }
                } else if (operator === ComparisonOperator.LessThanOrEquals) {
                    if (current_value === null || desired_value === null) {
                        return false;
                    }
                    if (!Utils.is_lower_than_or_equals(current_value, desired_value)) {
                        return false;
                    }
                } else if (operator === ComparisonOperator.GreaterThanOrEquals) {
                    if (current_value === null || desired_value === null) {
                        return false;
                    }
                    if (!Utils.is_higher_than_or_equals(current_value, desired_value)) {
                        return false;
                    }
                }
            }
            return true;
        }
        return false;
    }
}

class PermutationSelectorGenerators {
    static select_from_collection(values) {
        return function selector(state) {
            const output = [];
            for (const item of values) {
                if (item !== null) {
                    output.push(item);
                }
            }
            return output;
        };
    }

    static select_from_collection_in_state(key) {
        return function selector(state) {
            const output = [];
            if (key in state && Array.isArray(state[key])) {
                const values = state[key];
                for (const item of values) {
                    if (item !== null) {
                        output.push(item);
                    }
                }
            }
            return output;
        };
    }

    static select_from_integer_range(lower_bound, upper_bound) {
        return function selector(state) {
            const output = [];
            for (let i = lower_bound; i < upper_bound; i++) {
                output.push(i);
            }
            return output;
        };
    }
}

// === PRIORITY QUEUE CLASSES ===
class PriorityQueueNode {
    Priority = 0.0;
    QueueIndex = 0;

    constructor() {
        this.Priority = 0.0;
        this.QueueIndex = 0;
    }
}

// This is a simplified PQ based on a library, as the original Python one is complex.
// The key feature needed by A* is efficient update/re-prioritization, which is hard.
// The library version doesn't support updates, so we re-enqueue. This is less efficient
// but works for this port. The original Python code is more complex and efficient.
// For the verbatim port, the original heapq based class is implemented below.
class PriorityQueue {
    _heap = []; // Min-heap of [priority, count, item]
    _entry_finder = new Map(); // Maps item to entry in heap
    _counter = 0;
    _REMOVED = '<removed>';

    constructor(initial_capacity = 0) {
        // Capacity is not used in this JS implementation
    }

    enqueue(item, priority) {
        const itemHash = item.getHash();
        if (this._entry_finder.has(itemHash)) {
            this._entry_finder.get(itemHash)[2] = this._REMOVED;
        }
        const entry = [priority, this._counter++, item];
        this._entry_finder.set(itemHash, entry);
        this._heap.push(entry);
        this._siftUp(this._heap.length - 1);
    }

    dequeue() {
        while (this._heap.length > 0) {
            const entry = this._heap[0];
            const item = entry[2];
            if (this._heap.length === 1) {
                this._heap.pop();
            } else {
                this._heap[0] = this._heap.pop();
                this._siftDown(0);
            }

            if (item !== this._REMOVED) {
                this._entry_finder.delete(item.getHash());
                return item;
            }
        }
        throw new Error("Cannot dequeue from an empty priority queue.");
    }
    
    _siftUp(i) {
        let parent = Math.floor((i - 1) / 2);
        while (i > 0 && this._heap[i][0] < this._heap[parent][0]) {
            [this._heap[i], this._heap[parent]] = [this._heap[parent], this._heap[i]];
            i = parent;
            parent = Math.floor((i - 1) / 2);
        }
    }

    _siftDown(i) {
        let minIndex = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;
        if (left < this._heap.length && this._heap[left][0] < this._heap[minIndex][0]) {
            minIndex = left;
        }
        if (right < this._heap.length && this._heap[right][0] < this._heap[minIndex][0]) {
            minIndex = right;
        }
        if (i !== minIndex) {
            [this._heap[i], this._heap[minIndex]] = [this._heap[minIndex], this._heap[i]];
            this._siftDown(minIndex);
        }
    }

    update_priority(item, new_priority) {
        this.enqueue(item, new_priority);
    }

    contains(item) {
        const hash = item.getHash();
        return this._entry_finder.has(hash) && this._entry_finder.get(hash)[2] !== this._REMOVED;
    }

    get count() {
        // This is an approximation, as removed items are still in heap
        return this._entry_finder.size;
    }
}


class FastPriorityQueueNode {
    Priority = 0.0;
    QueueIndex = 0;

    constructor() {
        this.Priority = 0.0;
        this.QueueIndex = 0;
    }
}

class FastPriorityQueue {
    _num_nodes;
    _nodes;

    constructor(max_nodes) {
        if (max_nodes <= 0) {
            throw new Error("New queue size cannot be smaller than 1");
        }
        this._num_nodes = 0;
        this._nodes = new Array(max_nodes + 1).fill(null);
    }

    get count() {
        return this._num_nodes;
    }

    get max_size() {
        return this._nodes.length - 1;
    }

    clear() {
        for (let i = 1; i <= this._num_nodes; i++) {
            const node_to_clear = this._nodes[i];
            if (node_to_clear !== null) {
                node_to_clear.QueueIndex = 0;
            }
            this._nodes[i] = null;
        }
        this._num_nodes = 0;
    }

    contains(node) {
        if (node === null) {
            throw new Error("node cannot be null");
        }
        return (
            node.QueueIndex > 0 &&
            node.QueueIndex <= this._num_nodes &&
            this._nodes[node.QueueIndex] === node
        );
    }

    enqueue(node, priority) {
        if (node === null) {
            throw new Error("node cannot be null");
        }
        if (this._num_nodes >= this.max_size) {
            throw new Error("Queue is full - node cannot be added");
        }
        node.Priority = priority;
        this._num_nodes += 1;
        node.QueueIndex = this._num_nodes;
        this._nodes[this._num_nodes] = node;
        this._cascade_up(node);
    }

    _cascade_up(node) {
        let current_index = node.QueueIndex;
        while (current_index > 1) {
            const parent_index = Math.floor(current_index / 2);
            const parent_node = this._nodes[parent_index];
            if (this._has_higher_or_equal_priority(parent_node, node)) {
                break;
            }
            this._nodes[current_index] = parent_node;
            if (parent_node !== null) {
                parent_node.QueueIndex = current_index;
            }
            this._nodes[parent_index] = node;
            node.QueueIndex = parent_index;
            current_index = parent_index;
        }
    }

    _cascade_down(node) {
        let current_index = node.QueueIndex;
        while (true) {
            const child_left_index = 2 * current_index;
            const child_right_index = 2 * current_index + 1;
            let swap_index = 0;
            if (child_left_index <= this._num_nodes) {
                const child_left = this._nodes[child_left_index];
                if (this._has_higher_priority(child_left, node)) {
                    swap_index = child_left_index;
                }
            }
            if (child_right_index <= this._num_nodes) {
                const child_right = this._nodes[child_right_index];
                if (swap_index === 0) {
                    if (this._has_higher_priority(child_right, node)) {
                        swap_index = child_right_index;
                    }
                } else {
                    const child_to_compare = this._nodes[swap_index];
                    if (this._has_higher_priority(child_right, child_to_compare)) {
                        swap_index = child_right_index;
                    }
                }
            }
            if (swap_index === 0) {
                break;
            }
            const swap_node = this._nodes[swap_index];
            this._nodes[current_index] = swap_node;
            if (swap_node !== null) {
                swap_node.QueueIndex = current_index;
            }
            this._nodes[swap_index] = node;
            node.QueueIndex = swap_index;
            current_index = swap_index;
        }
    }

    _has_higher_priority(higher, lower) {
        return higher.Priority < lower.Priority;
    }

    _has_higher_or_equal_priority(higher, lower) {
        return higher.Priority <= lower.Priority;
    }

    dequeue() {
        if (this._num_nodes <= 0) {
            throw new Error("Cannot call dequeue() on an empty queue");
        }
        const return_me = this._nodes[1];
        if (return_me === null) {
            throw new Error("Heap root is unexpectedly null");
        }
        if (this._num_nodes === 1) {
            this._nodes[1] = null;
            this._num_nodes = 0;
            return_me.QueueIndex = 0;
            return return_me;
        }
        const former_last_node = this._nodes[this._num_nodes];
        if (former_last_node === null) {
            throw new Error("Last node is unexpectedly null");
        }
        this._nodes[1] = former_last_node;
        former_last_node.QueueIndex = 1;
        this._nodes[this._num_nodes] = null;
        this._num_nodes -= 1;
        return_me.QueueIndex = 0;
        this._cascade_down(former_last_node);
        return return_me;
    }

    resize(max_nodes) {
        if (max_nodes <= 0) {
            throw new Error("Queue size cannot be smaller than 1");
        }
        if (max_nodes < this._num_nodes) {
            throw new Error(
                `Called Resize(${max_nodes}), but current queue contains ${this._num_nodes} nodes`
            );
        }
        const new_nodes = new Array(max_nodes + 1).fill(null);
        for (let i = 1; i <= this._num_nodes; i++) {
            new_nodes[i] = this._nodes[i];
        }
        this._nodes = new_nodes;
    }

    get first() {
        if (this._num_nodes <= 0) {
            throw new Error("Cannot call .first on an empty queue");
        }
        if (this._nodes[1] === null) {
            throw new Error("First element in heap is unexpectedly null");
        }
        return this._nodes[1];
    }

    update_priority(node, priority) {
        if (node === null) {
            throw new Error("node cannot be null");
        }
        const old_priority = node.Priority;
        node.Priority = priority;
        this._on_node_updated(node);
    }

    _on_node_updated(node) {
        const parent_index = Math.floor(node.QueueIndex / 2);
        if (parent_index > 0 && this._has_higher_priority(node, this._nodes[parent_index])) {
            this._cascade_up(node);
        } else {
            this._cascade_down(node);
        }
    }

    remove(node) {
        if (node === null) {
            throw new Error("node cannot be null");
        }
        if (node.QueueIndex === this._num_nodes) {
            this._nodes[this._num_nodes] = null;
            this._num_nodes -= 1;
            node.QueueIndex = 0;
            return;
        }
        const former_last_node = this._nodes[this._num_nodes];
        if (former_last_node === null) {
            throw new Error(
                "Last node in heap is unexpectedly null during remove operation"
            );
        }
        const old_priority_of_former_last_node = former_last_node.Priority;
        this._nodes[node.QueueIndex] = former_last_node;
        former_last_node.QueueIndex = node.QueueIndex;
        this._nodes[this._num_nodes] = null;
        this._num_nodes -= 1;
        node.QueueIndex = 0;
        this._on_node_updated(former_last_node);
    }

    reset_node(node) {
        if (node === null) {
            throw new Error("node cannot be null");
        }
        node.QueueIndex = 0;
    }

    [Symbol.iterator]() {
        const active_nodes = [];
        for (let i = 1; i <= this._num_nodes; i++) {
            const node = this._nodes[i];
            if (node !== null) {
                active_nodes.push(node);
            }
        }
        return active_nodes[Symbol.iterator]();
    }

    is_valid_queue() {
        for (let i = 1; i <= this._num_nodes; i++) {
            const current_node = this._nodes[i];
            if (current_node === null) {
                return false;
            }
            if (current_node.QueueIndex !== i) {
                return false;
            }
            const child_left_index = 2 * i;
            if (child_left_index <= this._num_nodes) {
                const child_left = this._nodes[child_left_index];
                if (child_left === null || this._has_higher_priority(
                    child_left, current_node
                )) {
                    return false;
                }
            }
            const child_right_index = 2 * i + 1;
            if (child_right_index <= this._num_nodes) {
                const child_right = this._nodes[child_right_index];
                if (child_right === null || this._has_higher_priority(
                    child_right, current_node
                )) {
                    return false;
                }
            }
        }
        return true;
    }
}

// === CORE GOAP CLASSES ===
class Action {
    Name;
    _cost_base;
    _permutation_selectors;
    _executor;
    _cost_callback;
    _preconditions;
    _comparative_preconditions;
    _postconditions;
    _arithmetic_postconditions;
    _parameter_postconditions;
    _state_mutator;
    _state_checker;
    _parameters;
    StateCostDeltaMultiplier;
    ExecutionStatus = ExecutionStatus.NotYetExecuted;

    constructor(
        {
            name = null,
            permutation_selectors = null,
            executor = null,
            cost = 1.0,
            cost_callback = null,
            preconditions = null,
            comparative_preconditions = null,
            postconditions = null,
            arithmetic_postconditions = null,
            parameter_postconditions = null,
            state_mutator = null,
            state_checker = null,
            state_cost_delta_multiplier = null
        } = {}
    ) {
        this._permutation_selectors = permutation_selectors !== null ? permutation_selectors : {};
        this._executor = executor !== null ? executor : Action._default_executor_callback;
        const executor_name = this._executor.name || String(this._executor);
        this.Name = name !== null ? name : `Action ${uuidv4()} (${executor_name})`;
        this._cost_base = cost;
        this._cost_callback = cost_callback !== null ? cost_callback : Action._default_cost_callback;
        this._preconditions = preconditions !== null ? preconditions : {};
        this._comparative_preconditions = comparative_preconditions !== null ? comparative_preconditions : {};
        this._postconditions = postconditions !== null ? postconditions : {};
        this._arithmetic_postconditions = arithmetic_postconditions !== null ? arithmetic_postconditions : {};
        this._parameter_postconditions = parameter_postconditions !== null ? parameter_postconditions : {};
        this._state_mutator = state_mutator;
        this._state_checker = state_checker;
        this.StateCostDeltaMultiplier = state_cost_delta_multiplier !== null ? state_cost_delta_multiplier : Action.default_state_cost_delta_multiplier;
        this._parameters = {};
    }

    static _on_begin_execute_action_handlers = [];
    static _on_finish_execute_action_handlers = [];

    static OnBeginExecuteAction(agent, action, parameters) {
        for (const handler of this._on_begin_execute_action_handlers) {
            handler(agent, action, parameters);
        }
    }

    static OnFinishExecuteAction(agent, action, status, parameters) {
        for (const handler of this._on_finish_execute_action_handlers) {
            handler(agent, action, status, parameters);
        }
    }

    static register_on_begin_execute_action(handler) {
        this._on_begin_execute_action_handlers.push(handler);
    }

    static register_on_finish_execute_action(handler) {
        this._on_finish_execute_action_handlers.push(handler);
    }

    static default_state_cost_delta_multiplier(action, state_key) {
        return 1.0;
    }

    static _default_executor_callback(agent, action) {
        return ExecutionStatus.Failed;
    }

    static _default_cost_callback(action, current_state) {
        return action._cost_base;
    }

    copy() {
        const new_action = new Action({
            name: this.Name,
            permutation_selectors: this._permutation_selectors,
            executor: this._executor,
            cost: this._cost_base,
            cost_callback: this._cost_callback,
            preconditions: DictionaryExtensionMethods.copy_dict(this._preconditions),
            comparative_preconditions: DictionaryExtensionMethods.copy_comparison_value_pair_dict(
                this._comparative_preconditions
            ),
            postconditions: DictionaryExtensionMethods.copy_dict(this._postconditions),
            arithmetic_postconditions: DictionaryExtensionMethods.copy_non_nullable_dict(
                this._arithmetic_postconditions
            ),
            parameter_postconditions: DictionaryExtensionMethods.copy_string_dict(
                this._parameter_postconditions
            ),
            state_mutator: this._state_mutator,
            state_checker: this._state_checker,
            state_cost_delta_multiplier: this.StateCostDeltaMultiplier,
        });
        new_action._parameters = DictionaryExtensionMethods.copy_dict(this._parameters);
        return new_action;
    }

    set_parameter(key, value) {
        this._parameters[key] = value;
    }

    get_parameter(key) {
        return this._parameters[key];
    }

    get_cost(current_state) {
        try {
            return this._cost_callback(this, current_state);
        } catch (e) {
            return Infinity;
        }
    }

    execute(agent) {
        Action.OnBeginExecuteAction(agent, this, this._parameters);
        if (this.is_possible(agent.State)) {
            const new_status = this._executor(agent, this);
            if (new_status === ExecutionStatus.Succeeded) {
                this.apply_effects(agent.State);
            }
            this.ExecutionStatus = new_status;
            Action.OnFinishExecuteAction(
                agent, this, this.ExecutionStatus, this._parameters
            );
            return new_status;
        } else {
            this.ExecutionStatus = ExecutionStatus.NotPossible;
            Action.OnFinishExecuteAction(
                agent, this, this.ExecutionStatus, this._parameters
            );
            return ExecutionStatus.NotPossible;
        }
    }

    is_possible(state) {
        for (const key in this._preconditions) {
            const value = this._preconditions[key];
            if (!(key in state)) {
                return false;
            }

            const current_value = state[key];

            if (current_value === null) {
                if (value !== null) {
                    return false;
                }
            } else {
                if (current_value != value) {
                    return false;
                }
            }
        }
        for (const key in this._comparative_preconditions) {
            const comp_value_pair = this._comparative_preconditions[key];
            if (!(key in state)) {
                return false;
            }

            const current_val = state[key];
            const desired_val = comp_value_pair.Value;
            const operator = comp_value_pair.Operator;

            if (operator === ComparisonOperator.Undefined) {
                return false;
            }

            if (operator === ComparisonOperator.Equals) {
                if (current_val != desired_val) {
                    return false;
                }
            } else if (current_val === null || desired_val === null) {
                return false;
            } else {
                if (operator === ComparisonOperator.LessThan) {
                    if (!Utils.is_lower_than(current_val, desired_val)) return false;
                } else if (operator === ComparisonOperator.GreaterThan) {
                    if (!Utils.is_higher_than(current_val, desired_val)) return false;
                } else if (operator === ComparisonOperator.LessThanOrEquals) {
                    if (!Utils.is_lower_than_or_equals(current_val, desired_val)) return false;
                } else if (operator === ComparisonOperator.GreaterThanOrEquals) {
                    if (!Utils.is_higher_than_or_equals(current_val, desired_val)) return false;
                }
            }
        }
        if (this._state_checker !== null && !this._state_checker(this, state)) {
            return false;
        }
        return true;
    }

    get_permutations(state) {
        if (Object.keys(this._permutation_selectors).length === 0) {
            return [{}];
        }

        const combined_outputs = [];
        const outputs = {};
        for (const key in this._permutation_selectors) {
            const selector_callback = this._permutation_selectors[key];
            outputs[key] = selector_callback(state);
            if (outputs[key].length === 0) {
                return [];
            }
        }
        const permutation_parameters = Object.keys(outputs);
        const indices = new Array(permutation_parameters.length).fill(0);
        const counts = permutation_parameters.map(param => outputs[param].length);
        while (true) {
            const single_output = {};
            for (let i = 0; i < indices.length; i++) {
                if (indices[i] >= counts[i]) {
                    continue;
                }
                const param_key = permutation_parameters[i];
                single_output[param_key] = outputs[param_key][indices[i]];
            }
            combined_outputs.push(single_output);
            if (Action._indices_at_maximum(indices, counts)) {
                return combined_outputs;
            }
            Action._increment_indices(indices, counts);
        }
    }

    apply_effects(state) {
        for (const key in this._postconditions) {
            state[key] = this._postconditions[key];
        }
        for (const key in this._arithmetic_postconditions) {
            const value_to_add = this._arithmetic_postconditions[key];
            if (!(key in state)) {
                continue;
            }
            const current_value = state[key];
            if (typeof current_value === 'number' && typeof value_to_add === 'number') {
                state[key] = current_value + value_to_add;
            } else if (current_value instanceof Date && typeof value_to_add === 'number') { // JS timedelta is just ms number
                state[key] = new Date(current_value.getTime() + value_to_add);
            } else {
                try {
                    state[key] = current_value + value_to_add;
                } catch (e) {
                    // pass
                }
            }
        }
        for (const param_key in this._parameter_postconditions) {
            const state_key = this._parameter_postconditions[param_key];
            if (!(param_key in this._parameters)) {
                continue;
            }
            state[state_key] = this._parameters[param_key];
        }
        if (this._state_mutator !== null) {
            this._state_mutator(this, state);
        }
    }

    set_parameters(parameters) {
        this._parameters = parameters;
    }

    static _indices_at_maximum(indices, counts) {
        for (let i = 0; i < indices.length; i++) {
            if (indices[i] < counts[i] - 1) {
                return false;
            }
        }
        return true;
    }

    static _increment_indices(indices, counts) {
        if (Action._indices_at_maximum(indices, counts)) {
            return;
        }
        for (let i = 0; i < indices.length; i++) {
            if (indices[i] === counts[i] - 1) {
                indices[i] = 0;
            } else {
                indices[i] += 1;
                return;
            }
        }
    }

    getHash() {
        return this.Name;
    }

    equals(other) {
        if (!(other instanceof Action)) {
            return false;
        }
        return this.Name === other.Name;
    }
}

class Sensor {
    Name;
    _run_callback;
    static _on_sensor_run_handlers = [];

    static OnSensorRun(agent, sensor) {
        for (const handler of this._on_sensor_run_handlers) {
            handler(agent, sensor);
        }
    }

    static register_on_sensor_run(handler) {
        this._on_sensor_run_handlers.push(handler);
    }

    constructor(run_callback, name = null) {
        const callback_name = run_callback.name || String(run_callback);
        this.Name = name !== null ? name : `Sensor ${uuidv4()} (${callback_name})`;
        this._run_callback = run_callback;
    }

    run(agent) {
        Sensor.OnSensorRun(agent, this);
        this._run_callback(agent);
    }
}

class Agent {
    Name;
    CurrentActionSequences;
    State;
    Memory;
    Goals;
    Actions;
    Sensors;
    CostMaximum;
    StepMaximum;
    static _on_agent_step_handlers = [];
    static _on_agent_action_sequence_completed_handlers = [];
    static _on_planning_started_handlers = [];
    static _on_planning_started_for_single_goal_handlers = [];
    static _on_planning_finished_for_single_goal_handlers = [];
    static _on_planning_finished_handlers = [];
    static _on_plan_updated_handlers = [];
    static _on_evaluated_action_node_handlers = [];

    static OnAgentStep(agent) {
        for (const handler of this._on_agent_step_handlers) {
            handler(agent);
        }
    }

    static OnAgentActionSequenceCompleted(agent) {
        for (const handler of this._on_agent_action_sequence_completed_handlers) {
            handler(agent);
        }
    }

    static OnPlanningStarted(agent) {
        for (const handler of this._on_planning_started_handlers) {
            handler(agent);
        }
    }

    static OnPlanningStartedForSingleGoal(agent, goal) {
        for (const handler of this._on_planning_started_for_single_goal_handlers) {
            handler(agent, goal);
        }
    }

    static OnPlanningFinishedForSingleGoal(agent, goal, utility) {
        for (const handler of this._on_planning_finished_for_single_goal_handlers) {
            handler(agent, goal, utility);
        }
    }

    static OnPlanningFinished(agent, goal, utility) {
        for (const handler of this._on_planning_finished_handlers) {
            handler(agent, goal, utility);
        }
    }

    static OnPlanUpdated(agent, action_list) {
        for (const handler of this._on_plan_updated_handlers) {
            handler(agent, action_list);
        }
    }

    static OnEvaluatedActionNode(node, nodes) {
        for (const handler of this._on_evaluated_action_node_handlers) {
            handler(node, nodes);
        }
    }

    static register_on_agent_step(handler) {
        this._on_agent_step_handlers.push(handler);
    }

    static register_on_agent_action_sequence_completed(handler) {
        this._on_agent_action_sequence_completed_handlers.push(handler);
    }

    static register_on_planning_started(handler) {
        this._on_planning_started_handlers.push(handler);
    }

    static register_on_planning_started_for_single_goal(handler) {
        this._on_planning_started_for_single_goal_handlers.push(handler);
    }

    static register_on_planning_finished_for_single_goal(handler) {
        this._on_planning_finished_for_single_goal_handlers.push(handler);
    }

    static register_on_planning_finished(handler) {
        this._on_planning_finished_handlers.push(handler);
    }

    static register_on_plan_updated(handler) {
        this._on_plan_updated_handlers.push(handler);
    }

    static register_on_evaluated_action_node(handler) {
        this._on_evaluated_action_node_handlers.push(handler);
    }

    constructor(
        {
            name = null,
            state = null,
            memory = null,
            goals = null,
            actions = null,
            sensors = null,
            cost_maximum = Infinity,
            step_maximum = Infinity
        } = {}
    ) {
        // this._lock is not needed in single-threaded JS
        this.Name = name !== null ? name : `Agent ${uuidv4()}`;
        this.State = state !== null ? state : {};
        this.Memory = memory !== null ? memory : {};
        this.Goals = goals !== null ? goals : [];
        this.Actions = actions !== null ? actions : [];
        this.Sensors = sensors !== null ? sensors : [];
        this.CostMaximum = cost_maximum;
        this.StepMaximum = step_maximum;
        this.CurrentActionSequences = [];
        this.IsBusy = false;
        this.IsPlanning = false;
    }

    step(mode = StepMode.Default) {
        Agent.OnAgentStep(this);
        for (const sensor of this.Sensors) {
            sensor.run(this);
        }
        if (mode === StepMode.Default) {
            this._step_async();
            return;
        }
        if (!this.IsBusy) {
            Planner.plan(this, this.CostMaximum, this.StepMaximum);
        }
        if (mode === StepMode.OneAction) {
            this._execute();
        } else if (mode === StepMode.AllActions) {
            while (this.IsBusy) {
                this._execute();
            }
        }
    }

    clear_plan() {
        this.CurrentActionSequences = [];
    }

    plan() {
        if (!this.IsBusy && !this.IsPlanning) {
            this.IsPlanning = true;
            Planner.plan(this, this.CostMaximum, this.StepMaximum);
        }
    }

    plan_async() {
        if (!this.IsBusy && !this.IsPlanning) {
            this.IsPlanning = true;
            // Simulate async with setTimeout
            setTimeout(() => {
                Planner.plan(this, this.CostMaximum, this.StepMaximum);
            }, 0);
        }
    }

    execute_plan() {
        if (!this.IsPlanning) {
            this._execute();
        }
    }

    _step_async() {
        if (!this.IsBusy && !this.IsPlanning) {
            this.IsPlanning = true;
            setTimeout(() => {
                Planner.plan(this, this.CostMaximum, this.StepMaximum);
            }, 0);
        } else if (!this.IsPlanning) {
            this._execute();
        }
    }

    _execute() {
        if (this.CurrentActionSequences.length > 0) {
            const cullable_sequences = [];
            for (const sequence of this.CurrentActionSequences) {
                if (sequence.length > 0) {
                    const action_to_execute = sequence[0];
                    console.log(`${this.Name} executing action: ${action_to_execute.Name}`);
                    const execution_status = action_to_execute.execute(this);
                    if (execution_status !== ExecutionStatus.Executing) {
                        sequence.shift();
                    }
                    if (sequence.length === 0) {
                        cullable_sequences.push(sequence);
                    }
                } else {
                    cullable_sequences.push(sequence);
                }
            }
            for (const sequence of cullable_sequences) {
                const index = this.CurrentActionSequences.indexOf(sequence);
                if (index > -1) {
                    this.CurrentActionSequences.splice(index, 1);
                }
                Agent.OnAgentActionSequenceCompleted(this);
            }
            if (this.CurrentActionSequences.length === 0) {
                this.IsBusy = false;
            }
        } else {
            console.log(`DEBUG: ${this.Name} has no action sequences to execute`);
            this.IsBusy = false;
        }
    }
}

// === PLANNING CLASSES ===
class ActionNode extends PriorityQueueNode {
    State;
    Parameters;
    Action;
    _hash = null; // Cache for the hash

    constructor(action, state, parameters) {
        super();
        this.Action = action !== null ? action.copy() : null;
        this.State = DictionaryExtensionMethods.copy_concurrent_dict(state);
        this.Parameters = DictionaryExtensionMethods.copy_dict(parameters);
        if (this.Action !== null) {
            this.Action.set_parameters(this.Parameters);
        }
    }

    equals(other) {
        if (!(other instanceof ActionNode)) {
            return false;
        }
        if (this === other) {
            return true;
        }
        if (this.Action === null) {
            if (other.Action !== null) {
                return false;
            }
        } else if (other.Action === null) {
            return false;
        } else if (!this.Action.equals(other.Action)) {
            return false;
        }
        return this._state_matches(other);
    }

    // JS doesn't have a direct __ne__ equivalent that's auto-used.
    // not_equals(other) {
    //     return !this.equals(other);
    // }

    _makeValueHashable(obj) {
        if (obj === null || typeof obj === 'undefined') return 'null';
        if (typeof obj !== 'object') {
             // Differentiate between string and number for hashing
             return `${typeof obj}:${String(obj)}`;
        }

        if (obj.getHash && typeof obj.getHash === 'function') {
            return obj.getHash();
        }

        if (Array.isArray(obj)) {
            const arrParts = obj.map(item => this._makeValueHashable(item));
            return `[${arrParts.join(',')}]`;
        }
        
        // Plain object
        try {
            const sortedKeys = Object.keys(obj).sort();
            const objParts = sortedKeys.map(key => {
                const valHash = this._makeValueHashable(obj[key]);
                return `${key}:${valHash}`;
            });
            return `{${objParts.join(',')}}`;
        } catch (e) {
            return null; // Unhashable
        }
    }

    getHash() {
        if (this._hash !== null) return this._hash;
        
        const actionHash = this.Action ? this.Action.getHash() : 'null_action';
        
        const hashableItems = [];
        const sortedKeys = Object.keys(this.State).sort();

        for (const key of sortedKeys) {
            const value = this.State[key];
            const hashableValue = this._makeValueHashable(value);
            if (hashableValue !== null) {
                hashableItems.push(`${key}=${hashableValue}`);
            }
        }
        
        // The equivalent of frozenset is sorting the string representations
        const stateHash = hashableItems.join('&');
        this._hash = `${actionHash}|${stateHash}`;
        return this._hash;
    }

    cost(current_state) {
        if (this.Action === null) {
            return Infinity;
        }
        return this.Action.get_cost(current_state);
    }

    _state_matches(other_node) {
        const selfKeys = Object.keys(this.State);
        const otherKeys = Object.keys(other_node.State);

        if (selfKeys.length !== otherKeys.length) return false;

        for (const key in this.State) {
            if (!(key in other_node.State)) {
                return false;
            }
            const selfVal = this.State[key];
            const otherVal = other_node.State[key];

            if (selfVal && typeof selfVal.equals === 'function') {
                if (!selfVal.equals(otherVal)) return false;
            } else if (selfVal !== otherVal) {
                return false;
            }
        }
        return true;
    }
}

class ActionGraph {
    ActionNodes;

    constructor(actions, state) {
        this.ActionNodes = [];
        for (const action of actions) {
            const permutations = action.get_permutations(state);
            for (const permutation of permutations) {
                this.ActionNodes.push(new ActionNode(action, state, permutation));
            }
        }
    }

    *neighbors(node) {
        for (const other_node_template of this.ActionNodes) {
            if (
                other_node_template.Action !== null &&
                other_node_template.Action.is_possible(node.State)
            ) {
                const new_action = other_node_template.Action.copy();
                const new_state = DictionaryExtensionMethods.copy_concurrent_dict(node.State);
                const new_parameters = DictionaryExtensionMethods.copy_dict(
                    other_node_template.Parameters
                );
                const new_node = new ActionNode(new_action, new_state, new_parameters);
                if (new_node.Action !== null) {
                    new_node.Action.apply_effects(new_node.State);
                }
                yield new_node;
            }
        }
    }
}

class ActionAStar {
    _goal;
    FinalPoint = null;
    CostSoFar = new Map();
    StepsSoFar = new Map();
    CameFrom = new Map();

    constructor(graph, start, goal, cost_maximum, step_maximum) {
        this._goal = goal;
        
        const frontier = new PriorityQueue();
        frontier.enqueue(start, 0.0);
        
        const startHash = start.getHash();
        this.CameFrom.set(startHash, start); // Key: string hash, Value: node object
        this.CostSoFar.set(startHash, 0.0);
        this.StepsSoFar.set(startHash, 0);
        let nodes_explored = 0;

        while (frontier.count > 0) {
            const current = frontier.dequeue();
            nodes_explored++;

            if (this._meets_goal(current, this.CameFrom.get(current.getHash()))) {
                this.FinalPoint = current;
                break;
            }

            for (const next_node of graph.neighbors(current)) {
                const currentHash = current.getHash();
                const nextNodeHash = next_node.getHash();

                const action_cost = next_node.cost(current.State);
                const new_cost = this.CostSoFar.get(currentHash) + action_cost;
                const new_step_count = this.StepsSoFar.get(currentHash) + 1;
                
                if (new_cost > cost_maximum || new_step_count > step_maximum) {
                    continue;
                }
                
                if (!this.CostSoFar.has(nextNodeHash) || new_cost < this.CostSoFar.get(nextNodeHash)) {
                    this.CostSoFar.set(nextNodeHash, new_cost);
                    this.StepsSoFar.set(nextNodeHash, new_step_count);
                    const priority = new_cost + this._heuristic(next_node, goal, current);
                    
                    // The simple PQ doesn't have a real update, so we just re-enqueue.
                    // The check at the top of the loop will discard the old, more expensive entry.
                    frontier.enqueue(next_node, priority);
                    
                    this.CameFrom.set(nextNodeHash, current);
                    Agent.OnEvaluatedActionNode(next_node, this.CameFrom);
                }
            }
        }
    }
    
    _heuristic(action_node, goal, previous_node_in_path) {
        let cost = 0.0;
        if (goal instanceof Goal) {
            for (const key in goal.DesiredState) {
                const desired_value = goal.DesiredState[key];
                if (!(key in action_node.State) || action_node.State[key] != desired_value) {
                    cost += 1.0;
                }
            }
        } else if (goal instanceof ExtremeGoal) {
            for (const key in goal.DesiredState) {
                const maximize = goal.DesiredState[key];
                const value_diff_multiplier = action_node.Action ?
                    action_node.Action.StateCostDeltaMultiplier(action_node.Action, key) :
                    Action.default_state_cost_delta_multiplier(null, key);
                
                if (!(key in action_node.State) || !(key in previous_node_in_path.State)) {
                    cost += Infinity;
                    continue;
                }
                const current_val = action_node.State[key];
                const prev_val = previous_node_in_path.State[key];
                if (current_val === null || prev_val === null) {
                    cost += Infinity;
                    continue;
                }
                try {
                    const current_val_f = parseFloat(current_val);
                    const prev_val_f = parseFloat(prev_val);
                    if (isNaN(current_val_f) || isNaN(prev_val_f)) throw new Error();

                    const value_diff = current_val_f - prev_val_f;
                    if (maximize) {
                        if (Utils.is_lower_than_or_equals(current_val_f, prev_val_f)) {
                            cost += Math.abs(value_diff) * value_diff_multiplier;
                        }
                    } else { // minimize
                        if (Utils.is_higher_than_or_equals(current_val_f, prev_val_f)) {
                            cost += Math.abs(value_diff) * value_diff_multiplier;
                        }
                    }
                } catch (e) {
                    cost += Infinity;
                    continue;
                }
            }
        } else if (goal instanceof ComparativeGoal) {
            for (const key in goal.DesiredState) {
                const comp_value_pair = goal.DesiredState[key];
                const value_diff_multiplier = (action_node.Action ?
                    action_node.Action.StateCostDeltaMultiplier(action_node.Action, key) :
                    Action.default_state_cost_delta_multiplier(null, key)
                );
                
                if (!(key in action_node.State) || !(key in previous_node_in_path.State)) {
                    cost += Infinity;
                    continue;
                }
                const current_val = action_node.State[key];
                const desired_val = comp_value_pair.Value;
                const operator = comp_value_pair.Operator;
                
                if (current_val === null || desired_val === null) {
                    if (operator !== ComparisonOperator.Undefined) {
                        cost += Infinity;
                        continue;
                    }
                }

                let current_val_f = NaN, prev_val_f = NaN;
                try {
                     current_val_f = parseFloat(current_val);
                     prev_val_f = parseFloat(previous_node_in_path.State[key]);
                } catch (e) {
                    // keep as NaN
                }
                
                const value_diff_from_previous_step = Math.abs(current_val_f - prev_val_f);
                
                if (operator === ComparisonOperator.Undefined) {
                    cost += Infinity;
                } else if (operator === ComparisonOperator.Equals) {
                    if (current_val != desired_val) {
                        cost += value_diff_from_previous_step * value_diff_multiplier;
                    }
                } else if (operator === ComparisonOperator.LessThan) {
                    if (!Utils.is_lower_than(current_val, desired_val)) {
                        cost += value_diff_from_previous_step * value_diff_multiplier;
                    }
                } else if (operator === ComparisonOperator.GreaterThan) {
                    if (!Utils.is_higher_than(current_val, desired_val)) {
                        cost += value_diff_from_previous_step * value_diff_multiplier;
                    }
                } else if (operator === ComparisonOperator.LessThanOrEquals) {
                    if (!Utils.is_lower_than_or_equals(current_val, desired_val)) {
                        cost += value_diff_from_previous_step * value_diff_multiplier;
                    }
                } else if (operator === ComparisonOperator.GreaterThanOrEquals) {
                    if (!Utils.is_higher_than_or_equals(current_val, desired_val)) {
                        cost += value_diff_from_previous_step * value_diff_multiplier;
                    }
                }
            }
        }
        return cost;
    }

    _meets_goal(action_node, previous_node_in_path) {
        return Utils.meets_goal(this._goal, action_node, previous_node_in_path);
    }
}

class Planner {
    static plan(agent, cost_maximum, step_maximum) {
        Agent.OnPlanningStarted(agent);
        let best_plan_utility = 0.0;
        let best_astar = null;
        let best_goal = null;
        for (const goal of agent.Goals) {
            Agent.OnPlanningStartedForSingleGoal(agent, goal);
            const graph = new ActionGraph(agent.Actions, agent.State);
            const start_node = new ActionNode(null, agent.State, {});
            const astar_result = new ActionAStar(
                graph, start_node, goal, cost_maximum, step_maximum
            );
            const cursor = astar_result.FinalPoint;

            if (cursor !== null) {
                const cursorHash = cursor.getHash();
                const plan_cost = astar_result.CostSoFar.get(cursorHash, 0.0);

                let reported_utility = 0.0;
                if (plan_cost === 0) {
                    reported_utility = 0.0;
                } else {
                    reported_utility = goal.Weight / plan_cost;
                }
                Agent.OnPlanningFinishedForSingleGoal(
                    agent, goal, reported_utility
                );
                
                let comparison_utility = reported_utility;
                if (plan_cost === 0 && goal.Weight > 0) {
                    comparison_utility = Infinity;
                } else if (plan_cost === 0 && goal.Weight <= 0) {
                    comparison_utility = goal.Weight === 0 ? NaN : -Infinity;
                }

                if (cursor.Action !== null && comparison_utility > best_plan_utility) {
                    best_plan_utility = comparison_utility;
                    best_astar = astar_result;
                    best_goal = goal;
                }
            } else {
                Agent.OnPlanningFinishedForSingleGoal(
                    agent, goal, 0.0
                );
            }
        }

        if (best_plan_utility > 0 && best_astar !== null && best_goal !== null && best_astar.FinalPoint !== null) {
            Planner._update_agent_action_list(best_astar.FinalPoint, best_astar, agent);
            agent.IsBusy = true;
            Agent.OnPlanningFinished(agent, best_goal, best_plan_utility);
        } else {
            Agent.OnPlanningFinished(agent, null, 0.0);
        }
        agent.IsPlanning = false;
    }

    static _update_agent_action_list(start_node, astar, agent) {
        let cursor = start_node;

        const action_list = [];
        while (cursor !== null && cursor.Action !== null && astar.CameFrom.has(cursor.getHash())) {
            action_list.push(cursor.Action);
            const prev_cursor = astar.CameFrom.get(cursor.getHash());
            if(cursor === prev_cursor) break; // prevent infinite loop if start node points to itself
            cursor = prev_cursor;
        }
        action_list.reverse();
        agent.CurrentActionSequences.push(action_list);
        Agent.OnPlanUpdated(agent, action_list);
    }
}

// === APPLICATION CLASSES ===
class RpgUtils {
    static in_distance(pos1, pos2, max_distance) {
        const distance = RpgUtils._distance(pos1, pos2);
        return distance <= max_distance;
    }

    static get_enemy_in_range(source, agents, distance) {
        for (const agent of agents) {
            if (agent === source) {
                continue;
            }
            const source_pos = source.State["position"];
            const agent_pos = agent.State["position"];
            const source_faction = source.State["faction"];
            const agent_faction = agent.State["faction"];
            if (
                source_pos instanceof Vector2 &&
                agent_pos instanceof Vector2 &&
                typeof source_faction === 'string' &&
                typeof agent_faction === 'string' &&
                RpgUtils.in_distance(source_pos, agent_pos, distance) &&
                source_faction !== agent_faction
            ) {
                return agent;
            }
        }
        return null;
    }

    static move_towards_other_position(pos1, pos2) {
        const new_pos = new Vector2(pos1.X, pos1.Y);
        const x_diff = pos2.X - new_pos.X;
        const y_diff = pos2.Y - new_pos.Y;
        let x_sign = 0;
        if (x_diff > 0) x_sign = 1;
        else if (x_diff < 0) x_sign = -1;
        let y_sign = 0;
        if (y_diff > 0) y_sign = 1;
        else if (y_diff < 0) y_sign = -1;
        
        if (x_sign !== 0) {
            new_pos.X += x_sign;
        } else if (y_sign !== 0) {
            new_pos.Y += y_sign;
        }
        return new_pos;
    }

    static enemy_permutations(state) {
        const enemies = [];
        const agents_list = state["agents"];
        const agent_faction = state["faction"];
        if (
            !Array.isArray(agents_list) ||
            !agents_list.every(a => a instanceof Agent) ||
            typeof agent_faction !== 'string'
        ) {
            return enemies;
        }
        for (const agent of agents_list) {
            if (
                typeof agent.State["faction"] === 'string' &&
                agent.State["faction"] !== agent_faction
            ) {
                enemies.push(agent);
            }
        }
        return enemies;
    }

    static food_permutations(state) {
        const food_positions = [];
        const source_positions = state["foodPositions"];
        if (!Array.isArray(source_positions) || !source_positions.every(p => p instanceof Vector2)) {
            return food_positions;
        }
        food_positions.push(...source_positions);
        return food_positions;
    }

    static starting_position_permutations(state) {
        const starting_positions = [];
        const position = state["position"];
        if (!(position instanceof Vector2)) {
            return starting_positions;
        }
        starting_positions.push(position);
        return starting_positions;
    }

    static go_to_enemy_cost(action, state) {
        const starting_position = action.get_parameter("startingPosition");
        const target_agent = action.get_parameter("target");
        if (!(starting_position instanceof Vector2) || !(target_agent instanceof Agent)) {
            return Infinity;
        }
        const target_position = target_agent.State["position"];
        if (!(target_position instanceof Vector2)) {
            return Infinity;
        }
        return RpgUtils._distance(starting_position, target_position);
    }

    static go_to_food_cost(action, state) {
        const starting_position = action.get_parameter("startingPosition");
        const target_position = action.get_parameter("target");
        if (!(starting_position instanceof Vector2) || !(target_position instanceof Vector2)) {
            return Infinity;
        }
        return RpgUtils._distance(starting_position, target_position);
    }

    static _distance(pos1, pos2) {
        return Math.sqrt(
            Math.pow(Math.abs(pos2.X - pos1.X), 2) + Math.pow(Math.abs(pos2.Y - pos1.Y), 2)
        );
    }
}

class CommonRpgAgentHandlers {
    static _rng = new random.Random();

    static _get_food_in_range(source, food_positions, range_val) {
        for (const position of food_positions) {
            if (RpgUtils.in_distance(source, position, range_val)) {
                return position;
            }
        }
        return null;
    }

    static see_enemies_sensor_handler(agent_instance) {
        // No lock needed in JS single-threaded model
        const agents_in_state = agent_instance.State["agents"];
        if (Array.isArray(agents_in_state)) {
            const sight_range = agent_instance.State["sight_range"] || 10.0;
            const enemy_in_range = RpgUtils.get_enemy_in_range(
                agent_instance, agents_in_state, sight_range
            );
            agent_instance.State["canSeeEnemies"] = enemy_in_range !== null;
        }
    }

    static enemy_proximity_sensor_handler(agent_instance) {
        const agents_in_state = agent_instance.State["agents"];
        if (Array.isArray(agents_in_state)) {
            const enemy_in_range = RpgUtils.get_enemy_in_range(
                agent_instance, agents_in_state, 1.0
            );
            agent_instance.State["nearEnemy"] = enemy_in_range !== null;
        }
    }

    static kill_nearby_enemy_executor(agent_instance, action_instance) {
        const agents_in_state = agent_instance.State["agents"];
        if (Array.isArray(agents_in_state)) {
            const target_enemy = RpgUtils.get_enemy_in_range(
                agent_instance, agents_in_state, 1.0
            );
            if (target_enemy !== null) {
                let current_hp = target_enemy.State["hp"];
                if (typeof current_hp === 'number') {
                    current_hp -= 1;
                    target_enemy.State["hp"] = current_hp;
                    console.log(
                        `${agent_instance.Name} attacked ${target_enemy.Name}. ${target_enemy.Name} HP: ${current_hp}`
                    );
                    if (current_hp <= 0) {
                        console.log(`${target_enemy.Name} defeated!`);
                        return ExecutionStatus.Succeeded;
                    }
                }
            }
        }
        return ExecutionStatus.Failed;
    }

    static go_to_enemy_executor(agent_instance, action_instance) {
        const target_agent = action_instance.get_parameter("target");
        const agent_position = agent_instance.State["position"];
        if (!(target_agent instanceof Agent) || !(agent_position instanceof Vector2)) {
            return ExecutionStatus.Failed;
        }
        const target_position = target_agent.State["position"];
        if (!(target_position instanceof Vector2)) {
            return ExecutionStatus.Failed;
        }
        const new_position = RpgUtils.move_towards_other_position(
            agent_position, target_position
        );
        agent_instance.State["position"] = new_position;
        console.log(
            `${agent_instance.Name} moving toward ${target_agent.Name} from ${agent_position} to ${new_position}`
        );
        if (RpgUtils.in_distance(new_position, target_position, 1.0)) {
            console.log(`${agent_instance.Name} reached ${target_agent.Name}!`);
            return ExecutionStatus.Succeeded;
        } else {
            return ExecutionStatus.Executing;
        }
    }

    static see_food_sensor_handler(agent_instance) {
        const agent_position = agent_instance.State["position"];
        const food_positions_in_state = agent_instance.State["foodPositions"];
        if (agent_position instanceof Vector2 && Array.isArray(food_positions_in_state)) {
            const food_sight_range = agent_instance.State["food_sight_range"] || 20.0;
            const food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                agent_position, food_positions_in_state, food_sight_range
            );
            agent_instance.State["canSeeFood"] = food_in_range !== null;
            if (!agent_instance.State["canSeeFood"] && agent_instance.State["eatingFood"]) {
                agent_instance.State["eatingFood"] = false;
            }
        }
    }

    static food_proximity_sensor_handler(agent_instance) {
        const agent_position = agent_instance.State["position"];
        const food_positions_in_state = agent_instance.State["foodPositions"];
        if (agent_position instanceof Vector2 && Array.isArray(food_positions_in_state)) {
            const food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                agent_position, food_positions_in_state, 1.0
            );
            agent_instance.State["nearFood"] = food_in_range !== null;
            if (!agent_instance.State["nearFood"] && agent_instance.State["eatingFood"]) {
                agent_instance.State["eatingFood"] = false;
            }
        }
    }

    static look_for_food_executor(agent_instance, action_instance) {
        const agent_position = agent_instance.State["position"];
        if (agent_position instanceof Vector2) {
            let new_x = agent_position.X + CommonRpgAgentHandlers._rng.randint(-1, 1);
            let new_y = agent_position.Y + CommonRpgAgentHandlers._rng.randint(-1, 1);
            new_x = Math.max(0, Math.min(new_x, MaxX - 1));
            new_y = Math.max(0, Math.min(new_y, MaxY - 1));
            const new_position = new Vector2(new_x, new_y);
            agent_instance.State["position"] = new_position;
        }
        const can_see_food = agent_instance.State["canSeeFood"];
        if (typeof can_see_food === 'boolean' && can_see_food) {
            return ExecutionStatus.Succeeded;
        }
        return ExecutionStatus.Failed;
    }

    static go_to_food_executor(agent_instance, action_instance) {
        const food_position = action_instance.get_parameter("target");
        const agent_position = agent_instance.State["position"];
        if (!(food_position instanceof Vector2) || !(agent_position instanceof Vector2)) {
            return ExecutionStatus.Failed;
        }
        const new_position = RpgUtils.move_towards_other_position(
            agent_position, food_position
        );
        agent_instance.State["position"] = new_position;
        if (RpgUtils.in_distance(new_position, food_position, 1.0)) {
            return ExecutionStatus.Succeeded;
        } else {
            return ExecutionStatus.Executing;
        }
    }

    static eat_food_executor(agent_instance, action_instance) {
        const food_positions_in_state = agent_instance.State["foodPositions"];
        const agent_position = agent_instance.State["position"];
        if (Array.isArray(food_positions_in_state) && agent_position instanceof Vector2) {
            const food_to_eat = CommonRpgAgentHandlers._get_food_in_range(
                agent_position, food_positions_in_state, 1.0
            );
            if (food_to_eat !== null) {
                const food_eaten = agent_instance.State["food_eaten"] || 0;
                console.log(
                    "food_eaten" in agent_instance.State ?
                    `${agent_instance.Name} ate food at ${food_to_eat}. Food eaten: ${food_eaten} -> ${food_eaten + 1}` :
                    `${agent_instance.Name} ate food at ${food_to_eat}`
                );
                const index = food_positions_in_state.indexOf(food_to_eat);
                if (index > -1) {
                    food_positions_in_state.splice(index, 1);
                }
                return ExecutionStatus.Succeeded;
            }
        }
        return ExecutionStatus.Failed;
    }
}

class RpgCharacterFactory {
    static create(agents, name = "Player") {
        const remove_enemies_goal = new Goal(
            "Remove Enemies", 1.0, { "canSeeEnemies": false }
        );
        const see_enemies_sensor = new Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        );
        const enemy_proximity_sensor = new Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler, "Enemy Proximity Sensor"
        );
        const go_to_enemy_action = new Action({
            name: "Go To Enemy",
            executor: CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions: { "canSeeEnemies": true, "nearEnemy": false },
            postconditions: { "nearEnemy": true },
            permutation_selectors: {
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback: RpgUtils.go_to_enemy_cost,
        });
        const kill_nearby_enemy_action = new Action({
            name: "Kill Nearby Enemy",
            executor: CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions: { "nearEnemy": true },
            postconditions: { "canSeeEnemies": false, "nearEnemy": false },
        });
        const agent = new Agent({
            name: name,
            state: {
                "canSeeEnemies": false,
                "nearEnemy": false,
                "hp": 80,
                "position": new Vector2(10, 10),
                "faction": name.includes("Monster") ? "enemy" : "player",
                "agents": agents,
                "sight_range": name.includes("Monster") ? 5.0 : 10.0,
            },
            goals: [remove_enemies_goal],
            sensors: [see_enemies_sensor, enemy_proximity_sensor],
            actions: [go_to_enemy_action, kill_nearby_enemy_action],
        });
        return agent;
    }
}

class PlayerFactory {
    static create(agents, food_positions, name = "Player", use_extreme = false) {
        let food_goal;
        if (use_extreme) {
            food_goal = new ExtremeGoal(
                "Maximize Food Eaten", 1.0, { "food_eaten": true }
            );
        } else {
            food_goal = new ComparativeGoal(
                "Get exactly 3 food", 1.0, {
                    "food_eaten": new ComparisonValuePair(3, ComparisonOperator.Equals)
                }
            );
        }
        const remove_enemies_goal = new Goal(
            "Remove Enemies", 10.0, { "canSeeEnemies": false }
        );
        const see_enemies_sensor = new Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        );
        const enemy_proximity_sensor = new Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler, "Enemy Proximity Sensor"
        );
        const see_food_sensor = new Sensor(
            CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor"
        );
        const food_proximity_sensor = new Sensor(
            CommonRpgAgentHandlers.food_proximity_sensor_handler, "Food Proximity Sensor"
        );
        const go_to_enemy_action = new Action({
            name: "Go To Enemy",
            executor: CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions: { "canSeeEnemies": true, "nearEnemy": false },
            postconditions: { "nearEnemy": true },
            permutation_selectors: {
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback: RpgUtils.go_to_enemy_cost,
        });
        const kill_nearby_enemy_action = new Action({
            name: "Kill Nearby Enemy",
            executor: CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions: { "nearEnemy": true },
            postconditions: { "canSeeEnemies": false, "nearEnemy": false },
        });
        const look_for_food_action = new Action({
            name: "Look For Food",
            executor: CommonRpgAgentHandlers.look_for_food_executor,
            preconditions: { "canSeeFood": false },
            postconditions: { "canSeeFood": true },
        });
        const go_to_food_action = new Action({
            name: "Go To Food",
            executor: CommonRpgAgentHandlers.go_to_food_executor,
            preconditions: { "canSeeFood": true, "nearFood": false },
            postconditions: { "nearFood": true },
            permutation_selectors: {
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback: RpgUtils.go_to_food_cost,
        });
        const eat_food_action = new Action({
            name: "Eat Food",
            executor: CommonRpgAgentHandlers.eat_food_executor,
            preconditions: { "nearFood": true },
            arithmetic_postconditions: { "food_eaten": 1 },
        });

        const rest_executor = (agent_instance, action_instance) => {
            console.log(`${agent_instance.Name} is resting`);
            return ExecutionStatus.Succeeded;
        };
        const rest_action = new Action({
            name: "Rest",
            executor: rest_executor,
            preconditions: { "well_rested": false },
            postconditions: { "well_rested": true, "stretched": false },
            cost_callback: (agent_instance, action_instance) => 100,
        });

        const walk_around_executor = (agent_instance, action_instance) => {
            console.log(`${agent_instance.Name} is walking around`);
            return ExecutionStatus.Succeeded;
        };
        const walk_around_action = new Action({
            name: "Walk Around",
            executor: walk_around_executor,
            preconditions: { "stretched": false },
            postconditions: { "stretched": true, "well_rested": false },
            cost_callback: (agent_instance, action_instance) => 100,
        });

        const agent = new Agent({
            name: name,
            state: {
                "canSeeEnemies": false,
                "nearEnemy": false,
                "canSeeFood": false,
                "nearFood": false,
                "hp": 80,
                "food_eaten": 0,
                "position": new Vector2(10, 10),
                "faction": "player",
                "agents": agents,
                "foodPositions": food_positions,
                "well_rested": false,
                "stretched": false,
                "sight_range": 10.0,
                "food_sight_range": 20.0,
            },
            goals: [
                food_goal,
                remove_enemies_goal,
                new Goal("Get well rested", 0.11, { "well_rested": true }),
                new Goal("Get stretched", 0.1, { "stretched": true }),
            ],
            sensors: [
                see_enemies_sensor,
                enemy_proximity_sensor,
                see_food_sensor,
                food_proximity_sensor,
            ],
            actions: [
                go_to_enemy_action,
                kill_nearby_enemy_action,
                look_for_food_action,
                go_to_food_action,
                eat_food_action,
                rest_action,
                walk_around_action,
            ],
        });
        return agent;
    }
}

class RpgMonsterFactory {
    static _counter = 1;

    static create(agents, food_positions) {
        const monster_name = `Monster ${RpgMonsterFactory._counter}`;
        RpgMonsterFactory._counter++;
        const agent = RpgCharacterFactory.create(agents, monster_name);
        agent.State["faction"] = "enemy";
        const eat_food_goal = new Goal("Eat Food", 0.1, { "eatingFood": true });
        const see_food_sensor = new Sensor(CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor");
        const food_proximity_sensor = new Sensor(CommonRpgAgentHandlers.food_proximity_sensor_handler, "Food Proximity Sensor");
        const look_for_food_action = new Action({
            name: "Look For Food",
            executor: CommonRpgAgentHandlers.look_for_food_executor,
            preconditions: { "canSeeFood": false, "canSeeEnemies": false },
            postconditions: { "canSeeFood": true },
        });
        const go_to_food_action = new Action({
            name: "Go To Food",
            executor: CommonRpgAgentHandlers.go_to_food_executor,
            preconditions: { "canSeeFood": true, "canSeeEnemies": false },
            postconditions: { "nearFood": true },
            permutation_selectors: {
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback: RpgUtils.go_to_food_cost,
        });
        const eat_action = new Action({
            name: "Eat",
            executor: CommonRpgAgentHandlers.eat_food_executor,
            preconditions: { "nearFood": true, "canSeeEnemies": false },
            postconditions: { "eatingFood": true },
        });

        Object.assign(agent.State, {
            "canSeeFood": false,
            "nearFood": false,
            "eatingFood": false,
            "foodPositions": food_positions,
            "hp": 2,
            "sight_range": 5.0,
            "food_sight_range": 5.0,
        });

        agent.Goals.push(eat_food_goal);
        agent.Sensors.push(see_food_sensor, food_proximity_sensor);
        agent.Actions.push(go_to_food_action, look_for_food_action, eat_action);
        return agent;
    }
}

class RpgExampleComparativePygame {
    static run(use_extreme) {
        pygame.init();
        const screen = pygame.display.set_mode([WIDTH, HEIGHT]);
        pygame.display.set_caption("RPG GOAP Example");
        const clock = pygame.time.Clock();

        const _random = new random.Random();
        const agents = [];
        const food_positions = [];

        const player = PlayerFactory.create(agents, food_positions, "Player", use_extreme);
        agents.push(player);

        for (let i = 0; i < 20; i++) {
            food_positions.push(new Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1)));
        }

        for (let i = 0; i < 10; i++) {
            const monster = RpgMonsterFactory.create(agents, food_positions);
            monster.State["position"] = new Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1));
            agents.push(monster);
        }

        let running = true;
        let turn = 0;
        
        const gameLoop = () => {
            if (!running || turn >= 600) {
                console.log("Game finished.");
                return;
            }

            turn++;
            console.log(`--- Turn ${turn} ---`);

            for (const agent of [...agents]) { // Iterate on a copy
                if (agents.includes(agent)) {
                    agent.step(StepMode.OneAction);
                    RpgExampleComparativePygame._process_deaths(agents);
                }
            }

            if (!agents.includes(player)) {
                console.log("Player defeated! Game Over.");
                running = false;
            }
            
            RpgExampleComparativePygame._render_grid(screen, agents, food_positions);
            
            setTimeout(gameLoop, 200); // Next turn after 200ms
        };
        
        gameLoop(); // Start the loop
    }

    static _render_grid(screen, agents, food_positions) {
        // This function is a no-op in the console version.
        // In a real browser-based version, this would draw to a canvas.
    }

    static _process_deaths(agents) {
        const cull_list = [];
        for (const agent of agents) {
            const hp = agent.State["hp"];
            if (typeof hp === 'number' && hp <= 0) {
                cull_list.push(agent);
            }
        }

        for (const agent_to_remove of cull_list) {
            const index = agents.indexOf(agent_to_remove);
            if (index > -1) {
                agents.splice(index, 1);
                console.log(`Agent ${agent_to_remove.Name} has died.`);
            }
        }
    }
}

// === MAIN EXECUTION ===
// In Node.js, the script is executed directly.
// This is equivalent to Python's `if __name__ == "__main__":`
RpgExampleComparativePygame.run(true);
