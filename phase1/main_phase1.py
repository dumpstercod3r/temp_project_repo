import json

from phase1.model_phase1 import ZumaModelPhase1


with open("settings_phase1.json", "r") as f:
    phase1_info = json.load(f)

model = ZumaModelPhase1(phase1_info)