import asyncio
import os
import sys
from typing import final, Type, TYPE_CHECKING
from .custom_logging.log_message_factory import LogMessageFactory
from .custom_logging.sources import PluginLogMessageSource
from .plugin_signal import Signal
from .plugin_status import Status
from .settings import Setting
if TYPE_CHECKING:
    from .webinterface_extension import WebinterfaceExtension
    from .plugin_extension import PluginExtension
    from .environment import Environment
    from .plugin_cog import PluginCog
    from .plugin_request import PluginRequest


class Plugin:
    def __init__(self,
                plugin_id:str,
                environment:"Environment",
                name:str = "Not set",
                description:str = "Not set",
                version:int = 0,
                used_host_version:int = 0,
                cogs: list[Type["PluginCog"]] = [],
                plugin_connections: list["PluginRequest"] = [],
            ):
        self.plugin_id: str = plugin_id
        self.name: str = name
        self.description: str = description
        self.version: int = version
        self.needs_backend_version: int = used_host_version
        self.cogs: list[Type["PluginCog"]] = cogs
        self.webinterface_extension: "WebinterfaceExtension" = None
        self.requested_connections: list["PluginRequest"] = plugin_connections

        self.environment: "Environment" = environment
        self.log_factory: "LogMessageFactory" = LogMessageFactory(self.environment.logger, PluginLogMessageSource(self))
        self.plugin_links: dict[str, "Plugin"] = {}
        self.loaded_extensions: list["PluginExtension"] = []

        self.status: "Status" = Status.NOT_STARTED
        self.started:"Signal" = Signal()
        self.stopped:"Signal" = Signal()

    def get_module_path(self) -> str:
        return os.path.dirname(sys.modules[self.__class__.__module__].__file__)

    def get_connection_requests(self, only_required:bool = False) -> list["PluginRequest"]:
        returned_requests = []
        if only_required:
            for request in self.requested_connections:
                if not request.required:
                    continue
                returned_requests.append(request)
        else:
            returned_requests = self.requested_connections
        return returned_requests

    def get_settings(self) -> list["Setting"]:
        return []

    def add_plugin_extension(self, extension: "PluginExtension") -> None:
        extension.set_parent_plugin(self)
        self.loaded_extensions.append(extension)

    def add_plugin_link(self, plugin:"Plugin") -> None:
        self.plugin_links[plugin.plugin_id] = plugin

    def remove_plugin_link(self, plugin:"Plugin") -> None:
        self.plugin_links.pop(plugin.plugin_id, None)

    @final
    def start(self):
        for requested_connection in self.get_connection_requests(True):
            if requested_connection.plugin_id not in self.plugin_links.keys():
                raise Exception(f"Plugin {requested_connection.plugin_id} is required but not found in established links.")
        try:
            self._start()
        except Exception as e:
            raise Exception("Custom start script raised exception: ", e)
        if self.check_bot_ready():
            self.reload_cogs()
        self.status = Status.STARTED
        self.started.emit()

    def _start(self):
        pass

    @final
    def stop(self):
        self._stop()
        self.status = Status.STOPPED
        self.stopped.emit()

    def _stop(self):
        self.unload_cogs()

    def check_bot_ready(self) -> bool:
        if not self.environment.bot:
            return False
        if not self.environment.bot.is_ready():
            return False
        return True

    def reload_cogs(self) -> None:
        if not self.cogs:
            return
        self.log_factory.log(f"Reloading Cogs for Plugin: {self.name}")
        self.unload_cogs()
        self.load_cogs()

    def unload_cogs(self) -> None:
        bot = self.environment.bot
        try:
            for cog_name in bot.cogs.keys():
                future = asyncio.run_coroutine_threadsafe(bot.remove_cog(cog_name), bot.loop)
                future.result(timeout=3)
        except TimeoutError:
            self.log_factory.log(f"Error while reloading Cog: Asyncio Timeout")
        except Exception as e:
            self.log_factory.log(f"Error while reloading Cog: {e}")


    def load_cogs(self) -> None:
        try:
            if not self.environment.bot:
                raise Exception("No bot instance given.")
            if not self.environment.bot.is_ready():
                raise Exception("Bot is not ready.")
        except Exception as e:
            self.log_factory.log(f"Loading Cogs could not be started: {self.name}: {e}")
            return
        bot = self.environment.bot
        for CogObject in self.cogs:
            try:
                cog_instance = CogObject(self)
                future = asyncio.run_coroutine_threadsafe(bot.add_cog(cog_instance), bot.loop)
                future.result(timeout=3)
            except TimeoutError:
                self.log_factory.log(f"Error while reloading Cog: Asyncio Timeout")
            except Exception as e:
                self.log_factory.log(f"Error while reloading Cog: {e}")