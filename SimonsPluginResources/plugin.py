import asyncio
from typing import Optional, TYPE_CHECKING, Type
from discord.ext import commands
from SimonsPluginResources.custom_logging.log_message_factory import LogMessageFactory
from SimonsPluginResources.custom_logging.sources import PluginLogMessageSource
from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_signal import Signal
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.asyncio_task_wrapper import AsyncTask
from SimonsPluginResources.settings import Setting

if TYPE_CHECKING:
    from SimonsPluginResources.plugin_host import PluginHost

class PluginMeta:
    def __init__(self, plugin_id: str):
        self.plugin_id:str = plugin_id
        self.name:str = "Unnamed Plugin"
        self.description:str = "No description provided"
        self.version:int = 0
        self.used_backend_version:int = 0
        self.connection_requests:Optional[list[PluginRequest]] = None
        self.settings: Optional[list[Setting]] = None

class Plugin:
    def __init__(self, host: "PluginHost", metadata: PluginMeta):
        self.host: "PluginHost" = host
        self.metadata: Optional[PluginMeta] = metadata

        self.plugin_links: dict[str, "Plugin"] = {}
        self.running_tasks: list["AsyncTask"] = []
        self.logging = LogMessageFactory(self.environment.logger, PluginLogMessageSource(self))
        self.environment.bot.signal_ready.connect(self.on_bot_ready)

        self.status: "Status" = Status.NOT_STARTED
        self.started: "Signal" = Signal()
        self.stopped: "Signal" = Signal()

    @property
    def plugin_id(self) -> str:
        return self.metadata.plugin_id

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def description(self) -> str:
        return self.metadata.description

    @property
    def version(self) -> int:
        return self.metadata.version

    @property
    def used_backend_version(self) -> int:
        return self.metadata.used_backend_version

    @property
    def connection_requests(self) -> Optional[list[PluginRequest]]:
        return self.metadata.connection_requests

    @property
    def settings(self) -> Optional[list[Setting]]:
        return self.metadata.settings

    @property
    def environment(self) -> "Environment":
        return self.host.environment

    @property
    def tasks(self) -> Optional[list[AsyncTask]]:
        return None

    @property
    def cogs(self) -> Optional[list[Type[commands.Cog]]]:
        return None

    async def on_bot_ready(self) -> None:
        if self.status == Status.STARTED:
            await self.reload_cogs()

    async def start(self) -> None:
        self.logging.info(f"Starting...")
        try:
            self.import_settings()
            await self.load_cogs()
            self.create_tasks()
        except Exception as e:
            self.logging.error(f"Failed to start plugin: {e}")
            self.status = Status.ERROR
        self.status = Status.STARTED

    async def stop(self) -> None:
        self.logging.log(f"Stopping...")
        try:
            await self.unload_cogs()
            self.remove_tasks()
        except Exception as e:
            self.logging.error(f"Failed to stop plugin: {e}")
            self.status = Status.ERROR
        self.status = Status.STOPPED

    def import_settings(self) -> None:
        for setting in self.settings:
            self.environment.settings.import_setting(setting)

    async def load_cogs(self) -> None:
        try:
            if not self.environment.bot:
                raise Exception("No bot instance given.")
            if not self.environment.bot.is_ready():
                raise Exception("Bot is not ready.")
        except Exception as e:
            self.logging.error(f"Loading Cogs could not be started: {e}.")
            return
        bot = self.environment.bot
        for CogObject in self.cogs:
            try:
                cog_instance = CogObject(self)
                await bot.add_cog(cog_instance)
            except TimeoutError:
                self.logging.error(f"Error while reloading Cog: Asyncio Timeout")
            except Exception as e:
                self.logging.error(f"Error while reloading Cog: {e}")
            self.logging.debug(f"Loaded Cog: {CogObject.__name__}")
        self.logging.info(f"Loaded {len(self.cogs)} Cogs.")

    async def unload_cogs(self) -> None:
        bot = self.environment.bot
        try:
            for cog_name in bot.cogs.keys():
                future = asyncio.run_coroutine_threadsafe(bot.remove_cog(cog_name), bot.loop)
                future.result(timeout=3)
        except TimeoutError:
            self.logging.error(f"Error while reloading Cog: Asyncio Timeout")
        except Exception as e:
            self.logging.error(f"Error while reloading Cog: {e}")

    async def reload_cogs(self) -> None:
        if not self.cogs:
            return
        self.logging.info(f"Reloading Cogs for Plugin: {self.name}")
        await self.unload_cogs()
        await self.load_cogs()

    def create_tasks(self) -> None:
        if self.tasks is None:
            return
        for task in self.tasks:
            self.environment.task_manager.add_task(task)

    def remove_tasks(self) -> None:
        if self.tasks is None:
            return
        for task in self.tasks:
            self.environment.task_manager.shutdown_task(task.name)

    def check_bot_ready(self) -> bool:
        if not self.environment.bot:
            return False
        if not self.environment.bot.is_ready():
            return False
        return True
