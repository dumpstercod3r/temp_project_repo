# pyright: strict

from __future__ import annotations

from typing import TypedDict, Protocol
from enum import StrEnum

type Coord = tuple[int, int]
type Graph = list[Node]
type Mechanic = int | Color
type Grid = list[list[GridConstruct | None]]


class RoundInfo(TypedDict):
    colors: list[str]
    tunnel_coords: list[list[int]]
    enemy_count: int
    enemy_types: list[str]
    enemy_max_counter: dict[str, int]
    enemy_appearance_rate: list[float]
    enemy_paths: list[list[list[int]]]
    bullet_types: list[str]
    tower_types: list[str]

class Phase4Info(TypedDict):
    lives: int
    grid_size: list[int]
    rounds: dict[str, RoundInfo]


class Node:
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


class Color(StrEnum):
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    YELLOW = "YELLOW"
    RED = "RED"
    PURPLE = "PURPLE"

class Direction(StrEnum):
    UP = 'UP'
    LEFT = 'LEFT'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'

class EnemyType(StrEnum):
    NORMAL = 'NORMAL'
    REGENERATOR = 'REGENERATOR'
    CHAMELEON = 'CHAMELEON'

class BulletType(StrEnum):
    NORMAL = 'NORMAL'

class TowerType(StrEnum):
    NORMAL = 'NORMAL'


class Enemy(Protocol):
    @property
    def hp(self) -> int:
        ...
    @property
    def color(self) -> Color:
        ...
    @property
    def is_dead(self) -> bool:
        ...
    @property
    def curr_node(self) -> Node:
        ...
    @property
    def coords(self) -> Coord: 
        ...
    @property
    def exp(self) -> int:
        ...
    @property
    def should_use_mechanic(self) -> bool:
        ...
    @property
    def enemy_type(self) -> EnemyType:
        ...
    def move_to_node(self, node: Node):
        ...
    def use_mechanic(self, var: Mechanic):
        ...
    def got_shot(self, damage: int):
        ...

class Bullet(Protocol):
    @property
    def coords(self) -> tuple[float, float]:
        ...
    @property
    def color(self) -> Color:
        ...
    @property
    def speed(self) -> int:
        ...
    @property
    def angle(self) -> float:
        ...
    @property
    def damage(self) -> int:
        ...
    def move_bullet_to(self, x: float, y: float):
        ...
    def effects(self):
        ...

class GridConstruct(Protocol):
    @property
    def coords(self) -> Coord:
        ...
    @property
    def overlay(self) -> bool:
        ...
    @property
    def resources(self) -> tuple[int, int]:
        ...

class Tower(Protocol):
    @property
    def cost(self) -> int:
        ...
    @property
    def coords(self) -> Coord:
        ...
    @property
    def overlay(self) -> bool:
        ...
    @property
    def bullet_type(self) -> BulletType:
        ...
    @property
    def shooting_speed(self) -> int:
        ...
    @property
    def resources(self) -> tuple[int, int]:
        ...
    @property
    def direction(self) -> Direction:
        ...
    def set_direction(self, direction: Direction):
        ...