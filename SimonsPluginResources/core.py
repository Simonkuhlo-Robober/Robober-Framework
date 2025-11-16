from typing import TYPE_CHECKING
from threading import Thread
from .custom_logging.logger import Logger
from SimonsPluginResources.environment import Environment
from .plugin_host import PluginHost
from .reelbot import ReelBot
from .settings import SimpleSettingsManager
if TYPE_CHECKING:
    from .settings import Setting


class CoreApp:
    def __init__(self, token: str, initial_settings:list["Setting"] | None = None):
        self.settings = SimpleSettingsManager()
        for setting in initial_settings:
            self.settings.import_setting(setting)
        self.logger = Logger()
        self.bot = ReelBot(self.logger, self.settings)
        self.bot.signal_ready.connect(self.on_bot_ready)
        self.environment = Environment(self.bot, self.settings, self.logger)
        self.plugin_host:PluginHost = PluginHost(self.environment)
        self.bot_token: str = token
        self.bot_thread:Thread = Thread(target=self.run_bot, daemon=True)

    def on_bot_ready(self):
        self.plugin_host.reload_cogs()

    def run_bot(self) -> None:
        self.bot.run(self.bot_token)

    def start(self) -> None:
        self.bot_thread.start()
        while True:
            cmd = input("Type /quit to exit: ")
            match cmd.strip():
                case "/quit":
                    print("Exiting...")
                    break
                case "/status bot_thread":
                    print("Bot status: ", self.bot_thread.is_alive())
                case "/plugins reload_cogs":
                    self.plugin_host.reload_cogs()
                case _:
                    print("Unknown command.")