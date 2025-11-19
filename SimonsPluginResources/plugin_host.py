from typing import Type

from SimonsPluginResources.custom_logging.log_message_factory import LogMessageFactory
from SimonsPluginResources.custom_logging.sources import LogMessageSource
from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin import Plugin
from SimonsPluginResources.plugin_request import PluginRequest


class PluginHost:
    def __init__(self, environment: Environment):
        self.version: int = 10
        self.environment = environment
        logging_source: LogMessageSource = LogMessageSource("[Plugin Host]", "Core/PluginHost")
        self.logging: LogMessageFactory = LogMessageFactory(logger=self.environment.logger, source=logging_source)
        self.loaded_plugins: dict[str, Plugin] = {}
        self.open_plugin_requests: dict[PluginRequest, Plugin] = {}

    async def add_plugin(self, plugin: Type[Plugin], autostart: bool = True) -> None:
        self.logging.log(f"Adding new plugin")
        instance: Plugin = plugin(self)
        #TODO handle plugin requests
        self.loaded_plugins[instance.plugin_id] = instance
        if autostart:
            await instance.start()
        self.logging.log(f"Finished adding new plugin")

    async def remove_plugin(self, plugin: Type[Plugin]) -> None:
        raise NotImplementedError

    def get_loaded_plugin(self, plugin_request: PluginRequest) -> Plugin:
        plugin_id = plugin_request.plugin_id
        self.logging.log(f"Getting loaded plugin {plugin_id}")
        self.logging.log(f"Loaded plugins: {self.loaded_plugins}")
        return self.loaded_plugins.get(plugin_id)

    def get_loaded_plugins(self) -> list["Plugin"]:
        return list(self.loaded_plugins.values())


