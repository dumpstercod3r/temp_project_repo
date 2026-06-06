import json

from model import ZumaModel
from view import ZumaView
from controller import ZumaController


with open("settings.json", "r") as f:
    info = json.load(f)

controller = ZumaController(ZumaModel(info), ZumaView())

if __name__ == "__main__":
    controller.start_game()