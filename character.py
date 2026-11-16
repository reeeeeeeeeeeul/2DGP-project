"""Player character sprite, keyboard input, and movement."""

from pathlib import Path

import pygame


PLAYER_SIZE = 32
PLAYER_SPEED = 120
CHARACTER_SHEET_PATH = Path(__file__).parent / "16x16-character-8D-template.png"
MOVEMENT_KEYS = {
    pygame.K_w: pygame.Vector2(0, -1),
    pygame.K_a: pygame.Vector2(-1, 0),
    pygame.K_s: pygame.Vector2(0, 1),
    pygame.K_d: pygame.Vector2(1, 0),
}


class Character:
    """A controllable 16x16 character displayed at the game's pixel scale."""

    def __init__(self, map_rect: pygame.Rect, wall_thickness: int) -> None:
        self.sprite = self._load_sprite()
        self.rect = pygame.Rect(
            map_rect.centerx - PLAYER_SIZE // 2,
            map_rect.bottom - wall_thickness - PLAYER_SIZE - 12,
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self._pressed_keys: list[int] = []

    @staticmethod
    def _load_sprite() -> pygame.Surface:
        sheet = pygame.image.load(CHARACTER_SHEET_PATH).convert_alpha()
        frame = sheet.subsurface(pygame.Rect(0, 0, 16, 16))
        return pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))

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
        if movement.length_squared():
            movement *= PLAYER_SPEED * delta_time

        self._move(movement, collision_rects)
        self.rect.clamp_ip(map_rect)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.rect)

    def _get_movement(self) -> pygame.Vector2:
        if not self._pressed_keys:
            return pygame.Vector2()
        return MOVEMENT_KEYS[self._pressed_keys[-1]].copy()

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
