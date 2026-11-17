"""Animated cauldron furniture."""

from pathlib import Path

import pygame


CAULDRON_FRAME_SIZE = 32
CAULDRON_FRAME_COUNT = 6
CAULDRON_SCALE = 2
CAULDRON_SIZE = CAULDRON_FRAME_SIZE * CAULDRON_SCALE
CAULDRON_FRAME_DURATION = 0.15
CAULDRON_COLLISION_SIZE = CAULDRON_SIZE - 16
CAULDRON_COLLISION_HEIGHT = CAULDRON_COLLISION_SIZE - 16
CAULDRON_PATH = (
    Path(__file__).parent
    / "CozyInteriors_v1.0"
    / "CozyInteriors"
    / "03_Furniture"
    / "Workshops"
    / "cauldron_purple_anim_6f.png"
)


class Cauldron:
    """A centered, animated cauldron with a smaller collision area."""

    def __init__(self, map_rect: pygame.Rect, top: int) -> None:
        self.frames = self._load_frames()
        self.frame_index = 0
        self.frame_timer = 0.0
        self.rect = pygame.Rect(
            map_rect.centerx - CAULDRON_SIZE // 2,
            top,
            CAULDRON_SIZE,
            CAULDRON_SIZE,
        )
        self.collision_rect = pygame.Rect(
            self.rect.centerx - CAULDRON_COLLISION_SIZE // 2,
            self.rect.top + (CAULDRON_SIZE - CAULDRON_COLLISION_SIZE) // 2,
            CAULDRON_COLLISION_SIZE,
            CAULDRON_COLLISION_HEIGHT,
        )

    @staticmethod
    def _load_frames() -> list[pygame.Surface]:
        sheet = pygame.image.load(CAULDRON_PATH).convert_alpha()
        frames = []
        for index in range(CAULDRON_FRAME_COUNT):
            frame = sheet.subsurface(
                pygame.Rect(
                    index * CAULDRON_FRAME_SIZE,
                    0,
                    CAULDRON_FRAME_SIZE,
                    CAULDRON_FRAME_SIZE,
                )
            )
            frames.append(
                pygame.transform.scale(frame, (CAULDRON_SIZE, CAULDRON_SIZE))
            )
        return frames

    def update(self, delta_time: float) -> None:
        self.frame_timer += delta_time
        while self.frame_timer >= CAULDRON_FRAME_DURATION:
            self.frame_timer -= CAULDRON_FRAME_DURATION
            self.frame_index = (self.frame_index + 1) % CAULDRON_FRAME_COUNT

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.frames[self.frame_index], self.rect)
