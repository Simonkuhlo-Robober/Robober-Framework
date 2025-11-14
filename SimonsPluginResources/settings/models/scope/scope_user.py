from pydantic import BaseModel
from typing import Literal

class ScopeUser(BaseModel):
    type: Literal["User"] = "User"
    user_id: int

    def __str__(self):
        return f"{self.type}.{self.user_id}"