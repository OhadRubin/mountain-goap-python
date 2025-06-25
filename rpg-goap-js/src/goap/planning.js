import { PriorityQueue, DictionaryExtensionMethods, Utils } from './utils.js';
import { Goal, ExtremeGoal, ComparativeGoal, ComparisonOperator } from './goals.js';
import { Action } from './actions.js';
import { Agent } from './agent.js';
import { PriorityQueueNode } from './types.js';

export class ActionNode extends PriorityQueueNode {
  constructor(action, state, parameters) {
    super();
    this.action = action ? action.copy() : null;
    this.state = DictionaryExtensionMethods.copyDict(state);
    this.parameters = DictionaryExtensionMethods.copyDict(parameters);
    if (this.action) {
      this.action.setParameters(this.parameters);
    }
  }

  cost(currentState) {
    if (!this.action) return Infinity;
    return this.action.getCost(currentState);
  }

  equals(other) {
    if (!(other instanceof ActionNode)) return false;
    if (this === other) return true;
    if (this.action) {
      if (!other.action) return false;
      if (!this.action.equals(other.action)) return false;
    } else if (other.action) {
      return false;
    }
    return this._stateMatches(other);
  }

  hashCode() {
    const actionHash = this.action ? this.action.hashCode() : 0;
    const items = [];
    for (const [k, v] of Object.entries(this.state)) {
      try {
        const val = typeof v === 'object' ? JSON.stringify(v) : String(v);
        items.push(`${k}:${val}`);
      } catch {}
    }
    const stateStr = items.sort().join('|');
    let hash = 0;
    const str = `${actionHash}|${stateStr}`;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return hash;
  }

  _stateMatches(other) {
    for (const [k, v] of Object.entries(this.state)) {
      if (!(k in other.state)) return false;
      if (other.state[k] !== v) return false;
    }
    for (const [k, v] of Object.entries(other.state)) {
      if (!(k in this.state)) return false;
      if (this.state[k] !== v) return false;
    }
    return true;
  }
}

export class ActionGraph {
  constructor(actions, state) {
    this.actionNodes = [];
    for (const action of actions) {
      const permutations = action.getPermutations(state);
      for (const perm of permutations) {
        this.actionNodes.push(new ActionNode(action, state, perm));
      }
    }
  }

  *neighbors(node) {
    for (const template of this.actionNodes) {
      if (template.action && template.action.isPossible(node.state)) {
        const newAction = template.action.copy();
        const newState = DictionaryExtensionMethods.copyDict(node.state);
        const newParams = DictionaryExtensionMethods.copyDict(template.parameters);
        const newNode = new ActionNode(newAction, newState, newParams);
        if (newNode.action) {
          newNode.action.applyEffects(newNode.state);
        }
        yield newNode;
      }
    }
  }
}

export class ActionAStar {
  constructor(graph, start, goal, costMax, stepMax) {
    this.goal = goal;
    this.finalPoint = null;
    this.costSoFar = new Map();
    this.stepsSoFar = new Map();
    this.cameFrom = new Map();

    const frontier = new PriorityQueue();
    frontier.enqueue(start, 0);
    this.cameFrom.set(start, start);
    this.costSoFar.set(start, 0);
    this.stepsSoFar.set(start, 0);

    while (frontier.count > 0) {
      const current = frontier.dequeue();
      if (this._meetsGoal(current, start)) {
        this.finalPoint = current;
        break;
      }
      for (const next of graph.neighbors(current)) {
        const actionCost = next.cost(current.state);
        const newCost = this.costSoFar.get(current) + actionCost;
        const newSteps = this.stepsSoFar.get(current) + 1;
        if (newCost > costMax || newSteps > stepMax) continue;
        if (!this.costSoFar.has(next) || newCost < this.costSoFar.get(next)) {
          this.costSoFar.set(next, newCost);
          this.stepsSoFar.set(next, newSteps);
          const priority = newCost + this._heuristic(next, goal, current);
          if (frontier.contains(next)) {
            frontier.updatePriority(next, priority);
          } else {
            frontier.enqueue(next, priority);
          }
          this.cameFrom.set(next, current);
          Agent.onEvaluatedActionNode(next, this.cameFrom);
        }
      }
    }
  }

