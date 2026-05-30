# pyright: strict

from __future__ import annotations

from collections.abc import Sequence, Callable
from typing import ClassVar
from random import Random

from common_types import Color, Direction, BulletType, EnemyType, TowerType, Bullet, Enemy, GridConstruct, Tower

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
    def connections(self) -> Sequence[Node]:
        return self._connections

    def occupy(self, enemy: Enemy):
        self._occupant = enemy
    
    def vacate(self):
        self._occupant = None
    
    def set_connections(self, *nodes: Node):
        self._connections.extend(nodes)

class NormalBullets:
    def __init__(self, color: Color):
        self._color: Color = color

    @property
    def size(self) -> int:
        return 1
    
    @property
    def color(self) -> Color:
        return self._color

    @property
    def speed(self) -> int:
        return 5
    
    @property
    def damage(self) -> int:
        return 1

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

    def move(self, node: Node):
        self._curr_node = node

    def valid_shot(self, damage: int):
        self._hp = max(0, self._hp-damage)
    
class NormalTower:
    def __init__(self, r: int, c: int):
        self._fire_rate: float = 0.9
        self._bullet_type: BulletType = BulletType.NORMAL
        self._coords: Coord = (r, c)
        self._direction: Direction = Direction.UP

    @property    
    def size(self) -> int:
        return 1

    @property
    def bullet_type(self) -> BulletType:
        return self._bullet_type

    @property
    def coords(self) -> Coord:
        return self._coords

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


