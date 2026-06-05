# pyright: strict

from __future__ import annotations

from typing import Protocol
import pyxel
import time
from phase1.common_types_phase1 import *
from phase1.managers_phase1 import *

from math import sin, cos, atan2

class UpdateHandler(Protocol):
    def update(self): ...

class DrawHandler(Protocol):
    def draw(self): ...

type Grid = list[list[Shooter | None]]

class ZumaViewPhase1:
    def __init__(self, fps: int):
        self._width: int = 240
        self._height: int = 240
        self._tile_size: int = 16
        self._bullet_orbit_radius = 12
        self._fps = fps
        self._start_time = time.time()
        self._frame_count = 0
        self._current_fps = self._fps

        # color dictionary for converting sprite colors
        # from template colors to actual color
        # {Color : (Dark Color, Light Color)}
        self._color_dictionary: dict[Color, tuple[int, int]] = {
            Color.GREEN: (pyxel.COLOR_GREEN, pyxel.COLOR_LIME)
        }
    
    @property
    def current_fps(self) -> int:
        return self._current_fps
    
    def draw_grid(self, grid: Grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if not(i == len(grid) // 2 and j == len(grid[i]) // 2):
                    tile = grid[i][j]
                    if tile is not None:
                        pyxel.blt(j * 16, i * 16, 0, tile.resources[0], tile.resources[1], 16, 16)
                    else:
                        pyxel.blt(j * 16, i * 16, 0, 0, 16, 16, 16)
                else:
                    pyxel.blt(j * 16, i * 16, 0, 0, 16, 16, 16)
    
    def draw_path(self, path: Graph):
        for i in path:
            coords = i.coords
            pyxel.pal(pyxel.COLOR_GRAY, pyxel.COLOR_WHITE)
            pyxel.blt(coords[0] * 16, coords[1]  * 16, 0, 0, 16, 16, 16)
            pyxel.pal()

    def draw_shooter(self, shooter: Shooter, next_bullet_color: Color):
        shooter_x = shooter.coords[0] * 16
        shooter_y = shooter.coords[1] * 16
        center_x = shooter_x + 8
        center_y = shooter_y + 8
        angle = atan2((pyxel.mouse_y - center_y), (pyxel.mouse_x - center_x))
        bullet_color = self._color_dictionary[next_bullet_color][1]

        # draws shooter itself:
        pyxel.blt(shooter_x, shooter_y, 0, 0, 0, 16, 16, pyxel.COLOR_BLACK)

        # draws bullet pointer:
        pyxel.circ(center_x + (self._bullet_orbit_radius * cos(angle)), center_y + (self._bullet_orbit_radius * sin(angle)), 5, bullet_color)
    
    def draw_bullet(self, bullet: Bullet):
        pyxel.circ(bullet.coords[0], bullet.coords[1], bullet.size, self._color_dictionary[bullet.color][1])
    
    def get_shot_info(self, shooter: Shooter) -> tuple[float, float, float] | None: # (x, y, angle), returns initial position and angle of a shot bullet
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            shooter_x = shooter.coords[0] * 16
            shooter_y = shooter.coords[1] * 16
            center_x = shooter_x + 8
            center_y = shooter_y + 8
            angle = atan2((pyxel.mouse_y - center_y), (pyxel.mouse_x - center_x))
            return (center_x + (self._bullet_orbit_radius * cos(angle)), center_y + (self._bullet_orbit_radius * sin(angle)), angle)
    
    def draw_enemy(self, enemy: Enemy):
        pyxel.pal(pyxel.COLOR_DARK_BLUE, self._color_dictionary[enemy.color][0])
        pyxel.pal(pyxel.COLOR_WHITE, self._color_dictionary[enemy.color][1])
        pyxel.blt(enemy.curr_node.coords[0] * 16, enemy.curr_node.coords[1] * 16, 0, 0, 32, 16, 16, pyxel.COLOR_BLACK)
        pyxel.pal()

    def start_game(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height, fps=self._fps)
        pyxel.load("../resources.pyxres")
        pyxel.run(update_handler.update, draw_handler.draw)
    
    def reset_screen(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        # calculates current fps
        self._frame_count += 1
        elapsed_time = time.time() - self._start_time
        
        if elapsed_time >= 1.0:
            self._current_fps = int(self._frame_count / elapsed_time)
            self._frame_count = 0
            self._start_time = time.time()