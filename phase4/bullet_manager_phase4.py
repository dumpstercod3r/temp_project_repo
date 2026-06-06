# pyright: strict

from __future__ import annotations

from typing import ClassVar
from collections.abc import Callable
from math import sin, cos, sqrt

from common_types_phase4 import *


class NormalBullet:
    def __init__(self, color: Color, x: float, y: float, angle: float):
        self._color: Color = color
        self._coords: tuple[float, float] = (x, y)
        self._angle = angle
    @property
    def coords(self) -> tuple[float, float]:
        return self._coords
    @property
    def color(self) -> Color:
        return self._color
    @property
    def speed(self) -> int:
        return 5 # seconds to cross diagonal length of screen
    @property
    def angle(self) -> float:
        return self._angle    
    @property
    def damage(self) -> int:
        return 1    
    def move_bullet_to(self, x: float, y: float):
        self._coords = (x, y)
    def effects(self):
        pass


class BulletManager:
    BULLET_FACTORY: ClassVar[dict[BulletType, Callable[[Color, float, float, float], Bullet]]
        ] = {
            BulletType.NORMAL: NormalBullet,
        }

    def __init__(self, colors: list[Color], grid_size: list[int]):
        self._screen_height: int = grid_size[0]
        self._screen_width: int = grid_size[1]
        self.prepare_round(colors)

    @property
    def active_bullets(self) -> list[Bullet]:
        return self._active_bullets
    
    def create_bullet(self, bullet_type: BulletType, color: Color, x: float, y: float, angle: float) -> Bullet:
        bullet = self.BULLET_FACTORY[bullet_type](color, x, y, angle)
        self._active_bullets.append(bullet)
        return bullet
    
    def move_bullet(self, bullet: Bullet, delta_time: float):
        diagonal_length = sqrt((self._screen_width ** 2) + (self._screen_height ** 2))
        change = (diagonal_length / bullet.speed) * delta_time
        new_x = bullet.coords[0] + (change * cos(bullet.angle))
        new_y = bullet.coords[1] + (change * sin(bullet.angle))
        bullet.move_bullet_to(new_x, new_y)
    
    def despawn(self, bullet: Bullet):
        self._active_bullets.remove(bullet)
    
    def screen_edge_collision(self, bullet: Bullet):
        x, y = bullet.coords
        if not(0 <= x < self._screen_width) or not(0 <= y < self._screen_height):
            self.despawn(bullet)
    
    def update(self, bullet_color: Color, fire_rate: float, click_info: tuple[float, float, float] | None, delta_time: float) -> bool:
        # each bullet moves every time this is called
        # checks if each bullet hits the edge of screen.
        if click_info is not None and self._elapsed_time_since_last_bullet >= 1 / fire_rate:
            self.create_bullet(BulletType.NORMAL, bullet_color, *click_info)
            self._elapsed_time_since_last_bullet = 0
            return True
        for i in self._active_bullets:
            self.screen_edge_collision(i)
            self.move_bullet(i, delta_time)
        self._elapsed_time_since_last_bullet += delta_time
        return False
    
    def prepare_round(self, colors: list[Color]):
        self._colors: list[Color] = colors
        self._active_bullets: list[Bullet] = []
        self._bullet_colors_queue = [] #???
        self._elapsed_time_since_last_bullet: float = 0