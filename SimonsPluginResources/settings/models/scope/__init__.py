from typing import Union
from .scope_guildmember import ScopeGuildMember
from .scope_user import ScopeUser
from .scope_guild import ScopeGuild
from .scope_global import ScopeGlobal
from .scope_plugin import ScopePlugin

Scope = Union[ScopeUser, ScopeGuild, ScopePlugin, ScopeGlobal, ScopeGuildMember]