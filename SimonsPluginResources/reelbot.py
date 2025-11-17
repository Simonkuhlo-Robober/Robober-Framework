import discord
from discord.ext import commands
from .plugin_signal import Signal
from .custom_logging import color_templates as colors
from .custom_logging.log_message_factory import LogMessageFactory
from .custom_logging.sources import LogMessageSource

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .custom_logging.logger import Logger
    from .settings import SettingsManager


class ReelBot(commands.Bot):
    def __init__(self, logger: "Logger", settings: "SettingsManager" = None):
        intents = discord.Intents.all()
        intents.message_content = True
        self.settings:SettingsManager = settings
        logging_source = LogMessageSource("[ReelBot]", "Bot")
        self.log_factory = LogMessageFactory(logger, logging_source)
        self.signal_setup:Signal = Signal()
        self.signal_ready:Signal = Signal()
        super().__init__(command_prefix=commands.when_mentioned_or(self.settings.get_value("Global/commands/trigger")), intents=intents)

    async def setup_hook(self) -> None:
        await self.signal_setup.emit()
        guild_id = self.settings.get_value("Global/debug_guild/id")
        if guild_id:
            self.tree.copy_global_to(guild=discord.Object(id=guild_id))
            await self.tree.sync(guild=discord.Object(id=guild_id))

    async def on_ready(self):
        await self.signal_ready.emit()
        message = colors.success('LOGGED IN')+' as '+colors.highlight(f"{self.user}")+f' (ID: {self.user.id})'
        self.log_factory.log(message)