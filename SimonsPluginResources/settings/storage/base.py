from typing import Optional
from ..models import Setting
from ..filters import SettingFilter


class SettingsStorage:
    """Abstract storage backend interface."""

    def get_list(self, apply_filter: "SettingFilter" = None) -> list[Setting] | None:
        raise NotImplementedError

    def get(self, path: str) -> Optional[Setting]:
        raise NotImplementedError

    def set(self, setting: Setting) -> None:
        raise NotImplementedError

    def delete(self, path: str) -> None:
        raise NotImplementedError