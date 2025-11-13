from typing import Optional

from .filters import SettingFilter
from .models import Setting
from .storage.base import SettingsStorage


class SettingsManager:
    """Manager layer that mediates between app requests and storage."""

    def __init__(self, storage: SettingsStorage):
        self.storage = storage

    def get_list(self, used_filter: SettingFilter = None):
        return self.storage.get_list(used_filter)

    def get_setting(self, path: str) -> Optional[Setting]:
        return self.storage.get(path)

    def get_value(self, path: str):
        setting = self.storage.get(path)
        if setting is None:
            return None
        return setting.value if setting.value else setting.default_value

    def set_current_value(self, path: str, new_value) -> Optional[Setting]:
        setting = self.storage.get(path)
        if not setting:
            raise KeyError(f"No setting found with path '{path}'")
        setting.current_value = str(new_value)  # ensure string version stored
        self.storage.set(setting)
        return setting

    def import_setting(self, setting: Setting) -> Optional[Setting]:
        if self.get_setting(setting.path):
            return
        self.create_setting(setting)

    def create_setting(self, setting: Setting) -> None:
        if self.storage.get(setting.path):
            raise ValueError(f"Setting '{setting.path}' already exists.")
        self.storage.set(setting)

    def delete_setting(self, path: str) -> None:
        self.storage.delete(path)