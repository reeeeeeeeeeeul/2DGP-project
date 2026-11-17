"""Workshop map layout, rendering, and collision geometry."""

from pathlib import Path

import pygame

from cauldron import Cauldron


MAP_SIZE = pygame.Vector2(320, 320)
WALL_THICKNESS = 32
ASSET_SCALE = 2
MAP_TILE_SIZE = 16
FLOOR_COLOR = (186, 151, 110)
FLOOR_ALT_COLOR = (180, 143, 102)

ASSET_ROOT = Path(__file__).parent
WALL_ASSET_ROOT = (
    ASSET_ROOT
    / "CozyInteriors_v1.0"
    / "CozyInteriors"
    / "02_Walls_Doors"
    / "village_wood"
)
KITCHEN_ASSET_ROOT = (
    ASSET_ROOT
    / "CozyInteriors_v1.0"
    / "CozyInteriors"
    / "03_Furniture"
    / "Kitchen"
)
COUNTER_SOURCE_SIZE = (16, 32)
COUNTER_SIZE = tuple(size * ASSET_SCALE for size in COUNTER_SOURCE_SIZE)
COUNTER_TOP_CROP = MAP_TILE_SIZE * 2
COUNTER_DISPLAY_SIZE = COUNTER_SIZE
COUNTER_Y = round(MAP_SIZE.y) - MAP_TILE_SIZE - COUNTER_DISPLAY_SIZE[1]
COUNTER_COLLISION_Y = COUNTER_Y + COUNTER_TOP_CROP
COUNTER_COLLISION_SIZE = (
    COUNTER_SIZE[0],
    COUNTER_SIZE[1] - COUNTER_TOP_CROP,
)
CAULDRON_Y = WALL_THICKNESS - MAP_TILE_SIZE


class WorkshopMap:
    """The empty workshop floor with a single rear wall."""

    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, round(MAP_SIZE.x), round(MAP_SIZE.y))
        self.surface = pygame.Surface(self.rect.size)
        self.foreground_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.cauldron = Cauldron(self.rect, CAULDRON_Y)
        self.wall_assets = {
            "face": self._load_asset(
                WALL_ASSET_ROOT / "village_wood_wall_face_mid.png", (16, 32)
            ),
            "counter": self._load_asset(
                KITCHEN_ASSET_ROOT / "counter_plain_mid.png",
                COUNTER_SOURCE_SIZE,
            ),
        }
        self.collision_rects = [
            pygame.Rect(
                self.rect.left,
                self.rect.top,
                self.rect.width,
                WALL_THICKNESS,
            )
        ]
        self.collision_rects.extend(
            pygame.Rect(
                x,
                COUNTER_COLLISION_Y,
                COUNTER_COLLISION_SIZE[0],
                COUNTER_COLLISION_SIZE[1],
            )
            for x in range(0, self.rect.width, COUNTER_DISPLAY_SIZE[0])
        )
        self.collision_rects.append(self.cauldron.collision_rect)

    def update(self, delta_time: float) -> None:
        self.cauldron.update(delta_time)

    @staticmethod
    def _load_asset(path: Path, size: tuple[int, int]) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        scaled_size = tuple(dimension * ASSET_SCALE for dimension in size)
        return pygame.transform.scale(image, scaled_size)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(self.surface, FLOOR_COLOR, self.rect)

        tile_size = MAP_TILE_SIZE
        for row, y in enumerate(range(self.rect.top, self.rect.bottom, tile_size)):
            for column, x in enumerate(
                range(self.rect.left, self.rect.right, tile_size)
            ):
                color = FLOOR_ALT_COLOR if (row + column) % 2 else FLOOR_COLOR
                pygame.draw.rect(self.surface, color, (x, y, tile_size, tile_size))

        for x in range(self.rect.left, self.rect.right, 32):
            self.surface.blit(self.wall_assets["face"], (x, self.rect.top))

        self.cauldron.draw(self.surface)

        display_size = self.get_display_size(screen.get_size())
        scaled_map = pygame.transform.scale(self.surface, display_size)
        screen.blit(scaled_map, self.get_display_origin(screen.get_size()))

    def draw_foreground(self, screen: pygame.Surface) -> None:
        self.foreground_surface.fill((0, 0, 0, 0))
        for x in range(self.rect.left, self.rect.right, COUNTER_SIZE[0]):
            self.foreground_surface.blit(self.wall_assets["counter"], (x, COUNTER_Y))

        display_size = self.get_display_size(screen.get_size())
        scaled_foreground = pygame.transform.scale(
            self.foreground_surface,
            display_size,
        )
        screen.blit(scaled_foreground, self.get_display_origin(screen.get_size()))

    @staticmethod
    def get_display_origin(screen_size: tuple[int, int]) -> tuple[int, int]:
        display_size = WorkshopMap.get_display_size(screen_size)
        return (
            round((screen_size[0] - display_size[0]) / 2),
            round((screen_size[1] - display_size[1]) / 2),
        )

    @staticmethod
    def get_display_scale(screen_size: tuple[int, int]) -> float:
        return min(
            screen_size[0] / MAP_SIZE.x,
            screen_size[1] / MAP_SIZE.y,
        )

    @staticmethod
    def get_display_size(screen_size: tuple[int, int]) -> tuple[int, int]:
        display_scale = WorkshopMap.get_display_scale(screen_size)
        return (
            round(MAP_SIZE.x * display_scale),
            round(MAP_SIZE.y * display_scale),
        )
