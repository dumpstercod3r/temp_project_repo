# pyright: strict

from __future__ import annotations

from enum import StrEnum
from random import Random

from phase2modified.common_types_phase2 import *
from phase2modified.managers_phase2 import *


class GameState(StrEnum):
    ROUND_SETUP = 'ROUND_SETUP'
    PLAYING = 'PLAYING'
    ROUND_OVER = 'ROUND_OVER'
    WIN = 'WIN'
    LOSE = 'LOSE'


class ZumaModelPhase4:
    