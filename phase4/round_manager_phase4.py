# pyright: strict

from __future__ import annotations

from random import Random

from common_types_phase4 import *
from map_manager_phase4 import *
from enemy_manager_phase4 import *
from bullet_manager_phase4 import *
from tower_manager_phase4 import *


class RoundState(StrEnum):
    ROUND_SETUP = "ROUND_SETUP" # not called at all
    PLAYING = "PLAYING"
    ROUND_OVER = "ROUND_OVER"
    

class RoundManager:
    def __init__(self, grid_size: list[int], round_info: RoundInfo):
        self._grid_size: list[int] = grid_size
        self._rng: Random = Random(67)
        self._curr_round: int = 1
        self._colors: list[Color] = [Color(color) for color in round_info['colors']]
        self._bullet_colors_queue: list[Color] = self._rng.sample(self._colors, k=len(self._colors))
        self._round_state: RoundState = RoundState.PLAYING
        self._map_manager: MapManager = MapManager(self._grid_size, round_info["tunnel_coords"], round_info["enemy_paths"])
        self._enemy_manager: EnemyManager = EnemyManager(round_info["enemy_count"], round_info["enemy_types"], self._colors, self._rng)
        self._bullet_manager: BulletManager = BulletManager(self._colors, self._grid_size)
        self._tower_manager: TowerManager = TowerManager()
    
    @property
    def curr_round(self) -> int:
        return self._curr_round
    @property
    def shooter(self) -> Shooter:
        return self._map_manager.shooter
    @property
    def next_bullet_color(self) -> Color:
        if not self._bullet_colors_queue:
            self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        return self._bullet_colors_queue[0]
    @property
    def grid(self) -> Grid:
        return self._map_manager.grid
    @property
    def tunnels(self) -> list[Tunnel]:
        return self._map_manager.tunnels
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._map_manager.enemy_paths
    @property
    def active_enemies(self) -> list[Enemy]:
        return self._enemy_manager.active_enemies
    @property
    def active_bullets(self) -> list[Bullet]:
        return self._bullet_manager.active_bullets
    @property
    def active_towers(self) -> list[Tower]:
        return self._tower_manager.active_towers
    @property
    def round_state(self) -> RoundState:
        return self._round_state
    
    def prepare_round(self, round_info: RoundInfo, exp: int):
        # called only when curr_round is not 1
        # refreshes RoundManager
        # updates managers with new info
        self._curr_round += 1
        self._colors = [Color(color) for color in round_info['colors']]
        self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        self._map_manager.prepare_round(round_info["enemy_paths"], round_info["tunnel_coords"])
        self._enemy_manager.prepare_round(round_info["enemy_count"], round_info["enemy_types"], self._colors)
        self._bullet_manager.prepare_round(self._colors)
        self._tower_manager.prepare_round(exp) # fix buying mechanics
        self._round_state = RoundState.PLAYING
    
    def shoot(self, x: float, y: float, angle: float):
        self._bullet_manager.create_bullet(self.shooter.bullet_type, self.pop_next_bullet_color(), x, y, angle)
    
    def pop_next_bullet_color(self) -> Color:
        if not self._bullet_colors_queue:
            self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        return self._bullet_colors_queue.pop(0)

    def hit_enemy(self, enemy: Enemy, bullet: Bullet) -> int:
        despawn_bullet = self._enemy_manager.got_shot(enemy, bullet)
        if despawn_bullet:
            self._bullet_manager.despawn(bullet)
            if enemy.is_dead:
                return enemy.exp
        return 0
      
    def bullet_enemy_collision(self):
        def is_colliding(bullet: Bullet, enemy: Enemy):
            buffer = 3
            if ((enemy.coords[0] * 16) - buffer <= bullet.coords[0] <= (enemy.coords[0] * 16) + buffer + 16 and 
            (enemy.coords[1] * 16) - buffer <= bullet.coords[1] <= (enemy.coords[1] * 16) + buffer + 16):
                return True
            else:
                return False
        for bullet in self.active_bullets:
            for enemy in self.active_enemies:
                if is_colliding(bullet, enemy):
                    self.hit_enemy(enemy, bullet)
    
    def update_roundstate(self):
        if self._round_state == RoundState.PLAYING and self._enemy_manager.all_enemies_dead:
            self._round_state = RoundState.ROUND_OVER

    def update(self, click_info: tuple[float, float, float] | None, delta_time: float) -> tuple[int, int]:
        # returns exp earned and lives lost
        exp_earned: int = 0
        lives_lost: int = 0

        if self._round_state == RoundState.PLAYING:
            shot = self._bullet_manager.update(self.next_bullet_color, self.shooter.fire_rate, click_info, delta_time)
            if shot:
                self.pop_next_bullet_color()
            lives_lost = self._enemy_manager.update(delta_time)
            self._tower_manager.update()
            self.bullet_enemy_collision()
            self._enemy_manager.spawn(self.enemy_paths)
            self.update_roundstate()
        
        return (exp_earned, lives_lost)