from SimonsPluginResources.settings.setting import Setting
from .setting_filter import SettingFilter

class SettingsManager:

    def __init__(self, initial_settings:list[Setting] = []) -> None:
        self.settings:dict[str, Setting] = {}
        self.import_list(initial_settings)

    def get_value_from_path(self, path:str):
        setting = self.settings.get(path)
        if setting:
            return setting.current_value
        return None

    def get_settings(self, settings_filter:SettingFilter = None) -> list[Setting]:
        if settings_filter:
            return settings_filter.filter_ist(list(self.settings.values()))
        else:
            return list(self.settings.values())

    def import_setting(self, setting:Setting) -> None:
        self.settings[setting.get_path()] = setting

    def import_list(self, setting_list:list[Setting]) -> None:
        for setting in setting_list:
            self.import_setting(setting)