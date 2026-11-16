"""Game state and rendering for the workshop scene."""

import pygame

from character import Character
from map import DISPLAY_SCALE, WorkshopMap


SCREEN_SIZE = (800, 800)
BACKGROUND_COLOR = (35, 28, 43)
TEXT_COLOR = (246, 232, 198)


class GameWorld:
    """Owns the map and player and coordinates their updates."""

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 28)
        self.workshop_map = WorkshopMap()
        self.character = Character(
            self.workshop_map.rect,
            self.workshop_map.collision_rects[0].height,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.character.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.character.update(
            delta_time,
            self.workshop_map.rect,
            self.workshop_map.collision_rects,
        )

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.workshop_map.draw(screen)
        display_origin = self.workshop_map.get_display_origin(screen.get_size())
        display_character = pygame.transform.scale(
            self.character.sprite,
            (
                self.character.rect.width * DISPLAY_SCALE,
                self.character.rect.height * DISPLAY_SCALE,
            ),
        )
        screen.blit(
            display_character,
            (
                display_origin[0] + self.character.rect.x * DISPLAY_SCALE,
                display_origin[1] + self.character.rect.y * DISPLAY_SCALE,
            ),
        )
        label = self.font.render("WASD  Move", True, TEXT_COLOR)
        screen.blit(label, (24, 24))
