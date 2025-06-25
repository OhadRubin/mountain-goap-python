import { Planner } from './planning.js';
import { StepMode } from './actions.js';
import { ExecutionStatus } from './goals.js';

export class Agent {
  static _onAgentStep = [];
  static _onActionSequenceCompleted = [];
  static _onPlanningStarted = [];
  static _onPlanningStartedForGoal = [];
  static _onPlanningFinishedForGoal = [];
  static _onPlanningFinished = [];
  static _onPlanUpdated = [];
  static _onEvaluatedActionNode = [];

  constructor({
    name = null,
    state = {},
    memory = {},
    goals = [],
    actions = [],
    sensors = [],
    costMaximum = Infinity,
    stepMaximum = Infinity,
  } = {}) {
    this.name = name ?? `Agent`;
    this.state = { ...state };
    this.memory = { ...memory };
    this.goals = goals.slice();
    this.actions = actions.slice();
    this.sensors = sensors.slice();
    this.costMaximum = costMaximum;
    this.stepMaximum = stepMaximum;
    this.currentActionSequences = [];
    this.isBusy = false;
    this.isPlanning = false;
  }

  step(mode = StepMode.Default) {
    Agent.onAgentStep(this);
    for (const sensor of this.sensors) {
      sensor.run(this);
    }
    if (mode === StepMode.Default) {
      this._stepAsync();
    } else if (mode === StepMode.OneAction) {
      this._execute();
    } else if (mode === StepMode.AllActions) {
      while (this.isBusy) {
        this._execute();
      }
    }
  }

  plan() {
    if (!this.isBusy && !this.isPlanning) {
      this.isPlanning = true;
      Agent.onPlanningStarted(this);
      Planner.plan(this, this.costMaximum, this.stepMaximum);
    }
  }

  planAsync() {
    if (!this.isBusy && !this.isPlanning) {
      this.isPlanning = true;
      Agent.onPlanningStarted(this);
      setTimeout(() => {
        Planner.plan(this, this.costMaximum, this.stepMaximum);
      }, 0);
    }
  }

  executePlan() {
    if (!this.isPlanning) {
      this._execute();
    }
  }

  clearPlan() {
    this.currentActionSequences.length = 0;
  }

  _stepAsync() {
    if (!this.isBusy && !this.isPlanning) {
      this.isPlanning = true;
      Agent.onPlanningStarted(this);
      Planner.plan(this, this.costMaximum, this.stepMaximum);
    } else if (!this.isPlanning) {
      this._execute();
    }
  }

  _execute() {
    if (this.currentActionSequences.length > 0) {
      const toRemove = [];
      for (const seq of this.currentActionSequences) {
        if (seq.length > 0) {
          const action = seq[0];
          const status = action.execute(this);
          if (status !== ExecutionStatus.Executing) {
            seq.shift();
          }
          if (seq.length === 0) toRemove.push(seq);
        } else {
          toRemove.push(seq);
        }
      }
      for (const s of toRemove) {
        const idx = this.currentActionSequences.indexOf(s);
        if (idx >= 0) this.currentActionSequences.splice(idx, 1);
      }
      if (this.currentActionSequences.length === 0) {
        this.isBusy = false;
        Agent._onActionSequenceCompleted.forEach((h) => h(this));
      }
    } else {
      this.isBusy = false;
    }
  }
}

Agent.onAgentStep = (agent) => {
  Agent._onAgentStep.forEach((h) => h(agent));
};
Agent.onActionSequenceCompleted = (agent) => {
  Agent._onActionSequenceCompleted.forEach((h) => h(agent));
};
Agent.onPlanningStarted = (agent) => {
  Agent._onPlanningStarted.forEach((h) => h(agent));
};
Agent.onPlanningStartedForGoal = (agent, goal) => {
  Agent._onPlanningStartedForGoal.forEach((h) => h(agent, goal));
};
Agent.onPlanningFinishedForGoal = (agent, goal, util) => {
  Agent._onPlanningFinishedForGoal.forEach((h) => h(agent, goal, util));
};
Agent.onPlanningFinished = (agent, goal, util) => {
  Agent._onPlanningFinished.forEach((h) => h(agent, goal, util));
};
Agent.onPlanUpdated = (agent, actions) => {
  Agent._onPlanUpdated.forEach((h) => h(agent, actions));
};
Agent.onEvaluatedActionNode = (node, map) => {
  Agent._onEvaluatedActionNode.forEach((h) => h(node, map));
};

Agent.registerOnAgentStep = (h) => Agent._onAgentStep.push(h);
Agent.registerOnActionSequenceCompleted = (h) =>
  Agent._onActionSequenceCompleted.push(h);
Agent.registerOnPlanningStarted = (h) => Agent._onPlanningStarted.push(h);
Agent.registerOnPlanningStartedForGoal = (h) =>
  Agent._onPlanningStartedForGoal.push(h);
Agent.registerOnPlanningFinishedForGoal = (h) =>
  Agent._onPlanningFinishedForGoal.push(h);
Agent.registerOnPlanningFinished = (h) =>
  Agent._onPlanningFinished.push(h);
Agent.registerOnPlanUpdated = (h) => Agent._onPlanUpdated.push(h);
Agent.registerOnEvaluatedActionNode = (h) =>
  Agent._onEvaluatedActionNode.push(h);