class ZumaModelPhase1:
    BULLET_FACTORY: ClassVar[dict[BulletType, Callable[[Color], Bullet]]]

    ENEMY_FACTORY: ClassVar[dict[EnemyType, Callable[[Color, Node], Enemy]]
        ] = {
            EnemyType.NORMAL: NormalEnemy,
        }

    def __init__(self):
        self._lives: int = 2
        self._rounds: int = 1
        self._curr_round: int = 0
        self._colors: list[Color] = [Color.GREEN]                                       # possible enemy colors
        self._base_enemy_num: int = 5
        self._enemy_types: list[EnemyType] = [EnemyType.NORMAL]                         # possible enemies encountered
        self._remaining_Enemy: int = 5                                                # Enemy left to defeat for this round
        self._active_Enemy: list[Enemy] = []                                        # alive enemies on nodes
        self._enemy_paths: list[Graph] = []                                             # list of enemy paths
        self._shooter: Shooter = Shooter(7//2, 7//2)                                    # for phase 1
        self._grid_constructs: list[GridConstruct] = []                                # list of tunnels, buildings, shooter, towers. Basically anything that appears on the grid
        self._Tower: list[Tower] = []                                                 # list of Tower
        self._grid_size: tuple[int, int] = (7, 7)                                       # for phase 1, 7x7 grid
        self._grid: Grid
        self._rng = Random(67)                                                          # remove 67 for actual gameplay

    @property
    def shooter(self) -> Shooter:
        return self._shooter

    @property
    def grid(self) -> Grid:
        return self._grid
    
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._enemy_paths
    
    @property
    def is_round_over(self) -> bool:
        return self._remaining_Enemy == 0
    
    @property
    def is_game_over(self) -> bool:
        return self._curr_round > self._rounds or self._lives == 0

    def make_grid(self):                                                                # currently for phase 1 only
        """
        Self-explanatory.
        Adds Shooter in the middle.
        """
        r, c = self._grid_size

        self._grid = [[None for _ in range(c)] for _ in range(r)]

        self._grid[r//2][c//2] = self._shooter
        # add func to place starting grid constructs
    
    def make_path(self):                                                                # currently for phase 1 only
        """
        Graph-based traversal. Creation here starts from final node to start node.
        Each node knows if it has an occupant | None and knows which nodes are connected to it.
        """
        next_node = None
        path: Graph = []

        for c in range(self._grid_size[1]-1, -1, -1):
            curr_node = Node(1, c)
            path.insert(0, curr_node)
            if next_node is not None:
                next_node.set_connections(curr_node)
            next_node = curr_node
        
        self._enemy_paths.append(path)

    def choose_color(self) -> Color:
        return self._colors[self._rng.randint(0, len(self._colors)-1)]
    
    def create_enemy(self, start_node: Node) -> Enemy:
        """
        Creates Enemies instances based on random EnemyType.
        """
        match self._enemy_types[self._rng.randint(0, len(self._enemy_types)-1)]:
            case EnemyType.NORMAL:
                return NormalEnemy(self.choose_color(), start_node)
        
        raise AssertionError("Unhandled enemy type")

    def spawn_enemy(self):
        """
        Chooses which enemy to create.
        If starting node isn't occupied, enemy will be created and placed in it.
        Additionally, enemy knows it has been moved to starting node.
        """
        for path in self._enemy_paths:
            start_node = path[0]

            if not start_node.is_occupied:
                enemy = self.create_enemy(start_node)
                self._active_Enemy.append(enemy)
                start_node.occupy(enemy)
    
    def despawn_enemy(self, enemy: Enemy):                                            # controller checks if round is over and calls update from model if it is
        """
        Enemy is removed from list of active enemies.
        Counter for remaining enemies decreases.
        """
        self._active_Enemy.remove(enemy)
        self._remaining_Enemy -= 1
    
    def move_enemy(self, enemy: Enemy):
        """
        Enemy either despawns if it has reached the last node, occupies the next vacant node, or does not move.
        Enemy knows whether it has been relocated or not.
        """
        curr_node = enemy.curr_node
        next_nodes = curr_node.connections
        lnen = len(next_nodes)

        if lnen == 0:                                                                   # curr_node is last node
            curr_node.vacate()
            self.despawn_enemy(enemy)
            self._lives = max(0, self._lives - 1)
        elif lnen == 1 and not next_nodes[0].is_occupied:                               # no intersection
            curr_node.vacate()
            next_nodes[0].occupy(enemy)
            enemy.move(next_nodes[0])
        else:                                                                           # with intersection
            for next_node in next_nodes:
                if not next_node.is_occupied:
                    curr_node.vacate()
                    next_node.occupy(enemy)
                    enemy.move(next_node)
                    break
    
    def got_shot(self, enemy: Enemy, bullet: Bullet) -> bool:
        """
        Called when an enemy gets shot by a bullet.
        If enemy is same color as bullet, enemy calculates hit and function returns True.
        If enemy is not of same color, function returns False.
        If bool returned is True, bullet will be despawned.
        If false, bullet passes through.
        """
        if enemy.color == bullet.color:                                                 # same color
            enemy.valid_shot(bullet.damage)
            #bullet.effects() # not sure where to put effects processing (collision handling will prob be in view) # bullet's effects take place, could be explosion, piercing or lightning chain
            
            return True
        else:                                                                           # bullet passes through
            return False
    
    def create_tower(self, tower_type: TowerType, r: int, c: int):
        match tower_type:
            case TowerType.NORMAL:
                return NormalTower(r, c)
        
        raise AssertionError("Unhandled tower type")

    def place_tower(self, tower_type: TowerType, r: int, c: int):
        tower = self.create_tower(tower_type, r, c)

        self._grid_constructs.append(tower)
        self._Tower.append(tower)

    def create_bullet(self, bullet_type: BulletType) -> Bullet:
        color = self.choose_color()

        match bullet_type:
            case BulletType.NORMAL:
                return NormalBullets(color)

        raise AssertionError("Unhandled bullet type")

    def update(self):
        """
        Called everytime it's time for enemies to move or if round is over.
        """
        if self.is_round_over:
            self._curr_round += 1
            # prompt player to place tower, upgrade it or set direction
        else:                                                                           # updates position of all enemies
            for enemy in reversed(self._active_Enemy[:]): # traversing a copy of active enemies in preparation for multihit. Starting from enemy in lead of line then traversing backwards
                self.move_enemy(enemy)
