# pyright: strict

from __future__ import annotations

from collections.abc import Sequence
from random import Random

from common_types import Color, EnemyType, Enemies, Towers

type Coord = tuple[int, int]
type Grid = list[list[Shooter | Towers | None]]

class Node:
    def __init__(self, x: int, y: int):
        self._coords: Coord = (x, y)
        self._occupant: Enemies | None = None
        self._connections: list[Node] = []
    
    @property
    def coords(self) -> Coord:
        return self._coords
    
    @property
    def occupant(self) -> Enemies | None:
        return self._occupant
    
    @property
    def is_occupied(self) -> bool:
        return self._occupant is not None
    
    @property
    def connections(self) -> Sequence[Node]:
        return self._connections

    def occupy(self, enemy: Enemies):
        self._occupant = enemy
    
    def vacate(self):
        self._occupant = None
    
    def set_connections(self, *nodes: Node):
        self._connections.extend(nodes)

class NormalEnemy:
    def __init__(self, color: Color, node: Node) -> None:
        self._color: Color = color
        self._curr_node: Node = node

    @property
    def size(self) -> int:
        return 1
    
    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def curr_node(self) -> Node:
        return self._curr_node
    
    @property
    def exp(self) -> int:
        return 1

    def move(self, node: Node):
        self._curr_node = node

class Shooter:
    ...

        
class ZumaModelPhase1:
    def __init__(self):
        self._lives: int = 2
        self._rounds: int = 1
        self._curr_round: int = 0
        self._colors: list[Color] = [Color.GREEN]
        self._base_enemy_num: int = 5
        self._enemy_types: list[EnemyType] = [EnemyType.NORMAL]
        self._remaining_enemies: int = 5
        self._active_enemies: list[Enemies] = []
        self._enemy_path: list[Node] = []
        self._grid_size: tuple[int, int] = (7, 7)
        self._grid: Grid
        self._rng = Random(67) # remove 67 for final

    @property
    def is_round_over(self) -> bool:
        return self._remaining_enemies == 0
    
    @property
    def is_game_over(self) -> bool:
        return self._curr_round > self._rounds or self._lives == 0

    def make_grid(self):
        r, c = self._grid_size

        self._grid = [[None for _ in range(c)] for _ in range(r)]
        self._grid[r//2][c//2] = Shooter()
    
    def make_path(self):
        """
        Graph-based traversal.
        Each node knows if it has an occupant/None and knows which nodes are connected to it.
        """
        next_node = None
        for c in range(self._grid_size[1]-1, -1, -1):
            curr_node = Node(1, c)
            self._enemy_path.insert(0, curr_node)
            if next_node is not None:
                next_node.set_connections(curr_node)
            next_node = curr_node
    
    def choose_color(self) -> Color:
        return self._colors[self._rng.randint(0, len(self._colors)-1)]
    
    def create_enemy(self, start_node: Node) -> Enemies:
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
        start_node = self._enemy_path[0]

        if not start_node.is_occupied:
            enemy = self.create_enemy(start_node)
            self._active_enemies.append(enemy)
            start_node.occupy(enemy)
    
    def despawn_enemy(self, enemy: Enemies): # controller checks if round is over and calls update from model if it is
        """
        Enemy is removed from list of active enemies.
        Counter for remaining enemies decreases.
        """
        self._active_enemies.remove(enemy)
        self._remaining_enemies -= 1
    
    def move_enemy(self, enemy: Enemies):
        """
        Enemy either despawns if it has reached the last node, occupies the next vacant node, or does not move.
        Enemy knows whether it has been relocated or not.
        """
        curr_node = enemy.curr_node
        next_nodes = curr_node.connections
        lnen = len(next_nodes)

        if lnen == 0: # curr_node is last node
            curr_node.vacate()
            self.despawn_enemy(enemy)
            self._lives = max(0, self._lives - 1)
        elif lnen == 1 and not next_nodes[0].is_occupied: # no intersection
            curr_node.vacate()
            next_nodes[0].occupy(enemy)
            enemy.move(next_nodes[0])
        else: # may intersection
            for next_node in next_nodes:
                if not next_node.is_occupied:
                    curr_node.vacate()
                    next_node.occupy(enemy)
                    enemy.move(next_node)
                    break
    
    def update(self):
        """
        Called everytime it's time for enemies to move or if round is over.
        """
        if self.is_round_over:
            self._curr_round += 1
        else: # updates position of all enemies
            for enemy in reversed(self._active_enemies[:]): # traversing a copy of active enemies in preparation for multihit
                self.move_enemy(enemy)