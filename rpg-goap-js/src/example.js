import { createCanvas } from 'canvas';
import { Agent } from './goap/agent.js';
import { StepMode } from './goap/actions.js';
import { PlayerFactory, RpgMonsterFactory } from './rpg/factories.js';
import { Vector2, MaxX, MaxY } from './rpg/utils.js';

// Minimal canvas-based example mirroring the Python version

const CELL_SIZE = 20;
const WIDTH = MaxX * CELL_SIZE;
const HEIGHT = MaxY * CELL_SIZE;

const canvas = createCanvas(WIDTH, HEIGHT);
const ctx = canvas.getContext('2d');

const agents = [];
const foodPositions = [];

function randomInt(max) {
  return Math.floor(Math.random() * max);
}

for (let i = 0; i < 20; i++) {
  foodPositions.push(new Vector2(randomInt(MaxX), randomInt(MaxY)));
}

const player = PlayerFactory.create(agents, foodPositions);
agents.push(player);

for (let i = 0; i < 5; i++) {
  const m = RpgMonsterFactory.create(agents, foodPositions);
  m.state.position = new Vector2(randomInt(MaxX), randomInt(MaxY));
  agents.push(m);
}

let turn = 0;

function step() {
  turn += 1;
  agents.forEach((a) => a.step(StepMode.OneAction));
  draw();
  if (turn < 10) setTimeout(step, 200);
}

function draw() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  ctx.strokeStyle = 'white';
  for (let x = 0; x <= WIDTH; x += CELL_SIZE) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, HEIGHT);
    ctx.stroke();
  }
  for (let y = 0; y <= HEIGHT; y += CELL_SIZE) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(WIDTH, y);
    ctx.stroke();
  }

  ctx.fillStyle = 'yellow';
  for (const pos of foodPositions) {
    ctx.fillRect(pos.x * CELL_SIZE + 2, pos.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
  }

  for (const agent of agents) {
    const pos = agent.state.position;
    if (!(pos instanceof Vector2)) continue;
    ctx.fillStyle = agent.state.faction === 'player' ? 'blue' : 'green';
    ctx.fillRect(pos.x * CELL_SIZE + 2, pos.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
  }
}

step();

export { canvas }; // For potential testing

