# pyright: strict

from __future__ import annotations

from typing import TypedDict, Protocol
from enum import StrEnum

type Coord = tuple[int, int]
type Graph = list[Node]
type Grid = list[list[GridConstruct | None]]


class RoundInfo(TypedDict):
    enemy_count: int
    enemy_types: list[str]
    enemy_paths: list[list[list[int]]]
    bullet_types: list[str]
    tower_types: list[str]
class GameInfo(TypedDict):
    lives: int
    grid_size: list[int]
    color: list[str]
    rounds: dict[str, RoundInfo]