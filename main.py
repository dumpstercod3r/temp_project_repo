import json

from phase2modified.model_phase2 import ZumaModelPhase2
from phase2modified.view_phase2 import ZumaViewPhase2
from phase2modified.controller_phase2 import ZumaControllerPhase2


with open("settings_phase2.json", "r") as f:
    phase2_info = json.load(f)

controller = ZumaControllerPhase2(ZumaModelPhase2(phase2_info), ZumaViewPhase2())

if __name__ == "__main__":
    controller.start_game()