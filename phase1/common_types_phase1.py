# pyright: strict

from __future__ import annotations

from typing import TypedDict, Protocol
from enum import StrEnum #, auto


type Coord = tuple[int, int]
type Graph = list[Node]
class Phase1Info(TypedDict):
    lives: int
    rounds: int
    enemy_count: int
    enemy_types: list[str]
    colors: list[str]
    enemy_paths: list[list[list[int]]]
    bullet_types: list[str]


class Color(StrEnum):
    GREEN = 'GREEN'

class BulletType(StrEnum):
    NORMAL = 'NORMAL'

class EnemyType(StrEnum):
    NORMAL = 'NORMAL'

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


class Bullet(Protocol):
    @property
    def size(self) -> int:
        ...
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

class Enemy(Protocol):
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
        ...
    @property
    def coords(self) -> Coord:
        ...
    @property
    def exp(self) -> int:
        ...
    def move_to_node(self, node: Node):
        ...
    def valid_shot(self, damage: int):
        ...