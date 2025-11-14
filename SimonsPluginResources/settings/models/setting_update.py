from pydantic import BaseModel
from .scope import Scope

class SettingUpdate(BaseModel):
    rel_path: str | None = None
    default_value: str | None = None
    current_value: str | None = None
    description: str | None = None
    comment: str | None = None
    scope: Scope | None = None