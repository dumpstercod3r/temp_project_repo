# pyright: strict

from __future__ import annotations

from typing import ClassVar
from collections.abc import Callable
from random import Random
from math import sin, cos, sqrt

from phase1.common_types_phase1 import *


class NormalBullet:
    def __init__(self, color: Color, x: float, y: float, angle: float):
        self._color: Color = color
        self._coords = (x, y)
        self._angle = angle
    @property
    def size(self) -> int:
        return 1    
    @property
    def coords(self) -> tuple[float, float]:
        return self._coords
    @property
    def color(self) -> Color:
        return self._color
    @property
    def speed(self) -> int:
        return 5    
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
    def size(self) -> int:
        return 1   
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
    def exp(self) -> int:
        return 1
    def move_to_node(self, node: Node):
        self._curr_node = node
    def valid_shot(self, damage: int):
        self._hp = max(0, self._hp-damage)
        self._is_dead = self._hp == 0

class Shooter:
    def __init__(self, r: int, c: int):
        self._fire_rate: float = 0.9
        self._bullet_type: BulletType = BulletType.NORMAL
        self._coords: Coord = (r, c)
    @property
    def fire_rate(self) -> float:
        return self._fire_rate
    @property
    def bullet_type(self) -> BulletType:
        return self._bullet_type
    @property    
    def size(self) -> int:
        return 1
    @property
    def coords(self) -> Coord:
        return self._coords
    @property
    def resources(self) -> tuple[int, int]:
        return (0, 0)
    

class MapManager:
    def __init__(self, enemy_paths: list[list[list[int]]]):
        self._shooter: Shooter = Shooter(6, 6)
        self._grid_size: Coord = (13, 13)
        self._grid: list[list[Shooter | None]] = []
        self._raw_enemy_paths: list[list[list[int]]] = enemy_paths
        self._enemy_paths: list[Graph] = []
    
    @property
    def shooter(self) -> Shooter:
        return self._shooter

    @property
    def grid(self) -> list[list[Shooter | None]]:
        return self._grid
    
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._enemy_paths
    
    def make_grid(self):
        r, c = self._grid_size
        self._grid = [[None for _ in range(c)] for _ in range(r)]
        self._grid[r//2][c//2] = self._shooter
    
    def make_paths(self):
        self._enemy_paths = []
        
        for enemy_path in self._raw_enemy_paths:
            next_node = None
            path: Graph = []

            for coord in reversed(enemy_path):
                r, c = coord
                curr_node = Node(r, c)
                path.insert(0, curr_node)

                if next_node != None:
                    curr_node.set_connections(next_node)
                
                next_node = curr_node
            
            self._enemy_paths.append(path)

    def prepare_round(self):
        self.make_grid()
        self.make_paths()


class EnemyManager:
    ENEMY_FACTORY: ClassVar[dict[EnemyType, Callable[[Color, Node], Enemy]]
        ] = {
            EnemyType.NORMAL: NormalEnemy,
        }
    
    def __init__(self, enemy_count: int, enemy_types: list[str], colors: list[Color]):
        self._enemy_count: int = enemy_count
        self._enemy_types: list[EnemyType] = [EnemyType(enemy) for enemy in enemy_types]
        self._active_enemies: list[Enemy] = []
        self._enemies_defeated: int = 0
        self._enemy_colors: list[Color] = colors
        self._rng: Random = Random(67)
    
    @property
    def active_enemies(self) -> list[Enemy]:
        return self._active_enemies
    
    def choose_color(self) -> Color:
        return self._enemy_colors[self._rng.randint(0, len(self._enemy_colors)-1)]
    
    def create_enemy(self, start_node: Node) -> Enemy:
        return self.ENEMY_FACTORY[self._enemy_types[self._rng.randint(0, len(self._enemy_types)-1)]](self.choose_color(), start_node)
    
    def spawn(self, enemy_paths: list[Graph]):
        for path in enemy_paths:
            start_node = path[0]

            if not start_node.is_occupied:
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
        
        return False
    
    def got_shot(self, enemy: Enemy, bullet: Bullet) -> bool:
        if enemy.color == bullet.color:
            enemy.valid_shot(bullet.damage)
            if enemy.is_dead:
                self.despawn(enemy)
            return True
        else:
            return False
    
    def prepare_round(self):
        self._active_enemies = []
        self._enemies_defeated = 0


class BulletManager:
    BULLET_FACTORY: ClassVar[dict[BulletType, Callable[[Color, float, float, float], Bullet]]
        ] = {
            BulletType.NORMAL: NormalBullet,
        }

    def __init__(self, colors: list[Color]):
        self._colors: list[Color] = colors
        self._active_bullets: list[Bullet] = []

    @property
    def active_bullets(self) -> list[Bullet]:
        return self._active_bullets
    
    def create_bullet(self, bullet_type: BulletType, color: Color, x: float, y: float, angle: float) -> Bullet:
        bullet = self.BULLET_FACTORY[bullet_type](color, x, y, angle)
        self._active_bullets.append(bullet)
        return bullet
    
    def move_bullet(self, bullet: Bullet, screen_width: int, screen_height: int):
        diagonal_length = sqrt((screen_width ** 2) + (screen_height ** 2))
        change = diagonal_length / bullet.speed
        new_x = bullet.coords[0] + (change * cos(bullet.angle))
        new_y = bullet.coords[1] + (change * sin(bullet.angle))
        bullet.move_bullet_to(new_x, new_y)
    
    def despawn_bullet(self, bullet: Bullet):
        self._active_bullets.remove(bullet)