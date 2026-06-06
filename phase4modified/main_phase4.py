import json

from model_phase4 import ZumaModelPhase4
from view_phase4 import ZumaViewPhase4
from controller_phase4 import ZumaControllerPhase4


with open("settings_phase4.json", "r") as f:
    phase2_info = json.load(f)

controller = ZumaControllerPhase4(ZumaModelPhase4(phase2_info), ZumaViewPhase4())

if __name__ == "__main__":
    controller.start_game()