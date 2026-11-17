"""Automatic customer movement and animation."""

from pathlib import Path

import pygame

from character import Character, PLAYER_SIZE


CUSTOMER_SPEED = 80
SPEECH_FRAME_SIZE = 11
SPEECH_FRAME_COUNT = 8
SPEECH_FRAME_DURATION = 0.15
SPEECH_SCALE = 2
SPEECH_INDICATORS_PATH = (
    Path(__file__).parent
    / "tiny-speech-indicators"
    / "tiny-speech-indicators"
    / "speech_bubble_animation-11x11.png"
)


class Customer(Character):
    """A customer who enters from the lower-right and walks to the center."""

    def __init__(self, map_rect: pygame.Rect, wall_thickness: int) -> None:
        super().__init__(map_rect, wall_thickness)
        self.rect.topleft = (
            map_rect.right - PLAYER_SIZE,
            map_rect.bottom - PLAYER_SIZE,
        )
        self._position = pygame.Vector2(self.rect.topleft)
        self._target = pygame.Vector2(
            map_rect.centerx - PLAYER_SIZE / 2,
            self._position.y,
        )
        self._path = [self._target.copy()]
        self._path_index = 0
        self._speech_frames = self._load_speech_frames()
        self._speech_frame_index = 0
        self._speech_timer = 0.0
        self.speech_indicator = self._speech_frames[0]
        self.is_arrived = False

    @staticmethod
    def _load_speech_frames() -> list[pygame.Surface]:
        sheet = pygame.image.load(SPEECH_INDICATORS_PATH).convert_alpha()
        return [
            sheet.subsurface(
                pygame.Rect(
                    index * SPEECH_FRAME_SIZE,
                    0,
                    SPEECH_FRAME_SIZE,
                    SPEECH_FRAME_SIZE,
                )
            )
            for index in range(SPEECH_FRAME_COUNT)
        ]

    def update(
        self,
        delta_time: float,
        map_rect: pygame.Rect,
        collision_rects: list[pygame.Rect],
    ) -> None:
        del map_rect, collision_rects
        is_moving = self._path_index < len(self._path)
        if is_moving:
            waypoint = self._path[self._path_index]
            direction = waypoint - self._position
            distance = direction.length()
            if distance == 0:
                self._path_index += 1
                is_moving = self._path_index < len(self._path)
            else:
                direction.normalize_ip()
                step = min(CUSTOMER_SPEED * delta_time, distance)
                self._position += direction * step
                self.rect.topleft = round(self._position.x), round(self._position.y)
                self._update_facing(direction)
                if step == distance:
                    self._path_index += 1
                    is_moving = self._path_index < len(self._path)

        if not is_moving:
            self._facing = "up"
            self.is_arrived = True
            self._update_speech_indicator(delta_time)

        self._update_animation(delta_time, is_moving, False)

    def _update_speech_indicator(self, delta_time: float) -> None:
        self._speech_timer += delta_time
        while self._speech_timer >= SPEECH_FRAME_DURATION:
            self._speech_timer -= SPEECH_FRAME_DURATION
            self._speech_frame_index = (
                self._speech_frame_index + 1
            ) % SPEECH_FRAME_COUNT
        self.speech_indicator = self._speech_frames[self._speech_frame_index]
