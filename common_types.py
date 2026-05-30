# pyright: strict

from enum import StrEnum, auto
from typing import Protocol

from model import Coord, Node

class Color(StrEnum):                                                                   # There will be custom colors
    GREEN = auto()

class Direction(StrEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

class BulletType(StrEnum):
    """
    Used to help create Bullet instances.
    """
    NORMAL = auto()

class EnemyType(StrEnum):
    """
    Used to help create Enemy instances.
    """
    NORMAL = auto()

class TowerType(StrEnum):
    NORMAL = auto()


class Bullet(Protocol):
    """
    Bonus Feature.
    Base game will only use NormalBullet().
    """
    @property
    def size(self) -> int:
        """
        Size multiplier.
        Base size is at least 5 pixels.
        """
        ...
    @property
    def color(self) -> Color:
        ...
    @property
    def speed(self) -> int:
        """
        Seconds it takes to cross the diagonal length of the screen.
        """
        ...
    @property
    def damage(self) -> int:
        ...
    def effects(self):
        ...
    
class Enemy(Protocol):
    """
    Enemy instances that appear in the game.
    """
    @property
    def base_hp(self) -> int:
        ...
    @property
    def hp(self) -> int:
        ...
    @property
    def size(self) -> int:
        ...
    @property
    def color(self) -> Color:
        ...
    @property
    def is_dead(self) -> bool:
        ...
    @property
    def curr_node(self) -> Node:
        """
        Enemy knows what Node it is on.
        """
        ...
    @property
    def exp(self) -> int:
        ...
    def move(self, node: Node):
        ...
    def valid_shot(self, damage: int):
        ...

class GridConstruct(Protocol):
    """
    Parent class of all entities that use the grid(Shooter, Tower, Tunnel, Bonus Feature: Building).
    """
    @property
    def size(self) -> int:
        """
        Size multiplier.
        Base size is one tile size (15x15).
        """
        ...
    @property
    def coords(self) -> Coord:
        ...

class Tower(Protocol):
    """
    Parent class all Towers.
    """
    @property
    def size(self) -> int:
        ...
    @property
    def bullet_type(self) -> BulletType:
        ...
    @property
    def coords(self) -> Coord:
        ...
    @property
    def direction(self) -> Direction:
        ...
    def set_direction(self, direction: Direction):
        ...
