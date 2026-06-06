# pyright: strict

from __future__ import annotations

from enum import StrEnum# , auto
from random import Random

from phase2modified.common_types_phase2 import *
from phase2modified.managers_phase2 import *


class GameState(StrEnum):
    ROUND_SETUP = 'ROUND_SETUP'
    PLAYING = 'PLAYING'
    ROUND_OVER = 'ROUND_OVER'
    WIN = 'WIN'
    LOSE = 'LOSE'


class ZumaModelPhase2:
    def __init__(self, phase2_info: Phase2Info):
        self._rng: Random = Random(67)
        self._lives: int = phase2_info['lives']
        self._rounds: dict[str, RoundInfo] = phase2_info['rounds']
        self._max_rounds: int = len(self._rounds) # set to zero for endless
        self._curr_round: int = 1
        self._colors: list[Color] = [Color(color) for color in phase2_info['colors']]
        self._bullet_colors_queue: list[Color] = self._rng.sample(self._colors, k=len(self._colors))
        self._exp: int = 0
        self._gamestate: GameState = GameState.ROUND_SETUP
        self._map_manager: MapManager = MapManager(phase2_info['grid_size'], self._rounds[str(self.curr_round)]['enemy_paths'])
        self._enemy_manager: EnemyManager = EnemyManager(self._rounds[str(self.curr_round)]['enemy_count'], self._rounds[str(self.curr_round)]['enemy_types'], self._colors, self._rng)
        self._bullet_manager: BulletManager = BulletManager(self._colors, [x * 16 for x in phase2_info['grid_size']])
        self._tower_manager: TowerManager = TowerManager()

    @property
    def lives(self) -> int:
        return self._lives
    @property
    def rounds(self) -> dict[str, RoundInfo]:
        return self._rounds
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
    def enemy_paths(self) -> list[Graph]:
        return self._map_manager.enemy_paths
    @property
    def active_enemies(self) -> list[Enemy]:
        return self._enemy_manager.active_enemies
    @property
    def active_bullets(self) -> list[Bullet]:
        return self._bullet_manager.active_bullets
    @property
    def exp(self) -> int:
        return self._exp
    @property
    def gamestate(self) -> GameState:
        return self._gamestate

    def exp_manager(self, exp_lost: int):
        self._exp -= exp_lost

    def prepare_round(self, round_number: int):
        r = str(round_number)
        self._map_manager.prepare_round(self._rounds[r]["enemy_paths"])
        self._enemy_manager.prepare_round(self._rounds[r]["enemy_count"], self._rounds[r]["enemy_types"])
        self._bullet_manager.prepare_round()
        # self.exp_manager(self._tower_manager.prepare_round(self.exp)) # how to buy towers?
        self._gamestate = GameState.PLAYING
    
    def shoot(self, x: float, y: float, angle: float):
        self._bullet_manager.create_bullet(self.shooter.bullet_type, self.pop_next_bullet_color(), x, y, angle)
    
    def pop_next_bullet_color(self) -> Color:
        if not self._bullet_colors_queue:
            self._bullet_colors_queue = self._rng.sample(self._colors, k=len(self._colors))
        return self._bullet_colors_queue.pop(0)

    def hit_enemy(self, enemy: Enemy, bullet: Bullet):
        despawn_bullet = self._enemy_manager.got_shot(enemy, bullet)
        if despawn_bullet:
            self._bullet_manager.despawn(bullet)
            if enemy.is_dead:
                self._exp += enemy.exp
    
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
    
    def lives_manager(self, lost_life: int):
        self._lives = max(0, self._lives-lost_life)

    def update_gamestate(self):
        if self.gamestate == GameState.PLAYING:
            if self._enemy_manager.all_enemies_dead:
                self._gamestate = GameState.ROUND_OVER
            elif self.lives == 0:
                self._gamestate = GameState.LOSE
        elif self.gamestate == GameState.ROUND_OVER:
            if self.curr_round > self._max_rounds:
                self._gamestate = GameState.WIN
            else:
                self._gamestate = GameState.ROUND_SETUP
    
    def end_round(self):
        self._curr_round += 1
        self.update_gamestate()
        if self.gamestate == GameState.ROUND_SETUP:
            self.prepare_round(self._curr_round)
        else:
            self.end_game()
    
    def end_game(self):
        ...

    def update(self, click_info: tuple[float, float, float] | None, delta_time: float):
        if self.gamestate == GameState.PLAYING:
            shot = self._bullet_manager.update(self.next_bullet_color, self.shooter.fire_rate, click_info, delta_time)
            if shot:
                self.pop_next_bullet_color()
            self.lives_manager(self._enemy_manager.update(delta_time))
            self._tower_manager.update()
            self.bullet_enemy_collision()
            self._enemy_manager.spawn(self.enemy_paths)
            self.update_gamestate()
        elif self.gamestate == GameState.ROUND_OVER:
            self.end_round()
        elif self.gamestate == GameState.WIN or self.gamestate == GameState.LOSE:
            self.end_game