import json

from phase1.model_phase1 import ZumaModelPhase1
from phase1.view_phase1 import ZumaViewPhase1
from phase1.controller_phase1 import ZumaControllerPhase1


with open("settings_phase1.json", "r") as f:
    phase1_info = json.load(f)

controller = ZumaControllerPhase1(ZumaModelPhase1(phase1_info), ZumaViewPhase1())

if __name__ == "__main__":
    controller.start_game()