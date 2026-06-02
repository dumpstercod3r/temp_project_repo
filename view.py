# pyright: strict

from __future__ import annotations

from typing import Protocol
import pyxel

from model import Grid, Node, Shooter
from common_types import Bullet, Enemy, Color

class UpdateHandler(Protocol):
    def update(self): ...

class DrawHandler(Protocol):
    def draw(self): ...


class ZumaView:
    def __init__(self):
        self._width: int = 112
        self._height: int = 112
        self._tile_size: int = 16

        # color dictionary for converting sprite colors
        # from template colors to actual color
        # {Color : (Dark Color, Light Color)}
        self._color_dictionary: dict[Color, tuple[int, int]] = {
            Color.GREEN: (pyxel.COLOR_GREEN, pyxel.COLOR_LIME)
        }
    
    def draw_grid(self, grid: Grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if not(i == len(grid) // 2 and j == len(grid[i]) // 2):
                    tile = grid[i][j]
                    if tile is not None:
                        pyxel.blt(j * 16, i * 16, 0, tile.resources[0], tile.resources[1], 16, 16)
                    else:
                        pyxel.blt(j * 16, i * 16, 0, 0, 16, 16, 16)
    
    def draw_path(self, path: list[Node]):
        for i in path:
            coords = i.coords
            pyxel.pal(pyxel.COLOR_GRAY, pyxel.COLOR_WHITE)
            pyxel.blt(coords[0] * 16, coords[1]  * 16, 0, 0, 16, 16, 16)
            pyxel.pal()

    def draw_shooter(self, shooter: Shooter):
        ...
    
    def draw_bullet(self, bullet: Bullet):
        ...
    
    def draw_enemy(self, enemy: Enemy):
        ...

    def start_game(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height, fps=30)
        pyxel.load("resources.pyxres")
        pyxel.run(update_handler.update, draw_handler.draw)