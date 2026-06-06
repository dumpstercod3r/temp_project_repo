# pyright: strict

from __future__ import annotations

from phase2modified.model_phase2 import ZumaModelPhase2, GameState
from phase2modified.view_phase2 import ZumaViewPhase2

class ZumaControllerPhase2:
    def __init__(self, model: ZumaModelPhase2, view: ZumaViewPhase2):
        self._model: ZumaModelPhase2 = model
        self._view: ZumaViewPhase2 = view

    
    def start_game(self):
        self._model.prepare_round()
        self._view.start_game(self, self)
    
    def update(self):
        if not (self._model.gamestate == GameState.LOSE or self._model.gamestate == GameState.WIN):
            click_info = self._view.get_shot_info(self._model.shooter)
            self._model.update(click_info, self._view.delta_time)
    
    def draw(self):
        if not (self._model.gamestate == GameState.LOSE or self._model.gamestate == GameState.WIN):
            self._view.reset_screen()
            self._view.draw_grid(self._model.grid)
            for i in self._model.enemy_paths:
                self._view.draw_path(i)
            self._view.draw_shooter(self._model.shooter, self._model.next_bullet_color)
            for i in self._model.active_enemies:
                self._view.draw_enemy(i)
            for i in self._model.active_bullets:
                self._view.draw_bullet(i)
            
            self._view.draw_mouse()
