from .settings_manager import SettingsManager
from .storage import SettingsStorage, CacheStorage
from .models import Setting, Scope

class SimpleSettingsManager(SettingsManager):
    def __init__(self):
        super().__init__(CacheStorage())