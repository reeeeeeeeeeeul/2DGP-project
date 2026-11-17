"""Player character sprite, keyboard input, and movement."""

from pathlib import Path

import pygame


PLAYER_SIZE = 32
PLAYER_SPEED = 120
FRAME_SIZE = 16
FRAME_COUNT = 8
IDLE_FRAME_COUNT = 3
SLEEP_FRAME = 3
SLEEP_DELAY = 5.0
WALK_FRAME_START = 4
ANIMATION_FRAME_DURATION = 0.1
CHARACTER_SHEET_PATH = Path(__file__).parent / "16x16-character-8D-template.png"
MOVEMENT_KEYS = {
    pygame.K_w: pygame.Vector2(0, -1),
    pygame.K_a: pygame.Vector2(-1, 0),
    pygame.K_s: pygame.Vector2(0, 1),
    pygame.K_d: pygame.Vector2(1, 0),
}
FACING_ROWS = {
    "down": 0,
    "down_left": 1,
    "left": 2,
    "up_left": 3,
    "up": 4,
    "up_right": 5,
    "right": 6,
    "down_right": 7,
}


class Character:
    """A controllable 16x16 character displayed at the game's pixel scale."""

    def __init__(self, map_rect: pygame.Rect, wall_thickness: int) -> None:
        self._sprites = self._load_sprites()
        self._facing = "down"
        self._animation_frame = 0
        self._animation_timer = 0.0
        self._is_moving = False
        self._inactive_time = 0.0
        self.sprite = self._sprites[self._facing][self._animation_frame]
        self.rect = pygame.Rect(
            map_rect.centerx - PLAYER_SIZE // 2,
            map_rect.bottom - wall_thickness - PLAYER_SIZE - 12,
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self._pressed_keys: list[int] = []

    @staticmethod
    def _load_sprites() -> dict[str, list[pygame.Surface]]:
        sheet = pygame.image.load(CHARACTER_SHEET_PATH).convert_alpha()
        return {
            facing: [
                pygame.transform.scale(
                    sheet.subsurface(
                        pygame.Rect(
                            column * FRAME_SIZE,
                            row * FRAME_SIZE,
                            FRAME_SIZE,
                            FRAME_SIZE,
                        )
                    ),
                    (PLAYER_SIZE, PLAYER_SIZE),
                )
                for column in range(FRAME_COUNT)
            ]
            for facing, row in FACING_ROWS.items()
        }

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in MOVEMENT_KEYS:
            if event.key in self._pressed_keys:
                self._pressed_keys.remove(event.key)
            self._pressed_keys.append(event.key)
        elif event.type == pygame.KEYUP and event.key in MOVEMENT_KEYS:
            if event.key in self._pressed_keys:
                self._pressed_keys.remove(event.key)

    def update(
        self,
        delta_time: float,
        map_rect: pygame.Rect,
        collision_rects: list[pygame.Rect],
    ) -> None:
        movement = self._get_movement()
        is_moving = movement.length_squared() > 0
        if is_moving:
            self._inactive_time = 0.0
            self._update_facing(movement)
            movement *= PLAYER_SPEED * delta_time
        else:
            self._inactive_time += delta_time

        self._move(movement, collision_rects)
        self.rect.clamp_ip(map_rect)
        self._update_animation(
            delta_time,
            is_moving,
            self._inactive_time >= SLEEP_DELAY,
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.rect)

    def _get_movement(self) -> pygame.Vector2:
        if not self._pressed_keys:
            return pygame.Vector2()
        return MOVEMENT_KEYS[self._pressed_keys[-1]].copy()

    def _update_facing(self, movement: pygame.Vector2) -> None:
        if movement.x < 0:
            self._facing = "left"
        elif movement.x > 0:
            self._facing = "right"
        elif movement.y < 0:
            self._facing = "up"
        else:
            self._facing = "down"

    def _update_animation(
        self,
        delta_time: float,
        is_moving: bool,
        is_sleeping: bool,
    ) -> None:
        if is_sleeping:
            self._animation_frame = SLEEP_FRAME
            self._animation_timer = 0.0
            self.sprite = self._sprites[self._facing][self._animation_frame]
            return

        animation_start = WALK_FRAME_START if is_moving else 0
        animation_count = (
            FRAME_COUNT - WALK_FRAME_START if is_moving else IDLE_FRAME_COUNT
        )
        if is_moving != self._is_moving:
            self._animation_frame = animation_start
            self._animation_timer = 0.0
            self._is_moving = is_moving
        else:
            self._animation_timer += delta_time

        while self._animation_timer >= ANIMATION_FRAME_DURATION:
            self._animation_timer -= ANIMATION_FRAME_DURATION
            self._animation_frame = (
                animation_start
                + (self._animation_frame - animation_start + 1) % animation_count
            )
        self.sprite = self._sprites[self._facing][self._animation_frame]

    def _move(
        self,
        movement: pygame.Vector2,
        collision_rects: list[pygame.Rect],
    ) -> None:
        self.rect.x += round(movement.x)
        for wall in collision_rects:
            if self.rect.colliderect(wall):
                if movement.x > 0:
                    self.rect.right = wall.left
                elif movement.x < 0:
                    self.rect.left = wall.right

        self.rect.y += round(movement.y)
        for wall in collision_rects:
            if self.rect.colliderect(wall):
                if movement.y > 0:
                    self.rect.bottom = wall.top
                elif movement.y < 0:
                    self.rect.top = wall.bottom
