"""Game state and rendering for the workshop scene."""

import pygame

from character import Character
from customer import Customer, SPEECH_FRAME_SIZE, SPEECH_SCALE
from map import WorkshopMap


BACKGROUND_COLOR = (35, 28, 43)


class GameWorld:
    """Owns the map and player and coordinates their updates."""

    def __init__(self) -> None:
        self.workshop_map = WorkshopMap()
        self.character = Character(
            self.workshop_map.rect,
            self.workshop_map.collision_rects[0].height,
        )
        self.customer = Customer(
            self.workshop_map.rect,
            self.workshop_map.collision_rects[0].height,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.character.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.workshop_map.update(delta_time)
        self.character.update(
            delta_time,
            self.workshop_map.rect,
            self.workshop_map.collision_rects,
        )
        self.customer.update(
            delta_time,
            self.workshop_map.rect,
            self.workshop_map.collision_rects,
        )

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.workshop_map.draw(screen)
        display_origin = self.workshop_map.get_display_origin(screen.get_size())
        display_scale = self.workshop_map.get_display_scale(screen.get_size())
        display_character = pygame.transform.scale(
            self.character.sprite,
            (
                round(self.character.rect.width * display_scale),
                round(self.character.rect.height * display_scale),
            ),
        )
        screen.blit(
            display_character,
            (
                display_origin[0] + round(self.character.rect.x * display_scale),
                display_origin[1] + round(self.character.rect.y * display_scale),
            ),
        )
        self.workshop_map.draw_foreground(screen)
        display_customer = pygame.transform.scale(
            self.customer.sprite,
            (
                round(self.customer.rect.width * display_scale),
                round(self.customer.rect.height * display_scale),
            ),
        )
        screen.blit(
            display_customer,
            (
                display_origin[0] + round(self.customer.rect.x * display_scale),
                display_origin[1] + round(self.customer.rect.y * display_scale),
            ),
        )
        if self.customer.is_arrived:
            speech_source_size = SPEECH_FRAME_SIZE * SPEECH_SCALE
            speech_size = round(speech_source_size * display_scale)
            display_speech_indicator = pygame.transform.scale(
                self.customer.speech_indicator,
                (speech_size, speech_size),
            )
            screen.blit(
                display_speech_indicator,
                (
                    display_origin[0]
                    + round(
                        (
                            self.customer.rect.centerx
                            - speech_source_size / 2
                        )
                        * display_scale
                    ),
                    display_origin[1]
                    + round(
                        (
                            self.customer.rect.top
                            - speech_source_size
                            - 2
                        )
                        * display_scale
                    ),
                ),
            )
