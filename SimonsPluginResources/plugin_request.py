class PluginRequest:
    def __init__(self, plugin_id:str, plugin_version:int = None, required: bool = False):
        self.plugin_id = plugin_id
        self.plugin_version = plugin_version
        self.required = required