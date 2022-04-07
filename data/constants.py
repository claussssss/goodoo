from typing import Tuple, List

import pygame.image
from pygame import Surface
from pygame.math import Vector2

RESOLUTIONS: List[Tuple[int, int]] = [(1920, 1080), (1280, 720), (960, 540)]
SCREEN_SIZE: Tuple[int, int] = RESOLUTIONS[2]

WORLD_WIDTH: int = 32       # world width in tiles number
WORLD_HEIGHT: int = 18      # world height in tiles number

FPS: int = 60

TILE_EDGE: int = SCREEN_SIZE[0] // WORLD_WIDTH    # tile edge length in pixels
TILE_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE)
TILE_COLOR: Tuple[int, int, int] = (60, 60, 60)

GROUND_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE // 10)
GROUND_COLOR: Tuple[int, int, int] = (100, 100, 100)

PLAYER_EDGE: int = 2 * TILE_EDGE // 3    # player edge length in pixels
PLAYER_SIZE: Tuple[int, int] = (PLAYER_EDGE, PLAYER_EDGE)
PLAYER_MAX_V: float = TILE_EDGE - 0.1
PLAYER_SPRITE: str = "resources/sprites/player.png"

GRAVITY: Vector2 = Vector2(0, PLAYER_MAX_V / 75)    # gravity acceleration in pixels

BEAM_STRENGTH: float = PLAYER_MAX_V / 5             # beam impulse velocity length
BEAM_DURATION: float = 0.2                          # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)    # beam deterioration at each frame in percentage

BEAM_VECTOR_STEP: float = TILE_EDGE / 4
BEAM_MAX_VECTOR_STEP: int = int(Vector2(SCREEN_SIZE).length() / BEAM_VECTOR_STEP)

CURSOR_SPRITE: Surface = pygame.image.load("resources/sprites/cursor.png")
CURSOR_SIZE: Tuple[int, int] = CURSOR_SPRITE.get_size()

WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (250, 0, 0)
