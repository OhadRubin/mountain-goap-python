import { DictionaryExtensionMethods } from './utils.js';
import { ExecutionStatus, ComparisonOperator } from './goals.js';

export const StepMode = Object.freeze({
  Default: 1,
  OneAction: 2,
  AllActions: 3,
});


export class Action {
  constructor({
    name = null,
    permutationSelectors = {},
    executor = Action._defaultExecutor,
    cost = 1.0,
    costCallback = null,
    preconditions = {},
    comparativePreconditions = {},
    postconditions = {},
    arithmeticPostconditions = {},
    parameterPostconditions = {},
    stateMutator = null,
    stateChecker = null,
    stateCostDeltaMultiplier = Action.defaultStateCostDeltaMultiplier,
  } = {}) {
    this._permutationSelectors = { ...permutationSelectors };
    this._executor = executor;
    this.name = name ?? `Action ${Math.random()}`;
    this._costBase = cost;
    this._costCallback = costCallback ?? Action._defaultCostCallback;
    this._preconditions = { ...preconditions };
    this._comparativePreconditions = { ...comparativePreconditions };
    this._postconditions = { ...postconditions };
    this._arithmeticPostconditions = { ...arithmeticPostconditions };
    this._parameterPostconditions = { ...parameterPostconditions };
    this._stateMutator = stateMutator;
    this._stateChecker = stateChecker;
    this.stateCostDeltaMultiplier = stateCostDeltaMultiplier;
    this._parameters = {};
    this.executionStatus = ExecutionStatus.NotYetExecuted;
  }

  equals(other) {
    return other instanceof Action && this.name === other.name;
  }

  copy() {
    const a = new Action({
      name: this.name,
      permutationSelectors: this._permutationSelectors,
      executor: this._executor,
      cost: this._costBase,
      costCallback: this._costCallback,
      preconditions: DictionaryExtensionMethods.copyDict(this._preconditions),
      comparativePreconditions: DictionaryExtensionMethods.copyDict(
        this._comparativePreconditions
      ),
      postconditions: DictionaryExtensionMethods.copyDict(this._postconditions),
      arithmeticPostconditions: DictionaryExtensionMethods.copyDict(
        this._arithmeticPostconditions
      ),
      parameterPostconditions: DictionaryExtensionMethods.copyDict(
        this._parameterPostconditions
      ),
      stateMutator: this._stateMutator,
      stateChecker: this._stateChecker,
      stateCostDeltaMultiplier: this.stateCostDeltaMultiplier,
    });
    a._parameters = DictionaryExtensionMethods.copyDict(this._parameters);
    return a;
  }

  setParameter(key, value) {
    this._parameters[key] = value;
  }

  getParameter(key) {
    return this._parameters[key];
  }

  getCost(currentState) {
    try {
      return this._costCallback(this, currentState);
    } catch {
      return Infinity;
    }
  }

  execute(agent) {
    Action.onBeginExecute(agent, this, this._parameters);
    if (this.isPossible(agent.state)) {
      const status = this._executor(agent, this);
      if (status === ExecutionStatus.Succeeded) {
        this.applyEffects(agent.state);
      }
      this.executionStatus = status;
      Action.onFinishExecute(agent, this, status, this._parameters);
      return status;
    }
    this.executionStatus = ExecutionStatus.NotPossible;
    Action.onFinishExecute(agent, this, this.executionStatus, this._parameters);
    return this.executionStatus;
  }

  isPossible(state) {
    for (const [key, value] of Object.entries(this._preconditions)) {
      if (!(key in state)) return false;
      const current = state[key];
      if (current === null && value !== null) return false;
      if (current !== null && current !== value) return false;
    }
    for (const [key, pair] of Object.entries(this._comparativePreconditions)) {
      if (!(key in state)) return false;
      const current = state[key];
      const desired = pair.value;
      const op = pair.operator;
      if (op === ComparisonOperator.Undefined) return false;
      if (op === ComparisonOperator.Equals) {
        if (current !== desired) return false;
      } else if (current == null || desired == null) {
        return false;
      } else if (op === ComparisonOperator.LessThan) {
        if (!(current < desired)) return false;
      } else if (op === ComparisonOperator.GreaterThan) {
        if (!(current > desired)) return false;
      } else if (op === ComparisonOperator.LessThanOrEquals) {
        if (!(current <= desired)) return false;
      } else if (op === ComparisonOperator.GreaterThanOrEquals) {
        if (!(current >= desired)) return false;
      }
    }
    if (this._stateChecker && !this._stateChecker(this, state)) return false;
    return true;
  }

  getPermutations(state) {
    if (Object.keys(this._permutationSelectors).length === 0) return [{}];
    const outputs = {};
    for (const [key, selector] of Object.entries(this._permutationSelectors)) {
      const vals = selector(state);
      if (!vals || vals.length === 0) return [];
      outputs[key] = vals;
    }
    const params = Object.keys(outputs);
    const counts = params.map((p) => outputs[p].length);
    const indices = new Array(params.length).fill(0);
    const results = [];
    while (true) {
      const out = {};
      for (let i = 0; i < indices.length; i++) {
        const param = params[i];
        out[param] = outputs[param][indices[i]];
      }
      results.push(out);
      if (Action._indicesAtMaximum(indices, counts)) break;
      Action._incrementIndices(indices, counts);
    }
    return results;
  }

  applyEffects(state) {
    for (const [key, value] of Object.entries(this._postconditions)) {
      state[key] = value;
    }
    for (const [key, value] of Object.entries(this._arithmeticPostconditions)) {
      if (!(key in state)) continue;
      const current = state[key];
      if (typeof current === 'number' && typeof value === 'number') {
        state[key] = current + value;
      }
    }
    for (const [paramKey, stateKey] of Object.entries(this._parameterPostconditions)) {
      if (paramKey in this._parameters) {
        state[stateKey] = this._parameters[paramKey];
      }
    }
    if (this._stateMutator) this._stateMutator(this, state);
  }

  setParameters(params) {
    this._parameters = params;
  }

  hashCode() {
    let hash = 0;
    const str = this.name ?? '';
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  }

  static _defaultExecutor(agent, action) {
    return ExecutionStatus.Failed;
  }

  static _defaultCostCallback(action, state) {
    return action._costBase;
  }

  static defaultStateCostDeltaMultiplier(action, key) {
    return 1.0;
  }

  static _indicesAtMaximum(indices, counts) {
    for (let i = 0; i < indices.length; i++) {
      if (indices[i] < counts[i] - 1) return false;
    }
    return true;
  }

  static _incrementIndices(indices, counts) {
    if (Action._indicesAtMaximum(indices, counts)) return;
    for (let i = 0; i < indices.length; i++) {
      if (indices[i] === counts[i] - 1) {
        indices[i] = 0;
      } else {
        indices[i] += 1;
        return;
      }
    }
  }
}

Action._onBegin = [];
Action._onFinish = [];

Action.onBeginExecute = (agent, action, params) => {
  for (const h of Action._onBegin) h(agent, action, params);
};
Action.onFinishExecute = (agent, action, status, params) => {
  for (const h of Action._onFinish) h(agent, action, status, params);
};

Action.registerOnBeginExecute = (h) => { Action._onBegin.push(h); };
Action.registerOnFinishExecute = (h) => { Action._onFinish.push(h); };
