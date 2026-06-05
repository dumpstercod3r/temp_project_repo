import json

from model_phase2 import ZumaModelPhase2


with open("settings_phase1.json", "r") as f:
    phase2_info = json.load(f)

model = ZumaModelPhase2(phase2_info)