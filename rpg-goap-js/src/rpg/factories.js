import {
  Action,
  StepMode,
} from '../goap/actions.js';
import {
  Goal,
  ComparativeGoal,
  ExtremeGoal,
  ComparisonOperator,
  ComparisonValuePair,
  ExecutionStatus,
} from '../goap/goals.js';
import { Sensor } from '../goap/sensors.js';
import { Agent } from '../goap/agent.js';
import {
  Vector2,
  RpgUtils,
  MaxX,
  MaxY,
} from './utils.js';

class CommonRpgAgentHandlers {
  static _rng() {
    return Math.random();
  }

  static _getFoodInRange(source, foodPositions, rangeVal) {
    for (const position of foodPositions) {
      if (RpgUtils.inDistance(source, position, rangeVal)) {
        return position;
      }
    }
    return null;
  }

  static seeEnemiesSensorHandler(agent) {
    const agents = agent.state.agents;
    if (Array.isArray(agents)) {
      const range = agent.state.sight_range ?? 10.0;
      const enemy = RpgUtils.getEnemyInRange(agent, agents, range);
      agent.state.canSeeEnemies = enemy !== null;
    }
  }

  static enemyProximitySensorHandler(agent) {
    const agents = agent.state.agents;
    if (Array.isArray(agents)) {
      const enemy = RpgUtils.getEnemyInRange(agent, agents, 1.0);
      agent.state.nearEnemy = enemy !== null;
    }
  }

  static killNearbyEnemyExecutor(agent, action) {
    const agents = agent.state.agents;
    if (Array.isArray(agents)) {
      const target = RpgUtils.getEnemyInRange(agent, agents, 1.0);
      if (target) {
        const currentHp = target.state.hp;
        if (typeof currentHp === 'number') {
          target.state.hp = currentHp - 1;
          if (target.state.hp <= 0) {
            return ExecutionStatus.Succeeded;
          }
          return ExecutionStatus.Executing;
        }
      }
    }
    return ExecutionStatus.Failed;
  }

  static goToEnemyExecutor(agent, action) {
    const target = action.getParameter('target');
    const agentPos = agent.state.position;
    if (!(target instanceof Agent) || !(agentPos instanceof Vector2)) {
      return ExecutionStatus.Failed;
    }
    const targetPos = target.state.position;
    if (!(targetPos instanceof Vector2)) return ExecutionStatus.Failed;
    const newPos = RpgUtils.moveTowardsOtherPosition(agentPos, targetPos);
    agent.state.position = newPos;
    if (RpgUtils.inDistance(newPos, targetPos, 1.0)) {
      return ExecutionStatus.Succeeded;
    }
    return ExecutionStatus.Executing;
  }

  static seeFoodSensorHandler(agent) {
    const agentPos = agent.state.position;
    const foodPositions = agent.state.foodPositions;
    if (agentPos instanceof Vector2 && Array.isArray(foodPositions)) {
      const range = agent.state.food_sight_range ?? 20.0;
      const food = CommonRpgAgentHandlers._getFoodInRange(
        agentPos,
        foodPositions,
        range
      );
      agent.state.canSeeFood = food !== null;
      if (!agent.state.canSeeFood && agent.state.eatingFood) {
        agent.state.eatingFood = false;
      }
    }
  }

  static foodProximitySensorHandler(agent) {
    const agentPos = agent.state.position;
    const foodPositions = agent.state.foodPositions;
    if (agentPos instanceof Vector2 && Array.isArray(foodPositions)) {
      const food = CommonRpgAgentHandlers._getFoodInRange(
        agentPos,
        foodPositions,
        1.0
      );
      agent.state.nearFood = food !== null;
      if (!agent.state.nearFood && agent.state.eatingFood) {
        agent.state.eatingFood = false;
      }
    }
  }

  static lookForFoodExecutor(agent, action) {
    const agentPos = agent.state.position;
    if (agentPos instanceof Vector2) {
      let newX = agentPos.x + Math.floor(CommonRpgAgentHandlers._rng() * 3) - 1;
      let newY = agentPos.y + Math.floor(CommonRpgAgentHandlers._rng() * 3) - 1;
      newX = Math.max(0, Math.min(newX, MaxX - 1));
      newY = Math.max(0, Math.min(newY, MaxY - 1));
      agent.state.position = new Vector2(newX, newY);
    }
    if (agent.state.canSeeFood === true) {
      return ExecutionStatus.Succeeded;
    }
    return ExecutionStatus.Failed;
  }

