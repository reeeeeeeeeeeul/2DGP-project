"""Pygame application setup and main loop."""

import sys

import pygame

from game_world import GameWorld


class GameFramework:
    """Initializes Pygame and runs the game world."""

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Witch's Little Workshop - Map Prototype")
        clock = pygame.time.Clock()
        world = GameWorld()
        running = True

        while running:
            delta_time = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False
                world.handle_event(event)

            world.update(delta_time)
            world.draw(screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
