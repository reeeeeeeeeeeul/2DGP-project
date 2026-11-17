"""Workshop map layout, rendering, and collision geometry."""

from pathlib import Path

import pygame


MAP_SIZE = pygame.Vector2(320, 320)
WALL_THICKNESS = 32
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


class WorkshopMap:
    """The empty workshop floor with a single rear wall."""

    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, round(MAP_SIZE.x), round(MAP_SIZE.y))
        self.surface = pygame.Surface(self.rect.size)
        self.wall_assets = {
            "face": self._load_asset(
                WALL_ASSET_ROOT / "village_wood_wall_face_mid.png", (32, 64)
            )
        }
        self.collision_rects = [
            pygame.Rect(
                self.rect.left,
                self.rect.top,
                self.rect.width,
                WALL_THICKNESS,
            )
        ]

    @staticmethod
    def _load_asset(path: Path, size: tuple[int, int]) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(self.surface, FLOOR_COLOR, self.rect)

        tile_size = 16
        for row, y in enumerate(range(self.rect.top, self.rect.bottom, tile_size)):
            for column, x in enumerate(
                range(self.rect.left, self.rect.right, tile_size)
            ):
                color = FLOOR_ALT_COLOR if (row + column) % 2 else FLOOR_COLOR
                pygame.draw.rect(self.surface, color, (x, y, tile_size, tile_size))

        for x in range(self.rect.left, self.rect.right, 32):
            self.surface.blit(self.wall_assets["face"], (x, self.rect.top))

        display_size = self.get_display_size(screen.get_size())
        scaled_map = pygame.transform.scale(self.surface, display_size)
        screen.blit(scaled_map, self.get_display_origin(screen.get_size()))

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
