from .plugin_signal import Signal
from .plugin_status import Status
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import Plugin


class PluginExtension:
    def __init__(self, parent_plugin: "Plugin" = None) -> None:
        self._parent_plugin = parent_plugin
        self.plugin_started: Signal = Signal()
        self.plugin_stopped: Signal = Signal()
        self.plugin_changed: Signal = Signal()

    @property
    def parent_plugin(self) -> "Plugin":
        return self._parent_plugin

    @parent_plugin.setter
    def parent_plugin(self, plugin: "Plugin") -> None:
        if self.parent_plugin:
            self.parent_plugin.started.disconnect(self.on_plugin_start)
            self.parent_plugin.stopped.disconnect(self.on_plugin_stop)
        self.parent_plugin = plugin
        self.parent_plugin.started.connect(self.on_plugin_start)
        self.parent_plugin.stopped.connect(self.on_plugin_stop)
        if self.parent_plugin.status == Status.STARTED:
            self.on_plugin_start()
        else:
            self.on_plugin_stop()

    def on_plugin_start(self) -> None:
        self.plugin_started.emit()
        self._start()

    def _start(self) -> None:
        pass

    def on_plugin_stop(self) -> None:
        self.plugin_stopped.emit()
        self._stop()

    def _stop(self) -> None:
        pass