  _heuristic(node, goal, prev) {
    let cost = 0;
    if (goal instanceof Goal) {
      for (const [k, v] of Object.entries(goal.desiredState)) {
        if (!(k in node.state) || node.state[k] !== v) cost += 1;
      }
    } else if (goal instanceof ExtremeGoal) {
      for (const [k, maximize] of Object.entries(goal.desiredState)) {
        if (!(k in node.state) || !(k in prev.state)) { cost += Infinity; continue; }
        const cur = node.state[k];
        const prevVal = prev.state[k];
        if (maximize) {
          if (!Utils.isHigherThanOrEquals(cur, prevVal)) cost += Math.abs(cur - prevVal);
        } else {
          if (!Utils.isLowerThanOrEquals(cur, prevVal)) cost += Math.abs(cur - prevVal);
        }
      }
    } else if (goal instanceof ComparativeGoal) {
      for (const [k, pair] of Object.entries(goal.desiredState)) {
        if (!(k in node.state) || !(k in prev.state)) { cost += Infinity; continue; }
        const cur = node.state[k];
        const desired = pair.value;
        const op = pair.operator;
        const prevVal = prev.state[k];
        const diff = Math.abs(cur - prevVal);
        if (op === ComparisonOperator.Equals) {
          if (cur !== desired) cost += diff;
        } else if (op === ComparisonOperator.LessThan) {
          if (!Utils.isLowerThan(cur, desired)) cost += diff;
        } else if (op === ComparisonOperator.GreaterThan) {
          if (!Utils.isHigherThan(cur, desired)) cost += diff;
        } else if (op === ComparisonOperator.LessThanOrEquals) {
          if (!Utils.isLowerThanOrEquals(cur, desired)) cost += diff;
        } else if (op === ComparisonOperator.GreaterThanOrEquals) {
          if (!Utils.isHigherThanOrEquals(cur, desired)) cost += diff;
        } else {
          cost += Infinity;
        }
      }
    }
    return cost;
  }

  _meetsGoal(node, prev) {
    return Utils.meetsGoal(this.goal, node, prev);
  }
}

export class Planner {
  static plan(agent, costMaximum, stepMaximum) {
    Agent.onPlanningStarted(agent);
    let bestUtility = 0;
    let bestAstar = null;
    let bestGoal = null;
    for (const goal of agent.goals) {
      Agent.onPlanningStartedForGoal(agent, goal);
      const graph = new ActionGraph(agent.actions, agent.state);
      const startNode = new ActionNode(null, agent.state, {});
      const astar = new ActionAStar(graph, startNode, goal, costMaximum, stepMaximum);
      const cursor = astar.finalPoint;
      if (cursor) {
        const planCost = astar.costSoFar.get(cursor) || 0;
        const util = planCost === 0 ? 0 : goal.weight / planCost;
        if (cursor.action && util > bestUtility) {
          bestUtility = util;
          bestAstar = astar;
          bestGoal = goal;
        }
        Agent.onPlanningFinishedForGoal(agent, goal, util);
      } else {
        Agent.onPlanningFinishedForGoal(agent, goal, 0);
      }
    }
    if (bestAstar && bestGoal && bestAstar.finalPoint) {
      Planner._updateAgentActionList(bestAstar.finalPoint, bestAstar, agent);
      agent.isBusy = true;
      Agent.onPlanningFinished(agent, bestGoal, bestUtility);
    } else {
      Agent.onPlanningFinished(agent, null, 0);
    }
    agent.isPlanning = false;
  }

  static _updateAgentActionList(startNode, astar, agent) {
    let cursor = startNode;
    const actionList = [];
    while (cursor && cursor.action && astar.cameFrom.has(cursor)) {
      actionList.push(cursor.action);
      cursor = astar.cameFrom.get(cursor);
    }
    actionList.reverse();
    agent.currentActionSequences.push(actionList);
    Agent.onPlanUpdated(agent, actionList);
  }
}
