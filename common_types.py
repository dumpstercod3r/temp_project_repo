# pyright: strict

from enum import StrEnum, auto
from typing import Protocol

from model import Node

class Color(StrEnum):
    GREEN = auto()

class EnemyType(StrEnum):
    NORMAL = auto()


class Bullets(Protocol):
    ...
    
class Enemies(Protocol):
    @property
    def size(self) -> int:
        ...
    @property
    def color(self) -> Color:
        ...
    @property
    def curr_node(self) -> Node:
        ...
    @property
    def exp(self) -> int:
        ...
    def move(self, node: Node):
        ...

class Towers(Protocol):
    ...