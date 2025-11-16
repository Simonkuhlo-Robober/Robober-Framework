from typing import Optional

from SimonsPluginResources.custom_logging.log_message_factory import LogMessageFactory
from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin_request import PluginRequest
from SimonsPluginResources.plugin_signal import Signal
from SimonsPluginResources.plugin_status import Status
from SimonsPluginResources.settings import Setting
from SimonsPluginResources.plugin_extension import PluginExtension

class PluginMeta:
    def __init__(self,
                 plugin_id: str,
                 name: str = "Unnamed Plugin",
                 description: str = "No description provided",
                 version: int = 0,
                 used_backend_version: int = 0,
                 connection_requests: Optional[list[PluginRequest]] = None,
                 settings: Optional[list[Setting]] = None
                 ):
        self.plugin_id:str = plugin_id
        self.name:str = name
        self.description:str = description
        self.version:int = version
        self.used_backend_version:int = used_backend_version
        self.connection_requests:Optional[list[PluginRequest]] = connection_requests
        self.settings: Optional[list[Setting]] = settings

class Plugin:
    def __init__(self,
                 environment: Environment,
                 metadata: PluginMeta,
                 ):
        self.environment = environment
        self.metadata = metadata

        self.plugin_links: dict[str, "Plugin"] = {}
        self.loaded_extensions: list["PluginExtension"] = []
        self.logging = LogMessageFactory(environment.logger)

        self.status: "Status" = Status.NOT_STARTED
        self.started: "Signal" = Signal()
        self.stopped: "Signal" = Signal()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def load_cogs(self) -> None:
        pass

    def unload_cogs(self) -> None:
        pass

    def reload_cogs(self) -> None:
        pass

    def create_tasks(self) -> None:
        pass

    def remove_tasks(self) -> None:
        pass
