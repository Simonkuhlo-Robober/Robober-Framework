from typing import Dict, Optional
from ..filters import SettingFilter
from .base import SettingsStorage
from ..models import Setting

class CacheStorage(SettingsStorage):
    """Stores settings in memory."""

    def __init__(self):
        self._data: Dict[str, Setting] = {}

    def get_list(self, apply_filter: SettingFilter = None) -> list[Setting]:
        if apply_filter is None:
            return list(self._data.values())
        filtered_settings: list[Setting] = []
        for setting in list(self._data.values()):
            if apply_filter.filter(setting):
                filtered_settings.append(setting)
        return filtered_settings

    def get(self, path: str) -> Optional[Setting]:
        return self._data.get(path)

    def set(self, setting: Setting) -> None:
        self._data[setting.path] = setting

    def delete(self, path: str) -> None:
        self._data.pop(path, None)