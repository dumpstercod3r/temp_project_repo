# pyright: strict

from __future__ import annotations

from typing import ClassVar
from collections.abc import Callable
from random import Random
from math import sin, cos, sqrt

from phase2modified.common_types_phase2 import *


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
    def bullet_type(self) -> BulletType:
        return BulletType.NORMAL
    @property
    def shooting_speed(self) -> int:
        return 2 # seconds per bullet
    @property
    def resources(self) -> tuple[int, int]:
        return (0, 0) # placeholder
    @property
    def direction(self) -> Direction:
        return self._direction
    def set_direction(self, direction: Direction):
        self._direction = direction

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
    def __init__(self, grid_size: list[int], raw_enemy_paths: list[list[list[int]]]):
        self._grid_size: list[int] = grid_size
        self._shooter: Shooter = Shooter(self._grid_size[0]//2, self._grid_size[1]//2)
        self._grid: Grid = []
        self._restricted_tiles: set[Coord] = set()
        self._raw_enemy_paths: list[list[list[int]]] = raw_enemy_paths
        self._enemy_paths: list[Graph] = []

    @property
    def shooter(self) -> Shooter:
        return self._shooter
    @property
    def grid(self) -> Grid:
        return self._grid
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._enemy_paths

    def update_restricted_tiles(self, coord: Coord, add: bool):
        if add:
            self._restricted_tiles.add(coord)
        else:
            self._restricted_tiles.discard(coord)
    
    def make_grid(self):
        r, c = self._grid_size
        self._grid = [[None for _ in range(c)] for _ in range(r)]
        self._grid[r//2][c//2] = self._shooter
        self.update_restricted_tiles((r, c), True)
    
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
    
    def can_place_tower(self, coord: Coord) -> bool:
        return not(coord in self._restricted_tiles)
    
    def place_tower(self, tower: Tower):
        r, c = tower.coords
        self._grid[r][c]
        self.update_restricted_tiles(tower.coords, True)
    
    def prepare_round(self):
        self.make_grid()
        self.make_paths()
    

class EnemyManager:
    ENEMY_FACTORY: ClassVar[dict[EnemyType, Callable[[Color, Node], Enemy]]
        ] = {
            EnemyType.NORMAL: NormalEnemy,
        }

    def __init__(self, enemy_count: int, enemy_types: list[str], colors: list[Color], rng: Random):
        self._enemy_count: int = enemy_count
        self._enemy_count_needed_to_spawn: int = self._enemy_count
        self._enemy_types: list[EnemyType] = [EnemyType(enemy) for enemy in enemy_types]
        self._active_enemies: list[Enemy] = []
        self._enemies_defeated: int = 0
        self._enemy_colors: list[Color] = colors
        self._all_enemies_defeated: bool = False
        self._rng: Random = rng
        self._elapsed_time_since_last_enemy_move: float = 0
    
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
    
    def prepare_round(self):
        self._active_enemies = []
        self._enemies_defeated = 0
        self._enemy_count_needed_to_spawn = self._enemy_count
        self._all_enemies_defeated = False


class BulletManager:
    BULLET_FACTORY: ClassVar[dict[BulletType, Callable[[Color, float, float, float], Bullet]]
        ] = {
            BulletType.NORMAL: NormalBullet,
        }

    def __init__(self, colors: list[Color], grid_size: list[int]):
        self._colors: list[Color] = colors
        self._active_bullets: list[Bullet] = []
        self._screen_height: int = grid_size[0]
        self._screen_width: int = grid_size[1]

        self._elapsed_time_since_last_bullet: float = 0

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
    
    def prepare_round(self):
        self._active_bullets = []


class TowerManager:
    TOWER_FACTORY: ClassVar[dict[TowerType, Callable[[int, int], Tower]]
        ] = {
            TowerType.NORMAL: NormalTower,
        }
    
    def __init__(self):
        self._active_towers: list[Tower] = []

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
        ...
    
    def update(self):
        # each tower shoots 1 bullet every 2 seconds
        ...