import pygame
import random
from typing import List

from goap import Agent, StepMode

from .utils import Vector2, MaxX, MaxY
from .factories import PlayerFactory, RpgMonsterFactory
CELL_SIZE = 30
WIDTH = 20 * CELL_SIZE
HEIGHT = 20 * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class RpgExampleComparativePygame:
    @staticmethod
    def run(use_extreme) -> None:

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG GOAP Example")
        clock = pygame.time.Clock()

        _random = random.Random()
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = PlayerFactory.create(agents, food_positions, use_extreme=use_extreme)
        agents.append(player)

        for _ in range(20):
            food_positions.append(
                Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1))
            )

        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(
                _random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1)
            )
            agents.append(monster)

        running = True
        turn = 0
        last_update = pygame.time.get_ticks()

        while running and turn < 600:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 200:
                turn += 1
                print(f"--- Turn {turn} ---")

                # Iterate on a copy of the agents list to safely handle agents being removed (defeated)
                for agent in list(agents):
                    if (
                        agent in agents
                    ):  # Check if agent wasn't removed by a previous death this turn
                        agent.step(mode=StepMode.OneAction)
                        # Process deaths immediately after each action to prevent dead agents from acting
                        RpgExampleComparativePygame._process_deaths(agents)
                last_update = current_time

                if player not in agents:
                    print("Player defeated! Game Over.")
                    break

            RpgExampleComparativePygame._render_grid(screen, agents, food_positions)
            pygame.display.flip()
            clock.tick(60)

        print("Game finished.")
        pygame.quit()

    @staticmethod
    def _render_grid(
        screen: pygame.Surface, agents: List["Agent"], food_positions: List[Vector2]
    ) -> None:
        screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

        for pos in food_positions:
            if 0 <= pos.X < MaxX and 0 <= pos.Y < MaxY:
                rect = pygame.Rect(
                    int(pos.X) * CELL_SIZE + 2,
                    int(pos.Y) * CELL_SIZE + 2,
                    CELL_SIZE - 4,
                    CELL_SIZE - 4,
                )
                pygame.draw.ellipse(screen, YELLOW, rect)

        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")

            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < MaxX and 0 <= agent_pos.Y < MaxY:
                    rect = pygame.Rect(
                        int(agent_pos.X) * CELL_SIZE + 2,
                        int(agent_pos.Y) * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4,
                    )

                    if agent_faction == "player":
                        agent_hp = agent.State.get("hp")
                        color = (
                            RED if isinstance(agent_hp, int) and agent_hp < 30 else BLUE
                        )
                        pygame.draw.rect(screen, color, rect)
                    else:
                        pygame.draw.rect(screen, GREEN, rect)

    @staticmethod
    def _process_deaths(agents: List["Agent"]) -> None:
        cull_list: List["Agent"] = []
        for agent in agents:
            hp = agent.State.get("hp")
            if isinstance(hp, int) and hp <= 0:
                cull_list.append(agent)

        for agent_to_remove in cull_list:
            agents.remove(agent_to_remove)
            print(f"Agent {agent_to_remove.Name} has died.")


