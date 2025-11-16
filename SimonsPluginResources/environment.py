from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager import AsyncTaskManager
    from SimonsPluginResources.reelbot import ReelBot
    from SimonsPluginResources.settings.settings_manager import SettingsManager
    from SimonsPluginResources.custom_logging.logger import Logger

class Environment:
    def __init__(self, bot: "ReelBot", settings: "SettingsManager", logger: "Logger", task_manager: "AsyncTaskManager"):
        self.bot = bot
        self.settings = settings
        self.logger = logger
        self.task_manager = task_manager