  static goToFoodExecutor(agent, action) {
    const foodPos = action.getParameter('target');
    const agentPos = agent.state.position;
    if (!(foodPos instanceof Vector2) || !(agentPos instanceof Vector2)) {
      return ExecutionStatus.Failed;
    }
    const newPos = RpgUtils.moveTowardsOtherPosition(agentPos, foodPos);
    agent.state.position = newPos;
    if (RpgUtils.inDistance(newPos, foodPos, 1.0)) {
      return ExecutionStatus.Succeeded;
    }
    return ExecutionStatus.Executing;
  }

  static eatFoodExecutor(agent, action) {
    const foodPositions = agent.state.foodPositions;
    const agentPos = agent.state.position;
    if (Array.isArray(foodPositions) && agentPos instanceof Vector2) {
      const food = CommonRpgAgentHandlers._getFoodInRange(
        agentPos,
        foodPositions,
        1.0
      );
      if (food) {
        const foodEaten = agent.state.food_eaten ?? 0;
        foodPositions.splice(foodPositions.indexOf(food), 1);
        agent.state.food_eaten = foodEaten + 1;
        return ExecutionStatus.Succeeded;
      }
    }
    return ExecutionStatus.Failed;
  }
}

export class RpgCharacterFactory {
  static create(agents, name = 'Player') {
    const removeEnemiesGoal = new Goal('Remove Enemies', 1.0, {
      canSeeEnemies: false,
    });

    const seeEnemiesSensor = new Sensor(
      CommonRpgAgentHandlers.seeEnemiesSensorHandler,
      'Enemy Sight Sensor'
    );
    const enemyProximitySensor = new Sensor(
      CommonRpgAgentHandlers.enemyProximitySensorHandler,
      'Enemy Proximity Sensor'
    );

    const goToEnemyAction = new Action({
      name: 'Go To Enemy',
      executor: CommonRpgAgentHandlers.goToEnemyExecutor,
      preconditions: { canSeeEnemies: true, nearEnemy: false },
      postconditions: { nearEnemy: true },
      permutationSelectors: {
        target: RpgUtils.enemyPermutations,
        startingPosition: RpgUtils.startingPositionPermutations,
      },
      costCallback: RpgUtils.goToEnemyCost,
    });

    const killNearbyEnemyAction = new Action({
      name: 'Kill Nearby Enemy',
      executor: CommonRpgAgentHandlers.killNearbyEnemyExecutor,
      preconditions: { nearEnemy: true },
      postconditions: { canSeeEnemies: false, nearEnemy: false },
    });

    const agent = new Agent({
      name,
      state: {
        canSeeEnemies: false,
        nearEnemy: false,
        hp: 80,
        position: new Vector2(10, 10),
        faction: name.includes('Monster') ? 'enemy' : 'player',
        agents,
        sight_range: name.includes('Monster') ? 5.0 : 10.0,
      },
      goals: [removeEnemiesGoal],
      sensors: [seeEnemiesSensor, enemyProximitySensor],
      actions: [goToEnemyAction, killNearbyEnemyAction],
    });

    return agent;
  }
}

