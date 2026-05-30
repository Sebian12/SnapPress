import json
import os

CONFIG_FILE = "config.json"

def save_config(b_mode, output_folder):
    config_data = {
        "appearance_mode": b_mode,
        "output_folder": output_folder,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"b_mode": "light", "output_folder": ""}