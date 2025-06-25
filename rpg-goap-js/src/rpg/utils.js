export const MaxX = 20;
export const MaxY = 20;

export class Vector2 {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  equals(other) {
    return other instanceof Vector2 && this.x === other.x && this.y === other.y;
  }
}

export class RpgUtils {
  static inDistance(pos1, pos2, maxDistance) {
    return RpgUtils._distance(pos1, pos2) <= maxDistance;
  }

  static getEnemyInRange(source, agents, distance) {
    for (const agent of agents) {
      if (agent === source) continue;
      const sourcePos = source.state.position;
      const agentPos = agent.state.position;
      const sourceFaction = source.state.faction;
      const agentFaction = agent.state.faction;
      if (
        sourcePos instanceof Vector2 &&
        agentPos instanceof Vector2 &&
        typeof sourceFaction === 'string' &&
        typeof agentFaction === 'string' &&
        RpgUtils.inDistance(sourcePos, agentPos, distance) &&
        sourceFaction !== agentFaction
      ) {
        return agent;
      }
    }
    return null;
  }

  static moveTowardsOtherPosition(pos1, pos2) {
    const newPos = new Vector2(pos1.x, pos1.y);
    const xDiff = pos2.x - newPos.x;
    const yDiff = pos2.y - newPos.y;
    const xSign = xDiff > 0 ? 1 : xDiff < 0 ? -1 : 0;
    const ySign = yDiff > 0 ? 1 : yDiff < 0 ? -1 : 0;
    if (xSign !== 0) {
      newPos.x += xSign;
    } else if (ySign !== 0) {
      newPos.y += ySign;
    }
    return newPos;
  }

  static enemyPermutations(state) {
    const enemies = [];
    const agents = state.agents;
    const agentFaction = state.faction;
    if (!Array.isArray(agents) || typeof agentFaction !== 'string') {
      return enemies;
    }
    for (const agent of agents) {
      const faction = agent.state.faction;
      if (typeof faction === 'string' && faction !== agentFaction) {
        enemies.push(agent);
      }
    }
    return enemies;
  }

  static foodPermutations(state) {
    const foodPositions = [];
    const positions = state.foodPositions;
    if (!Array.isArray(positions)) return foodPositions;
    for (const p of positions) {
      if (p instanceof Vector2) foodPositions.push(p);
    }
    return foodPositions;
  }

  static startingPositionPermutations(state) {
    const startingPositions = [];
    const pos = state.position;
    if (pos instanceof Vector2) startingPositions.push(pos);
    return startingPositions;
  }

  static goToEnemyCost(action) {
    const start = action.getParameter('startingPosition');
    const target = action.getParameter('target');
    if (!(start instanceof Vector2) || !target) return Infinity;
    const targetPos = target.state.position;
    if (!(targetPos instanceof Vector2)) return Infinity;
    return RpgUtils._distance(start, targetPos);
  }

  static goToFoodCost(action) {
    const start = action.getParameter('startingPosition');
    const target = action.getParameter('target');
    if (!(start instanceof Vector2) || !(target instanceof Vector2)) return Infinity;
    return RpgUtils._distance(start, target);
  }

  static _distance(p1, p2) {
    return Math.sqrt(
      Math.pow(Math.abs(p2.x - p1.x), 2) + Math.pow(Math.abs(p2.y - p1.y), 2)
    );
  }
}

