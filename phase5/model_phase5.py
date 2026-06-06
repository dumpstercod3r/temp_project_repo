# pyright: strict

from __future__ import annotations

from enum import StrEnum

from common_types_phase5 import *
from round_manager_phase5 import *


class GameState(StrEnum):
    ROUND_SETUP = 'ROUND_SETUP'
    PLAYING = 'PLAYING'
    ROUND_OVER = 'ROUND_OVER'
    WIN = 'WIN'
    LOSE = 'LOSE'


class ZumaModelPhase4:
    def __init__(self, phase4_info: Phase4Info):
        self._lives: int = phase4_info['lives']
        self._grid_size: list[int] = phase4_info['grid_size']
        self._exp: int = 0
        self._gamestate: GameState = GameState.ROUND_SETUP
        self._rounds: dict[str, RoundInfo] = phase4_info['rounds']
        self._round_manager: RoundManager = RoundManager(self._grid_size, self._rounds["1"])

    @property
    def total_rounds(self) -> int:
        return len(self._rounds)
    @property
    def curr_round(self) -> int: # at least 1 when round is playing
        return self._round_manager.curr_round
    @property
    def round_state(self) -> RoundState:
        return self._round_manager.round_state
    @property
    def grid(self) -> Grid:
        return self._round_manager.grid
    @property
    def tunnels(self) -> list[Tunnel]:
        return self._round_manager.tunnels
    @property
    def enemy_paths(self) -> list[Graph]:
        return self._round_manager.enemy_paths
    @property
    def active_enemies(self) -> list[Enemy]:
        return self._round_manager.active_enemies
    @property
    def active_bullets(self) -> list[Bullet]:
        return self._round_manager.active_bullets
    @property
    def active_towers(self) -> list[Tower]:
        return self._round_manager.active_towers
    @property
    def exp(self) -> int:
        return self._exp
    @property
    def gamestate(self) -> GameState:
        return self._gamestate
    
    def prepare_round(self):
        if self.curr_round > 1:
            self._round_manager.prepare_round(self._rounds[str(self.curr_round+1)], self._exp)
        self._gamestate = GameState.PLAYING
    
    def exp_manager(self, exp_gained: int):
        self._exp += exp_gained
    
    def lives_manager(self, lost_life: int):
        self._lives = max(0, self._lives-lost_life)        

    def update_gamestate(self):
        if self._gamestate == GameState.PLAYING:
            if self.round_state == RoundState.ROUND_OVER:
                self._gamestate = GameState.ROUND_OVER
            elif self._lives == 0:
                self._gamestate = GameState.LOSE
        elif self._gamestate == GameState.ROUND_OVER:
            if self.curr_round < self.total_rounds:
                self._gamestate = GameState.ROUND_SETUP
            else:
                self._gamestate = GameState.WIN
    
    def end_round(self):
        self.update_gamestate()
        if self.gamestate == GameState.ROUND_SETUP:
            self.prepare_round()
        else:
            self.end_game()
    
    def end_game(self):
        ...

    def update(self, click_info: tuple[float, float, float] | None, delta_time: float):
        if self.gamestate == GameState.PLAYING:
            exp_gained, lives_lost = self._round_manager.update(click_info, delta_time)
            self.exp_manager(exp_gained)
            self.lives_manager(lives_lost)
            self.update_gamestate()
        elif self.gamestate == GameState.ROUND_OVER:
            self.end_round()
        elif self.gamestate == GameState.LOSE:
            self.end_game()