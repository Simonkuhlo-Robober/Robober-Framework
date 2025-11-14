from pydantic import BaseModel
from .scope import Scope, ScopeGlobal

class Setting(BaseModel):
    rel_path: str
    default_value: str | None
    current_value: str | None = None
    scope: Scope = ScopeGlobal()

    @property
    def value(self):
        if not self.current_value:
            return self.default_value
        return self.current_value

    @property
    def path(self) -> str:
        return f"{self.scope}.{self.rel_path}"