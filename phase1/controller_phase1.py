# pyright: strict

from __future__ import annotations

from phase1.model_phase1 import ZumaModelPhase1
from phase1.view_phase1 import ZumaViewPhase1

class ZumaControllerPhase1:
    def __init__(self, model: ZumaModelPhase1, view: ZumaViewPhase1):
        self._model: ZumaModelPhase1 = model
        self._view: ZumaViewPhase1 = view

    
    def start_game(self):
        self._model.prepare_round()
        self._view.start_game(self, self)
    
    def update(self):
        if not self._model.is_game_over:
            click_info = self._view.get_shot_info(self._model.shooter)
            self._model.update(click_info, self._view.delta_time)
            # print(self._view.current_fps)
    
    def draw(self):
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
