import asyncio
from asyncio import CancelledError

from SimonsPluginResources.custom_logging.log_message_factory import LogMessageFactory
from SimonsPluginResources.custom_logging.logger import Logger
from SimonsPluginResources.custom_logging.sources import LogMessageSource
from SimonsPluginResources.asyncio_task_wrapper import AsyncTask


class AsyncTaskManager:
    def __init__(self, logger: Logger):
        self.logging: LogMessageFactory = LogMessageFactory(logger, LogMessageSource("[TaskManager]", "Core/TaskManager"))
        self.shutdown_event = asyncio.Event()
        self.waiting_tasks: list[AsyncTask] = []
        self.running_tasks: dict[str, AsyncTask] = {}
        self.unnamed_task_index: int = 0
        self.running: bool = False

    def add_task(self, task_wrapper: AsyncTask):
        """
        Add and schedule a coroutine as a managed task.
        """
        self.logging.info(f"Adding task: {task_wrapper.name}")
        self.waiting_tasks.append(task_wrapper)
        if self.running:
            self.load_waiting_tasks()

    def load_waiting_tasks(self):
        for task_wrapper in self.waiting_tasks:
            self.logging.info(f"Loading task: {task_wrapper.name}")
            if not task_wrapper.name:
                task_wrapper.name = f"unnamed-task-{self.unnamed_task_index}"
                self.unnamed_task_index += 1
            if task_wrapper.name in self.running_tasks.keys():
                raise Exception("Task names must be unique!")
            task_wrapper.task = asyncio.create_task(task_wrapper.target)
            self.running_tasks[task_wrapper.name] = task_wrapper

            def _on_done(wrapper: AsyncTask):
                self.running_tasks.pop(wrapper.name)
                t = wrapper.task
                if t.cancelled():
                    self.logging.info(f"Task {t.get_name()} was cancelled")
                elif t.exception():
                    self.logging.error(f"Task {t.get_name()} raised exception: {t.exception()}")

            task_wrapper.task.add_done_callback(lambda t: _on_done(task_wrapper))

    async def start(self):
        self.load_waiting_tasks()
        self.logging.info("AsyncTaskManager started. Running tasks.")
        self.running = True
        await self.shutdown_event.wait()
        await self.shutdown_all()

    def shutdown_task(self, name:str) -> None:
        task_wrapper = self.running_tasks.get(name)
        task_wrapper.task.cancel()

    async def shutdown_all(self):
        if not self.running_tasks:
            return
        for task_wrapper in self.running_tasks.values():
            self.shutdown_task(task_wrapper.name)
            try:
                await asyncio.gather(task_wrapper.task, return_exceptions=True)
            except CancelledError:
                pass
        self.running_tasks.clear()
        self.logging.info("Shutdown complete, all tasks cancelled.")

    def stop(self):
        self.shutdown_event.set()