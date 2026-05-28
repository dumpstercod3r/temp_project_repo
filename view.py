# pyright: strict

from __future__ import annotations

from typing import Protocol
import pyxel

from model import Grid, Node, Shooter
from common_types import Bullets, Enemies

class UpdateHandler(Protocol):
    def update(self): ...

class DrawHandler(Protocol):
    def draw(self): ...


class ZumaView:
    def __init__(self):
        self._width: int = 105
        self._height: int = 105
        self._tile_size: int = 15
    
    def draw_grid(self, grid: Grid):
        ...
    
    def draw_path(self, path: list[Node]):
        ...
    
    def draw_shooter(self, shooter: Shooter):
        ...
    
    def draw_bullet(self, bullet: Bullets):
        ...
    
    def draw_enemy(self, enemy: Enemies):
        ...

    def start_game(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height, fps=30)
        pyxel.run(update_handler.update, draw_handler.draw)