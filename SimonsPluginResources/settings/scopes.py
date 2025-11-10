class Scope:
    def __init__(self):
        self.name: str = "UNKNOWN"
        self.set_meta()

    def set_meta(self) -> None:
        pass

    def __str__(self):
        return self.name

class GlobalScope(Scope):
    def __init__(self):
        super().__init__()

    def set_meta(self) -> None:
        self.name = "GLOBAL"

    def __str__(self):
        return f"{self.name}"

class PluginScope(Scope):
    def __init__(self, plugin_id: str):
        super().__init__()
        self.plugin_id:str = plugin_id

    def set_meta(self) -> None:
        self.name = "PLUGIN"

    def __str__(self):
        return f"{self.name}:{self.plugin_id}"

class GuildScope(Scope):
    def __init__(self, guild_id: int):
        super().__init__()
        self.guild_id:int = guild_id

    def set_meta(self) -> None:
        self.name = "GUILD"

    def __str__(self):
        return f"{self.name}:{self.guild_id}"

class GuildMemberScope(GuildScope):
    def __init__(self, guild_id: int, member_id: int):
        super().__init__(guild_id)
        self.member_id:int = member_id

    def set_meta(self) -> None:
        self.name = "GUILD/MEMBER"

    def __str__(self):
        return f"{self.name}:{self.guild_id}/{self.member_id}"

class UserScope(Scope):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id:int = user_id

    def set_meta(self) -> None:
        self.name = "USER"

    def __str__(self):
        return f"{self.name}:{self.user_id}"