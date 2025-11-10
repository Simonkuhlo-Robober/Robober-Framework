from discord.ext import commands
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import Plugin

class PluginCog(commands.Cog):
    def __init__(self, parent_plugin: "Plugin"):
        self.parent_plugin = parent_plugin
        self.environment = parent_plugin.environment