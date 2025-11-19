import asyncio
from typing import List, Type
from dotenv import get_key
from SimonsPluginResources.asyncio_task_wrapper import AsyncTask
from SimonsPluginResources.custom_logging.logger import Logger
from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_host import PluginHost
from SimonsPluginResources.reelbot import ReelBot
from SimonsPluginResources.settings import SimpleSettingsManager, SettingsManager, Setting
from SimonsPluginResources.task_manager import AsyncTaskManager

class Launcher:
    def __init__(self, initial_plugins: List[Type[Plugin]] = [], initial_settings: List[Setting] = []) -> None:
        self.logger: Logger = Logger()
        self.task_manager: AsyncTaskManager = AsyncTaskManager(self.logger)
        self.settings: SettingsManager = SimpleSettingsManager()
        self.bot: ReelBot = ReelBot(self.logger, self.settings)
        self.env: Environment = Environment(self.settings, self.logger, self.task_manager, self.bot)
        self.plugin_host: PluginHost = PluginHost(self.env)
        self.bot_task_name: str = "Bot main loop"
        self.initial_plugins: List[Type[Plugin]] = initial_plugins
        self.initial_settings: List[Setting] = initial_settings

    async def main(self, start_bot:bool = True):
        for setting in self.initial_settings:
            self.settings.import_setting(setting)
        if start_bot:
            self.task_manager.add_task(AsyncTask(self.bot.start, args=(get_key(".env", "BOT_TOKEN"),), name=self.bot_task_name))
        for plugin in self.initial_plugins:
            await self.plugin_host.add_plugin(plugin)
        await self.task_manager.start()

    def run_blocking(self, start_bot:bool = True):
        asyncio.run(self.main(start_bot))