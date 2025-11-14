from pydantic import BaseModel
from typing import Literal

class ScopeGuildMember(BaseModel):
    type: Literal["GuildMember"] = "GuildMember"
    guild_id: int
    user_id: int

    def __str__(self):
        return f"{self.type}.{self.guild_id}:{self.user_id}"