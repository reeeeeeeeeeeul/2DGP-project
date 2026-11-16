"""Minimal square workshop map for the first playable prototype."""

import sys

import pygame


SCREEN_SIZE = (800, 800)
MAP_SIZE = pygame.Vector2(640, 640)
MAP_ORIGIN = pygame.Vector2(
    (SCREEN_SIZE[0] - MAP_SIZE.x) / 2,
    (SCREEN_SIZE[1] - MAP_SIZE.y) / 2,
)
WALL_THICKNESS = 48
PLAYER_SIZE = 24
PLAYER_SPEED = 240
ENTRANCE_WIDTH = 96

BACKGROUND_COLOR = (35, 28, 43)
FLOOR_COLOR = (186, 151, 110)
FLOOR_ALT_COLOR = (180, 143, 102)
WALL_COLOR = (76, 52, 69)
WALL_EDGE_COLOR = (111, 77, 84)
ENTRANCE_COLOR = (219, 183, 120)
PLAYER_COLOR = (104, 170, 214)
TEXT_COLOR = (246, 232, 198)


def get_map_rect() -> pygame.Rect:
    return pygame.Rect(
        round(MAP_ORIGIN.x),
        round(MAP_ORIGIN.y),
        round(MAP_SIZE.x),
        round(MAP_SIZE.y),
    )


def get_collision_rects(map_rect: pygame.Rect) -> list[pygame.Rect]:
    entrance_left = map_rect.centerx - ENTRANCE_WIDTH // 2
    entrance_right = map_rect.centerx + ENTRANCE_WIDTH // 2
    return [
        pygame.Rect(map_rect.left, map_rect.top, map_rect.width, WALL_THICKNESS),
        pygame.Rect(map_rect.left, map_rect.bottom - WALL_THICKNESS, entrance_left - map_rect.left, WALL_THICKNESS),
        pygame.Rect(entrance_right, map_rect.bottom - WALL_THICKNESS, map_rect.right - entrance_right, WALL_THICKNESS),
        pygame.Rect(map_rect.left, map_rect.top, WALL_THICKNESS, map_rect.height),
        pygame.Rect(map_rect.right - WALL_THICKNESS, map_rect.top, WALL_THICKNESS, map_rect.height),
    ]


def draw_map(screen: pygame.Surface, map_rect: pygame.Rect) -> None:
    pygame.draw.rect(screen, FLOOR_COLOR, map_rect)

    tile_size = 32
    for row, y in enumerate(range(map_rect.top + WALL_THICKNESS, map_rect.bottom - WALL_THICKNESS, tile_size)):
        for column, x in enumerate(
            range(map_rect.left + WALL_THICKNESS, map_rect.right - WALL_THICKNESS, tile_size)
        ):
            color = FLOOR_ALT_COLOR if (row + column) % 2 else FLOOR_COLOR
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))

    for wall in get_collision_rects(map_rect):
        pygame.draw.rect(screen, WALL_COLOR, wall)
        pygame.draw.rect(screen, WALL_EDGE_COLOR, wall, 3)

    entrance = pygame.Rect(
        map_rect.centerx - ENTRANCE_WIDTH // 2,
        map_rect.bottom - WALL_THICKNESS,
        ENTRANCE_WIDTH,
        WALL_THICKNESS,
    )
    pygame.draw.rect(screen, ENTRANCE_COLOR, entrance)
    pygame.draw.rect(screen, WALL_EDGE_COLOR, entrance, 3)


def move_player(
    player: pygame.Rect,
    movement: pygame.Vector2,
    collision_rects: list[pygame.Rect],
) -> None:
    player.x += round(movement.x)
    for wall in collision_rects:
        if player.colliderect(wall):
            if movement.x > 0:
                player.right = wall.left
            elif movement.x < 0:
                player.left = wall.right

    player.y += round(movement.y)
    for wall in collision_rects:
        if player.colliderect(wall):
            if movement.y > 0:
                player.bottom = wall.top
            elif movement.y < 0:
                player.top = wall.bottom


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Witch's Little Workshop - Map Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    map_rect = get_map_rect()
    collision_rects = get_collision_rects(map_rect)
    player = pygame.Rect(
        map_rect.centerx - PLAYER_SIZE // 2,
        map_rect.bottom - WALL_THICKNESS - PLAYER_SIZE - 12,
        PLAYER_SIZE,
        PLAYER_SIZE,
    )
    running = True

    while running:
        delta_time = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w],
        )
        if movement.length_squared():
            movement = movement.normalize() * PLAYER_SPEED * delta_time
        move_player(player, movement, collision_rects)

        screen.fill(BACKGROUND_COLOR)
        draw_map(screen, map_rect)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.draw.rect(screen, TEXT_COLOR, player, 2)

        label = font.render("WASD  Move", True, TEXT_COLOR)
        screen.blit(label, (24, 24))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()