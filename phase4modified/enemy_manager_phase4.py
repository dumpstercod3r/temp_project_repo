# pyright: strict

from __future__ import annotations

from typing import ClassVar
from collections.abc import Callable
from random import Random

from common_types_phase4 import *
    

class NormalEnemy:
    def __init__(self, color: Color, node: Node) -> None:
        self._hp = 1
        self._color: Color = color
        self._is_dead: bool = False
        self._curr_node: Node = node
    @property
    def base_hp(self) -> int:
        return 1
    @property
    def hp(self) -> int:
        return self._hp   
    @property
    def color(self) -> Color:
        return self._color    
    @property
    def is_dead(self) -> bool:
        return self._is_dead 
    @property
    def curr_node(self) -> Node:
        return self._curr_node
    @property
    def coords(self) -> Coord: 
        return self.curr_node.coords
    @property
    def exp(self) -> int:
        return 1
    def move_to_node(self, node: Node):
        self._curr_node = node
    def got_shot(self, damage: int):
        self._hp = max(0, self._hp-damage)
        self._is_dead = self._hp == 0


class EnemyManager:
    ENEMY_FACTORY: ClassVar[dict[EnemyType, Callable[[Color, Node], Enemy]]
        ] = {
            EnemyType.NORMAL: NormalEnemy,
        }

    def __init__(self, enemy_count: int, enemy_types: list[str], colors: list[Color], rng: Random):
        self._rng: Random = rng
        self.prepare_round(enemy_count, enemy_types, colors)
    
    @property
    def active_enemies(self) -> list[Enemy]:
        return self._active_enemies
    @property
    def all_enemies_dead(self) -> bool:
        self._all_enemies_defeated = self._enemy_count == self._enemies_defeated
        return self._all_enemies_defeated
    
    def choose_color(self) -> Color:
        return self._enemy_colors[self._rng.randint(0, len(self._enemy_colors)-1)]
    
    def create_enemy(self, start_node: Node) -> Enemy:
        return self.ENEMY_FACTORY[self._enemy_types[self._rng.randint(0, len(self._enemy_types)-1)]](self.choose_color(), start_node)
    
    def spawn(self, enemy_paths: list[Graph]):
        for path in enemy_paths:
            start_node = path[0]

            if not start_node.is_occupied and self._enemy_count_needed_to_spawn > 0:
                self._enemy_count_needed_to_spawn -= 1
                enemy = self.create_enemy(start_node)
                self._active_enemies.append(enemy)
                start_node.occupy(enemy)
    
    def despawn(self, enemy: Enemy):
        enemy.curr_node.vacate()
        self._active_enemies.remove(enemy)
        self._enemies_defeated += 1

    def move(self, enemy: Enemy) -> bool:
        curr_node = enemy.curr_node
        next_nodes = curr_node.connections
        lnen = len(next_nodes)

        if lnen == 0:
            self.despawn(enemy)
            return True
        elif lnen == 1 and not next_nodes[0].is_occupied:
            curr_node.vacate()
            next_nodes[0].occupy(enemy)
            enemy.move_to_node(next_nodes[0])
        else:
            for next_node in next_nodes:
                if not next_node.is_occupied:
                    curr_node.vacate()
                    next_node.occupy(enemy)
                    enemy.move_to_node(next_node)
                    break
        # print([x.color for x in self._active_enemies])
        return False
    
    def got_shot(self, enemy: Enemy, bullet: Bullet) -> bool:
        if enemy.color == bullet.color:
            enemy.got_shot(bullet.damage)
            if enemy.is_dead:
                self.despawn(enemy)
            return True
        else:
            return False
    
    def update(self, delta_time: float) -> int:
        # each enemy moves after 2 seconds
        # if an self.move returns True, add to lose a life counter and return total amount lost
        total_dmg = 0
        if self._elapsed_time_since_last_enemy_move >= 2.0:
            for i in self._active_enemies:
                if self.move(i):
                    total_dmg += 1
            self._elapsed_time_since_last_enemy_move = 0
        self._elapsed_time_since_last_enemy_move += delta_time
        # print([x.color for x in self._active_enemies])
        return total_dmg
    
    def prepare_round(self, enemy_count: int, enemy_types: list[str], colors: list[Color]):
        self._enemy_count: int = enemy_count
        self._enemy_count_needed_to_spawn: int = self._enemy_count
        self._enemy_types: list[EnemyType] = [EnemyType(enemy) for enemy in enemy_types]
        self._active_enemies: list[Enemy] = []
        self._enemies_defeated: int = 0
        self._enemy_colors: list[Color] = colors
        self._all_enemies_defeated: bool = False
        self._elapsed_time_since_last_enemy_move: float = 0