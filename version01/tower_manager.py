# pyright: strict

from __future__ import annotations

from typing import ClassVar, Literal
from collections.abc import Callable

from common_types import *


class NormalTower:
    def __init__(self, r: int, c: int):
        self._coords: Coord = (r, c)
        self._direction: Direction = Direction.UP
    @property
    def cost(self) -> int:
        return 5
    @property
    def coords(self) -> Coord:
        return self._coords
    @property
    def overlay(self) -> bool:
        return False
    @property
    def bullet_type(self) -> BulletType:
        return BulletType.NORMAL
    @property
    def shooting_speed(self) -> int:
        return 2 # seconds per bullet
    @property
    def resources(self) -> tuple[int, int]:
        return (16, 0)
    @property
    def direction(self) -> Direction:
        return self._direction
    def set_direction(self, direction: Direction):
        self._direction = direction

class UpgradedTower:
    def __init__(self, r: int, c: int):
        self._coords: Coord = (r, c)
        self._direction: Direction = Direction.UP
    @property
    def cost(self) -> int:
        return 5
    @property
    def coords(self) -> Coord:
        return self._coords
    @property
    def overlay(self) -> bool:
        return False
    @property
    def bullet_type(self) -> BulletType:
        return BulletType.NORMAL
    @property
    def shooting_speed(self) -> int:
        return 2 # seconds per bullet
    @property
    def resources(self) -> tuple[int, int]:
        return (16, 0)
    @property
    def direction(self) -> Direction:
        return self._direction
    def set_direction(self, direction: Direction):
        self._direction = direction

class TowerManager:
    TOWER_FACTORY: ClassVar[dict[TowerType, Callable[[int, int], Tower]]
        ] = {
            TowerType.NORMAL: NormalTower,
        }
    
    def __init__(self):
        self._active_towers: list[Tower] = []
        self._current_direction: Direction = Direction.UP

    @property
    def active_towers(self) -> list[Tower]:
        return self._active_towers
    
    def can_buy_tower(self, tower_type: TowerType, exp: int) -> bool:
        tower = self.TOWER_FACTORY[tower_type](0, 0)
        return exp >= tower.cost

    def create_tower(self, tower_type: TowerType, r: int, c: int) -> Tower:
        tower = self.TOWER_FACTORY[tower_type](r, c)
        self._active_towers.append(tower)
        return tower

    def prepare_round(self, exp: int) -> int:
        # buy mechanics
        ...
    
    def update(self, keyboardinput: Direction | Literal["T"] | None):
        # each tower shoots 1 bullet every 2 seconds
        ...