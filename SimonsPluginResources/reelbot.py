import discord
from discord.ext import commands
from .plugin_signal import Signal
from .logging import color_templates as colors
from .logging.log_message_factory import LogMessageFactory
from .logging.sources import LogMessageSource

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .logging.logger import Logger
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
        super().__init__(command_prefix=commands.when_mentioned_or(self.settings.get_value_from_path("CORE.commands.trigger")), intents=intents)

    async def setup_hook(self) -> None:
        self.signal_setup.emit()
        guild_id = self.settings.get_value_from_path("CORE.debug_server.id")
        if guild_id:
            self.tree.copy_global_to(guild=discord.Object(id=guild_id))
            await self.tree.sync(guild=discord.Object(id=guild_id))

    async def on_ready(self):
        self.signal_ready.emit()
        message = colors.success('LOGGED IN')+' as '+colors.highlight(f"{self.user}")+f' (ID: {self.user.id})'
        self.log_factory.log(message)