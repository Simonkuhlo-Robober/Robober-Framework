import asyncio
from typing import TYPE_CHECKING, Optional

from SimonsPluginResources.plugin_signal import Signal

if TYPE_CHECKING:
    from SimonsPluginResources.task_manager import AsyncTaskManager
    from SimonsPluginResources.reelbot import ReelBot
    from SimonsPluginResources.settings.settings_manager import SettingsManager
    from SimonsPluginResources.custom_logging.logger import Logger

class Environment:
    def __init__(self, settings: "SettingsManager", logger: "Logger", task_manager: "AsyncTaskManager", bot: Optional["ReelBot"]):
        self.bot = bot
        self.settings = settings
        self.logger = logger
        self.task_manager: "AsyncTaskManager" = task_manager
        self.bot_changed: Signal = Signal()