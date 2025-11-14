from .settings_manager import SettingsManager
from .storage import SettingsStorage, CacheStorage, FileStorage
from .models import Setting, Scope

class SimpleSettingsManager(SettingsManager):
    def __init__(self):
        super().__init__(FileStorage())