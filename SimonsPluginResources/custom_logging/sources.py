from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SimonsPluginResources.plugin import Plugin

class LogMessageSource:
    def __init__(self, label: str = "[Unknown]", path: str = ""):
        self.label = label
        self.path = path

    def __str__(self):
        return self.label

class PluginLogMessageSource(LogMessageSource):
    def __init__(self, plugin: "Plugin"):
        super().__init__(
            label=plugin.name,
            path=f"Plugins/{plugin.plugin_id}"
        )