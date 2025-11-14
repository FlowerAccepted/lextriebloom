"""
简单的设置管理器：读写 settings.json
"""
import json
from pathlib import Path

SETTINGS_PATH = Path("settings.json")


def load_settings():
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_settings(settings: dict) -> bool:
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False
