from pydantic import BaseModel
from typing import Literal

class ScopePlugin(BaseModel):
    type: Literal["Plugin"] = "Plugin"
    plugin_id: str

    def __str__(self):
        return f"{self.type}.{self.plugin_id}"