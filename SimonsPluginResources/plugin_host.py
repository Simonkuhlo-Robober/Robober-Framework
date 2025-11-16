from .custom_logging.log_message_factory import LogMessageFactory
from .custom_logging.sources import LogMessageSource
from .plugin import Plugin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SimonsPluginResources.environment import Environment
    from .plugin_request import PluginRequest

class HostPlugin(Plugin):
    def __init__(self, environment: "Environment", host: "PluginHost"):
        super().__init__(
            plugin_id="HOST",
            name="Host Plugin",
            description="This plugin lets you interact with the connected plugin Host",
            version=0,
            used_host_version=1,
            environment=environment,
        )
        self.host = host

    def get_loaded_plugins(self) -> list["Plugin"]:
        return self.host.get_loaded_plugins()

    def get_loaded_plugin(self, request: "PluginRequest") -> Plugin:
        return self.host.get_plugin(request)

class PluginHost:
    def __init__(self, environment: "Environment"):
        self.version: int = 2
        self.environment: "Environment" = environment
        self.loaded_plugins: list[Plugin] = []
        logging_source: LogMessageSource = LogMessageSource("[Plugin Host]", "Core/PluginHost")
        self.log_factory: LogMessageFactory = LogMessageFactory(logger=self.environment.logger, source=logging_source)

        host_plugin = HostPlugin(self.environment, self)
        self.add_plugin(host_plugin)


    def add_plugin(self, plugin: "Plugin"):
        self.log_factory.log(f"Adding plugin {plugin.name}")
        for request in plugin.requested_connections:
            linked_plugin = self.get_plugin(request)
            if linked_plugin:
                plugin.add_plugin_link(linked_plugin)
        for setting in plugin.get_settings():
            self.environment.settings.import_setting(setting)
        self.loaded_plugins.append(plugin)
        try:
            plugin.start()
        except Exception as e:
            self.log_factory.log(f"Failed to autostart plugin {plugin.name}. Try starting it manually or fixing dependencies: {e}")

    def has_plugin(self, plugin_id: str, version:int = None) -> bool:
        for plugin in self.loaded_plugins:
            if not plugin.plugin_id == plugin_id:
                plugin.plugin_version = version
                continue
            if version:
                if not plugin.version == version:
                    continue
            return True
        return False

    def remove_plugin(self, plugin_id: str):
        pass

    def get_loaded_plugins(self) -> list["Plugin"]:
        return self.loaded_plugins.copy()

    def get_plugin(self, plugin_request: "PluginRequest") -> "Plugin":
        for plugin in self.loaded_plugins:
            if plugin.plugin_id == plugin_request.plugin_id:
                return plugin
        return None

    def load_folder(self, folder_path: str):
        pass

    def reload_cogs(self) -> None:
        for plugin in self.loaded_plugins:
            plugin.reload_cogs()