export class PlayerFactory {
  static create(agents, foodPositions, name = 'Player', useExtreme = false) {
    const foodGoal = useExtreme
      ? new ExtremeGoal('Maximize Food Eaten', 1.0, { food_eaten: true })
      : new ComparativeGoal('Get exactly 3 food', 1.0, {
          food_eaten: new ComparisonValuePair(3, ComparisonOperator.Equals),
        });

    const removeEnemiesGoal = new Goal('Remove Enemies', 10.0, {
      canSeeEnemies: false,
    });

    const seeEnemiesSensor = new Sensor(
      CommonRpgAgentHandlers.seeEnemiesSensorHandler,
      'Enemy Sight Sensor'
    );
    const enemyProximitySensor = new Sensor(
      CommonRpgAgentHandlers.enemyProximitySensorHandler,
      'Enemy Proximity Sensor'
    );
    const seeFoodSensor = new Sensor(
      CommonRpgAgentHandlers.seeFoodSensorHandler,
      'Food Sight Sensor'
    );
    const foodProximitySensor = new Sensor(
      CommonRpgAgentHandlers.foodProximitySensorHandler,
      'Food Proximity Sensor'
    );

    const goToEnemyAction = new Action({
      name: 'Go To Enemy',
      executor: CommonRpgAgentHandlers.goToEnemyExecutor,
      preconditions: { canSeeEnemies: true, nearEnemy: false },
      postconditions: { nearEnemy: true },
      permutationSelectors: {
        target: RpgUtils.enemyPermutations,
        startingPosition: RpgUtils.startingPositionPermutations,
      },
      costCallback: RpgUtils.goToEnemyCost,
    });

    const killNearbyEnemyAction = new Action({
      name: 'Kill Nearby Enemy',
      executor: CommonRpgAgentHandlers.killNearbyEnemyExecutor,
      preconditions: { nearEnemy: true },
      postconditions: { canSeeEnemies: false, nearEnemy: false },
    });

    const lookForFoodAction = new Action({
      name: 'Look For Food',
      executor: CommonRpgAgentHandlers.lookForFoodExecutor,
      preconditions: { canSeeFood: false },
      postconditions: { canSeeFood: true },
    });

    const goToFoodAction = new Action({
      name: 'Go To Food',
      executor: CommonRpgAgentHandlers.goToFoodExecutor,
      preconditions: { canSeeFood: true, nearFood: false },
      postconditions: { nearFood: true },
      permutationSelectors: {
        target: RpgUtils.foodPermutations,
        startingPosition: RpgUtils.startingPositionPermutations,
      },
      costCallback: RpgUtils.goToFoodCost,
    });

    const eatFoodAction = new Action({
      name: 'Eat Food',
      executor: CommonRpgAgentHandlers.eatFoodExecutor,
      preconditions: { nearFood: true },
      arithmeticPostconditions: { food_eaten: 1 },
    });

    const restAction = new Action({
      name: 'Rest',
      executor: () => ExecutionStatus.Succeeded,
      preconditions: { well_rested: false },
      postconditions: { well_rested: true, stretched: false },
      costCallback: () => 100,
    });

    const walkAroundAction = new Action({
      name: 'Walk Around',
      executor: () => ExecutionStatus.Succeeded,
      preconditions: { stretched: false },
      postconditions: { stretched: true, well_rested: false },
      costCallback: () => 100,
    });

    const agent = new Agent({
      name,
      state: {
        canSeeEnemies: false,
        nearEnemy: false,
        canSeeFood: false,
        nearFood: false,
        hp: 80,
        food_eaten: 0,
        position: new Vector2(10, 10),
        faction: 'player',
        agents,
        foodPositions,
        well_rested: false,
        stretched: false,
        sight_range: 10.0,
        food_sight_range: 20.0,
      },
      goals: [
        foodGoal,
        removeEnemiesGoal,
        new Goal('Get well rested', 0.11, { well_rested: true }),
        new Goal('Get stretched', 0.1, { stretched: true }),
      ],
      sensors: [
        seeEnemiesSensor,
        enemyProximitySensor,
        seeFoodSensor,
        foodProximitySensor,
      ],
      actions: [
        goToEnemyAction,
        killNearbyEnemyAction,
        lookForFoodAction,
        goToFoodAction,
        eatFoodAction,
        restAction,
        walkAroundAction,
      ],
    });

    return agent;
  }
}

export class RpgMonsterFactory {
  static _counter = 1;

  static create(agents, foodPositions) {
    const name = `Monster ${RpgMonsterFactory._counter++}`;
    const agent = RpgCharacterFactory.create(agents, name);
    agent.state.faction = 'enemy';

    const eatFoodGoal = new Goal('Eat Food', 0.1, { eatingFood: true });
    const seeFoodSensor = new Sensor(
      CommonRpgAgentHandlers.seeFoodSensorHandler,
      'Food Sight Sensor'
    );
    const foodProximitySensor = new Sensor(
      CommonRpgAgentHandlers.foodProximitySensorHandler,
      'Food Proximity Sensor'
    );

    const lookForFoodAction = new Action({
      name: 'Look For Food',
      executor: CommonRpgAgentHandlers.lookForFoodExecutor,
      preconditions: { canSeeFood: false, canSeeEnemies: false },
      postconditions: { canSeeFood: true },
    });

    const goToFoodAction = new Action({
      name: 'Go To Food',
      executor: CommonRpgAgentHandlers.goToFoodExecutor,
      preconditions: { canSeeFood: true, canSeeEnemies: false },
      postconditions: { nearFood: true },
      permutationSelectors: {
        target: RpgUtils.foodPermutations,
        startingPosition: RpgUtils.startingPositionPermutations,
      },
      costCallback: RpgUtils.goToFoodCost,
    });

    const eatAction = new Action({
      name: 'Eat',
      executor: CommonRpgAgentHandlers.eatFoodExecutor,
      preconditions: { nearFood: true, canSeeEnemies: false },
      postconditions: { eatingFood: true },
    });

    agent.state = {
      ...agent.state,
      canSeeFood: false,
      nearFood: false,
      eatingFood: false,
      foodPositions,
      hp: 2,
      sight_range: 5.0,
      food_sight_range: 5.0,
    };

    agent.goals.push(eatFoodGoal);
    agent.sensors.push(seeFoodSensor, foodProximitySensor);
    agent.actions.push(goToFoodAction, lookForFoodAction, eatAction);
    return agent;
  }
}

export { CommonRpgAgentHandlers };

