import json
import os
import sys

if hasattr(sys, '_MEIPASS'):
    CONFIG_FILE = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    CONFIG_FILE = "config.json"

def save_config(b_mode, output_folder, thumb_size):
    config_data = {
        "b_mode": b_mode,
        "output_folder": output_folder,
        "thumb_size": thumb_size
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return {
                    "b_mode": data.get("b_mode", "light"),
                    "output_folder": data.get("output_folder", ""),
                    "thumb_size": data.get("thumb_size", 100)
                }
        except (json.JSONDecodeError, KeyError):
            pass
    return {"b_mode": "light", "output_folder": "", "thumb_size": 100}