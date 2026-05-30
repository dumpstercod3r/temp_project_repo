# pyright: strict

from enum import StrEnum, auto
from typing import Protocol


type Coord = tuple[int, int]
type Graph = list[Node]
"""
There are two types of Grids, Ally Grid and Obstacle Grid.
Ally Grid is a Grid containing either Shooter | Tower | None.
Members of Ally Grid can be placed anywhere except on enemy path.
Obstacle Grid is a Grid containing either Tunnels | Buildings | None.
Members of Obstacle Grid can be placed anywhere.
"""
type Grid = list[list[GridConstruct | None]]

class Node:
    """
    Nodes for graph-based traversal.
    Nodes contain info on what enemy is on it and the other nodes the enemy can go to.
    Superimposed on Ally Grid.
    """
    def __init__(self, x: int, y: int):
        self._coords: Coord = (x, y)
        self._occupant: Enemy | None = None
        self._connections: list[Node] = []
    
    @property
    def coords(self) -> Coord:
        return self._coords
    
    @property
    def occupant(self) -> Enemy | None:
        return self._occupant
    
    @property
    def is_occupied(self) -> bool:
        return self._occupant is not None
    
    @property
    def connections(self) -> list[Node]:
        return self._connections

    def occupy(self, enemy: Enemy):
        self._occupant = enemy
    
    def vacate(self):
        self._occupant = None
    
    def set_connections(self, *nodes: Node):
        self._connections.extend(nodes)


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
    def move_to_node(self, node: Node):
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
