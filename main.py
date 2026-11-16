"""Minimal square workshop map for the first playable prototype."""

import sys
from pathlib import Path

import pygame


SCREEN_SIZE = (800, 800)
MAP_SIZE = pygame.Vector2(320, 320)
DISPLAY_SCALE = 2
DISPLAY_MAP_SIZE = MAP_SIZE * DISPLAY_SCALE
MAP_ORIGIN = pygame.Vector2(
    (SCREEN_SIZE[0] - DISPLAY_MAP_SIZE.x) / 2,
    (SCREEN_SIZE[1] - DISPLAY_MAP_SIZE.y) / 2,
)
WALL_THICKNESS = 32
PLAYER_SIZE = 32
PLAYER_SPEED = 120
ASSET_ROOT = Path(__file__).parent
WALL_ASSET_ROOT = ASSET_ROOT / "CozyInteriors_v1.0" / "CozyInteriors" / "02_Walls_Doors" / "village_wood"
CHARACTER_SHEET_PATH = ASSET_ROOT / "16x16-character-8D-template.png"

BACKGROUND_COLOR = (35, 28, 43)
FLOOR_COLOR = (186, 151, 110)
FLOOR_ALT_COLOR = (180, 143, 102)
TEXT_COLOR = (246, 232, 198)


def get_map_rect() -> pygame.Rect:
    return pygame.Rect(
        0,
        0,
        round(MAP_SIZE.x),
        round(MAP_SIZE.y),
    )


def get_collision_rects(map_rect: pygame.Rect) -> list[pygame.Rect]:
    return [
        pygame.Rect(map_rect.left, map_rect.top, map_rect.width, WALL_THICKNESS),
    ]


def load_asset(path: Path, size: tuple[int, int]) -> pygame.Surface:
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def load_wall_assets() -> dict[str, pygame.Surface]:
    return {
        "face": load_asset(WALL_ASSET_ROOT / "village_wood_wall_face_mid.png", (32, 64)),
    }


def load_character() -> pygame.Surface:
    sheet = pygame.image.load(CHARACTER_SHEET_PATH).convert_alpha()
    frame = sheet.subsurface(pygame.Rect(0, 0, 16, 16))
    return pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))


def draw_map(
    screen: pygame.Surface,
    map_rect: pygame.Rect,
    wall_assets: dict[str, pygame.Surface],
) -> None:
    pygame.draw.rect(screen, FLOOR_COLOR, map_rect)

    tile_size = 16
    for row, y in enumerate(range(map_rect.top, map_rect.bottom, tile_size)):
        for column, x in enumerate(range(map_rect.left, map_rect.right, tile_size)):
            color = FLOOR_ALT_COLOR if (row + column) % 2 else FLOOR_COLOR
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))

    for x in range(map_rect.left, map_rect.right, 32):
        screen.blit(wall_assets["face"], (x, map_rect.top))


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


def keep_player_inside_map(player: pygame.Rect, map_rect: pygame.Rect) -> None:
    player.clamp_ip(map_rect)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Witch's Little Workshop - Map Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    map_rect = get_map_rect()
    collision_rects = get_collision_rects(map_rect)
    wall_assets = load_wall_assets()
    character = load_character()
    map_surface = pygame.Surface((round(MAP_SIZE.x), round(MAP_SIZE.y)))
    logical_map_rect = pygame.Rect(0, 0, round(MAP_SIZE.x), round(MAP_SIZE.y))
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
        keep_player_inside_map(player, map_rect)

        screen.fill(BACKGROUND_COLOR)
        draw_map(map_surface, logical_map_rect, wall_assets)
        map_surface.blit(character, player)
        scaled_map = pygame.transform.scale(
            map_surface, (round(DISPLAY_MAP_SIZE.x), round(DISPLAY_MAP_SIZE.y))
        )
        screen.blit(scaled_map, MAP_ORIGIN)

        label = font.render("WASD  Move", True, TEXT_COLOR)
        screen.blit(label, (24, 24))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()