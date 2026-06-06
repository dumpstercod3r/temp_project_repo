# pyright: strict

from __future__ import annotations

from common_types_phase5 import *


class Tunnel:
    def __init__(self, coords: Coord):
        self._coords = coords
    @property
    def coords(self) -> Coord:
        return self._coords
    @property
    def overlay(self) -> bool:
        return True
    @property
    def resources(self) -> tuple[int, int]:
        return (0, 0) # placeholder
    
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
    def overlay(self) -> bool:
        return False
    @property
    def resources(self) -> tuple[int, int]:
        return (0, 0)
    

class MapManager:
    def __init__(self, grid_size: list[int], tunnel_coords: list[list[int]], raw_enemy_paths: list[list[list[int]]]):
        self._grid_size: list[int] = grid_size
        self._shooter: Shooter = Shooter(self._grid_size[0]//2, self._grid_size[1]//2)
        self.prepare_round(raw_enemy_paths, tunnel_coords)

    @property
    def shooter(self) -> Shooter:
        return self._shooter
    @property
    def grid(self) -> Grid:
        return self._grid
    @property
    def tunnels(self) -> list[Tunnel]:
        return self._tunnels
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._enemy_paths

    def update_restricted_tiles(self, coord: Coord, add: bool):
        if add:
            self._restricted_tiles.add(coord)
        else:
            self._restricted_tiles.discard(coord)
    
    def can_place_tunnel(self, coords: Coord) -> bool:
        return coords in self._restricted_tiles
    
    def make_grid(self, tunnel_coords: list[list[int]]):
        r, c = self._grid_size
        self._grid = [[None for _ in range(c)] for _ in range(r)]
        self._grid[r//2][c//2] = self._shooter
        self.update_restricted_tiles((r, c), True)

        for coord in tunnel_coords:
            r, c = coord
            if self.can_place_tunnel((r, c)):
                self._grid[r][c] = Tunnel((r, c))
    
    def make_paths(self, raw_enemy_paths: list[list[list[int]]]):
        self._enemy_paths = []
        self._raw_enemy_paths = raw_enemy_paths
        
        for enemy_path in self._raw_enemy_paths:
            next_node = None
            path: Graph = []

            for coord in reversed(enemy_path):
                r, c = coord
                curr_node = Node(r, c)
                path.insert(0, curr_node)
                self.update_restricted_tiles((r, c), True)

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
    
    def prepare_round(self, raw_enemy_paths: list[list[list[int]]], tunnel_coords: list[list[int]]):
        self._grid: Grid = []
        self._tunnels: list[Tunnel] = []
        self._restricted_tiles: set[Coord] = set()
        self._enemy_paths: list[Graph] = []
        self.make_paths(raw_enemy_paths)
        self.make_grid(tunnel_coords)