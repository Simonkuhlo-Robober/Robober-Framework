import json
import os
import tempfile
from typing import Dict, Optional

from discord import NotFound

from ..filters import SettingFilter
from .base import SettingsStorage
from ..models import Setting

class FileStorage(SettingsStorage):
    """Stores settings in a file."""

    def __init__(self, file_path:str = None):
        self.file_path = file_path
        if not self.file_path:
            self.file_path = ".settings.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                file.write("{}")


    def get_list(self, apply_filter: SettingFilter = None) -> list[Setting]:
        with open(self.file_path, "r") as file:
            loaded_dict = json.load(file)
        all_settings:list[Setting] = []
        for serial_setting in loaded_dict.values():
            all_settings.append(Setting.model_validate(serial_setting))
        if apply_filter is None:
            return all_settings
        filtered_settings: list[Setting] = []
        for setting in all_settings:
            if apply_filter.filter(setting):
                filtered_settings.append(setting)
        return filtered_settings

    def get(self, path: str) -> Optional[Setting]:
        with open(self.file_path, "r") as file:
            loaded_dict = json.load(file)
        setting_serial = loaded_dict.get(path)
        if setting_serial is None:
            return None
        return Setting.model_validate(setting_serial)

    def set(self, setting: Setting) -> None:
        with open(self.file_path, "r") as file:
            loaded_dict = json.load(file)
        loaded_dict[setting.path] = setting.model_dump()
        with open(self.file_path, "w") as file:
            json.dump(loaded_dict, file, indent=4)

    def delete(self, path: str) -> None:
        with open(self.file_path, "r") as file:
            loaded_dict = json.load(file)
        loaded_dict.pop(path)
        with open(self.file_path, "w") as file:
            json.dump(loaded_dict, file)