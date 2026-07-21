import json
import os
import sys
from CTkMessagebox import CTkMessagebox

DEFAULT_EXIF_REMOVE = {"gps": False, "camera": False, "datetime": False, "author": False, "software": False}

# Configuration file path
if hasattr(sys, '_MEIPASS'):
    CONFIG_FILE = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    CONFIG_FILE = "config.json"

_last_save_failed = False

# Function to save configuration
def save_config(appearance_mode, output_folder, thumb_size, preserve_exif, exif_remove):
    global _last_save_failed
    config_data = {
        "appearance_mode": appearance_mode,
        "output_folder": output_folder,
        "thumb_size": thumb_size,
        "preserve_exif": preserve_exif,
        "exif_remove": exif_remove,
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        _last_save_failed = False
    except OSError:
        if not _last_save_failed:
            _last_save_failed = True
            CTkMessagebox(title="ERROR08", message="Could not save config file!", icon="cancel")

# Function to load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

                if "exif_remove" in data:
                    exif_remove = {**DEFAULT_EXIF_REMOVE, **data["exif_remove"]}
                elif "remove_gps" in data:
                    exif_remove = dict(DEFAULT_EXIF_REMOVE)
                    exif_remove["gps"] = data["remove_gps"]
                else:
                    exif_remove = dict(DEFAULT_EXIF_REMOVE)
                
                return {
                    "appearance_mode": data.get("appearance_mode", "light"),
                    "output_folder": data.get("output_folder", ""),
                    "thumb_size": data.get("thumb_size", 100),
                    "preserve_exif": data.get("preserve_exif", False),
                    "exif_remove": exif_remove,
                }
        except (json.JSONDecodeError, KeyError):
            pass
    # If file doesn't exist or is corrupted, return default settings
    return {"appearance_mode": "light", "output_folder": "", "thumb_size": 100, "preserve_exif": False, "exif_remove": dict(DEFAULT_EXIF_REMOVE)}