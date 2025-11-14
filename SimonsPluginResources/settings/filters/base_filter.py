from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import Setting

class SettingFilter:
    def filter(self, setting: "Setting") -> bool:
        return True

    def filter_ist(self, setting_list:list["Setting"]) -> list["Setting"]:
        returned_list: list["Setting"] = []
        for setting in setting_list:
            if self.filter(setting):
                returned_list.append(setting)
        return returned_list