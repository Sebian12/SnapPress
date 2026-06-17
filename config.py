import json
import os
import sys

# Configuration file path
if hasattr(sys, '_MEIPASS'):
    CONFIG_FILE = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    CONFIG_FILE = "config.json"

# Function to save configuration
def save_config(b_mode, output_folder, thumb_size, preserve_exif, remove_gps):
    config_data = {
        "b_mode": b_mode,
        "output_folder": output_folder,
        "thumb_size": thumb_size,
        "preserve_exif": preserve_exif,
        "remove_gps": remove_gps,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

# Function to load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return {
                    "b_mode": data.get("b_mode", "light"),
                    "output_folder": data.get("output_folder", ""),
                    "thumb_size": data.get("thumb_size", 100),
                    "preserve_exif": data.get("preserve_exif", False),
                    "remove_gps": data.get("remove_gps", False),
                }
        except (json.JSONDecodeError, KeyError):
            pass
    # If file doesn't exist or is corrupted, return default settings
    return {"b_mode": "light", "output_folder": "", "thumb_size": 100, "preserve_exif": False, "remove_gps": False}