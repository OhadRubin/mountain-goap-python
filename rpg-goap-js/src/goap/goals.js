export const ComparisonOperator = Object.freeze({
  Undefined: 0,
  Equals: 1,
  LessThan: 2,
  LessThanOrEquals: 3,
  GreaterThan: 4,
  GreaterThanOrEquals: 5,
});

export class ComparisonValuePair {
  constructor(value = null, operator = ComparisonOperator.Undefined) {
    this.value = value;
    this.operator = operator;
  }
}

export const ExecutionStatus = Object.freeze({
  NotYetExecuted: 1,
  Executing: 2,
  Succeeded: 3,
  Failed: 4,
  NotPossible: 5,
});

export class BaseGoal {
  constructor(name = null, weight = 1.0) {
    this.name = name ?? `Goal ${Math.random()}`;
    this.weight = weight;
  }
}

export class Goal extends BaseGoal {
  constructor(name = null, weight = 1.0, desiredState = {}) {
    super(name, weight);
    this.desiredState = { ...desiredState };
  }
}

export class ExtremeGoal extends BaseGoal {
  constructor(name = null, weight = 1.0, desiredState = {}) {
    super(name, weight);
    this.desiredState = { ...desiredState };
  }
}

export class ComparativeGoal extends BaseGoal {
  constructor(name = null, weight = 1.0, desiredState = {}) {
    super(name, weight);
    this.desiredState = { ...desiredState };
  }
}
