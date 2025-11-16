from SimonsPluginResources.environment import Environment
from SimonsPluginResources.plugin import Plugin


class PluginInstance:
    def __init__(self, plugin: Plugin, environment: Environment):
        self.plugin = plugin
        self.environment = plugin.environment
        self.plugin_links: dict[str, "Plugin"] = {}