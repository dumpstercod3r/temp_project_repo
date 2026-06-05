# pyright: strict

from __future__ import annotations

from phase1.common_types_phase1 import *
from phase1.managers_phase1 import *
    

class ZumaModelPhase1:
    def __init__(self, phase1_info: Phase1Info):
        self._lives: int = phase1_info['lives']
        self._rounds: int = phase1_info['rounds']
        self._curr_round: int = 0
        self._colors: list[Color] = [Color(color) for color in phase1_info['colors']]
        self._map_manager: MapManager = MapManager(phase1_info['enemy_paths'])
        self._enemy_manager: EnemyManager = EnemyManager(phase1_info['enemy_count'], phase1_info['enemy_types'], self._colors)
        self._bullet_manager: BulletManager = BulletManager(self._colors, 240, 240)
        self._rng: Random = Random(67)
        self._bullet_colors_queue: list[Color] = self._rng.sample(self._colors, k=len(self._colors))
        self._is_game_over: bool = False
        self._exp: int = 0
    
    @property
    def shooter(self) -> Shooter:
        return self._map_manager.shooter
    
    @property
    def grid(self) -> list[list[Shooter | None]]:
        return self._map_manager.grid
    
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
    def next_bullet_color(self) -> Color:
        if not self._bullet_colors_queue:
            self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        return self._bullet_colors_queue[0]

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def exp(self) -> int:
        return self._exp
    
    def shoot(self, x: int, y: int, angle: int):
        self._bullet_manager.create_bullet(self.shooter.bullet_type, self.pop_next_bullet_color(), x, y, angle)
    
    def pop_next_bullet_color(self) -> Color:
        if not self._bullet_colors_queue:
            self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        return self._bullet_colors_queue.pop(0)
    
    def got_hit(self, enemy: Enemy, bullet: Bullet):
        despawn_bullet = self._enemy_manager.got_shot(enemy, bullet)
        if despawn_bullet:
            self._bullet_manager.despawn_bullet(bullet)
            self._exp += enemy.exp

    def lives_manager(self, lost_life: int):
        self._lives = max(0, self._lives-lost_life)

    def prepare_round(self):
        self._map_manager.prepare_round()
        self._enemy_manager.prepare_round()
    
    def check_for_collisions(self):
        def is_colliding(bullet: Bullet, enemy: Enemy):
            if ((enemy.coords[0] * 16) - 8 <= bullet.coords[0] <= (enemy.coords[0] * 16) + 8 and 
            (enemy.coords[1] * 16) - 8 <= bullet.coords[1] <= (enemy.coords[1] * 16) + 8):
                return True
            else:
                return False
        for bullet in self.active_bullets:
            for enemy in self.active_enemies:
                if is_colliding(bullet, enemy):
                    self.got_hit(enemy, bullet)

    def check_if_game_over(self) -> bool:
        return self._enemy_manager.all_enemies_defeated | self._lives == 0

    def update(self, click_info: tuple[float, float, float] | None, current_fps: int):
        if not self.is_game_over:
            self._bullet_manager.update(self.pop_next_bullet_color(), click_info, current_fps)
            self.lives_manager(self._enemy_manager.update())
            self.check_for_collisions()
            self.check_if_game_over()
        else:
            self.end_round()
    
    def end_round(self) -> bool:
        return self._enemy_manager.all_enemies_defeated