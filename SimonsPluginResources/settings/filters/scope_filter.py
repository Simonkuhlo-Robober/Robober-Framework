from typing import TYPE_CHECKING
from ..models.scope import Scope
if TYPE_CHECKING:
    from ..models import Setting
from .base_filter import SettingFilter

class SettingFilterScope(SettingFilter):
    def __init__(self, scope: Scope):
        self.scope = scope

    def filter(self, setting: "Setting") -> bool:
        if str(setting.scope) == str(self.scope):
            return True
        return False