from pydantic import BaseModel
from typing import Literal

class ScopeGlobal(BaseModel):
    type: Literal["Global"] = "Global"

    def __str__(self):
        return f"{self.type}"