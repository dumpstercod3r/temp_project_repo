# pyright: strict

from __future__ import annotations

from phase1.model_phase1 import ZumaModelPhase1
from phase1.view_phase1 import ZumaViewPhase1

class ZumaControllerPhase1:
    def __init__(self, model: ZumaModelPhase1, view: ZumaViewPhase1):
        self._model: ZumaModelPhase1 = model
        self._view: ZumaViewPhase1 = view