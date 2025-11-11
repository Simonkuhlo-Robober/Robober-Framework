from SimonsPluginResources.settings.scopes import Scope
from SimonsPluginResources.settings.setting import Setting


class SettingFilter:
    def filter(self, setting: Setting) -> bool:
        return True

    def filter_ist(self, setting_list:list[Setting]) -> list[Setting]:
        returned_list: list[Setting] = []
        for setting in setting_list:
            if self.filter(setting):
                returned_list.append(setting)
        return returned_list

class SettingPathFilter(SettingFilter):
    def __init__(self, path: str):
        self.path:str = path

    def filter(self, setting: Setting) -> bool:
        if setting.get_path() == self.path:
            return True
        return False

class SettingCategoryFilter(SettingFilter):
    def __init__(self, category: str):
        self.category: str = category

    def filter(self, setting: Setting) -> bool:
        if setting.category == self.category:
            return True
        return False

class SettingScopeFilter(SettingFilter):
    def __init__(self, scope: Scope):
        self.scope: Scope = scope

    def filter(self, setting: Setting) -> bool:
        if str(setting.scope) == str(self.scope):
            return True
        return False

class SettingFilterCollection(SettingFilter):
    def __init__(self, filters:list[SettingFilter | None] = []):
        self.filters = filters

    def add_filter(self, new_filter: SettingFilter) -> None:
        self.filters.append(new_filter)

    def filter(self, setting: Setting) -> bool:
        if not self.filters:
            return True
        for individual_filter in self.filters:
            if not individual_filter.filter(setting):
                return False
        return True
