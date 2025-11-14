from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import Setting
from .base_filter import SettingFilter

class SettingFilterCollection(SettingFilter):
    def __init__(self, filters:list["SettingFilter"] = []):
        self.filters = filters

    def add_filter(self, new_filter: "SettingFilter") -> None:
        self.filters.append(new_filter)

    def filter(self, setting: "Setting") -> bool:
        if not self.filters:
            return True
        for individual_filter in self.filters:
            if not individual_filter.filter(setting):
                return False
        return True
