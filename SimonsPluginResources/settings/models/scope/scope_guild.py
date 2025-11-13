from pydantic import BaseModel
from typing import Literal

class ScopeGuild(BaseModel):
    type: Literal["Guild"] = "Guild"
    guild_id: int

    def __str__(self):
        return f"{self.type}.{self.guild_id}"