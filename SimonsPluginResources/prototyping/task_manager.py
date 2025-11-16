import asyncio
from asyncio import AbstractEventLoop, CancelledError
from SimonsPluginResources.custom_logging.log_message_factory import LogMessageFactory
from SimonsPluginResources.custom_logging.logger import Logger
from SimonsPluginResources.custom_logging.sources import LogMessageSource
from SimonsPluginResources.prototyping.asyncio_task_wrapper import AsyncTask


class AsyncTaskManager:
    def __init__(self, logger: Logger):
        self.logging: LogMessageFactory = LogMessageFactory(logger, LogMessageSource("TaskManager", "Core/TaskManager"))
        self.shutdown_event = asyncio.Event()
        self.running_tasks: dict[str, AsyncTask] = {}
        self.unnamed_task_index: int = 0

    async def _setup(self) -> None:
        pass

    def add_task(self, task_wrapper: AsyncTask) -> asyncio.Task:
        """
        Add and schedule a coroutine as a managed task.
        """
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
                self.logging.log(f"Task {t.get_name()} was cancelled")
            elif t.exception():
                self.logging.log(f"Task {t.get_name()} raised exception: {t.exception()}")

        task_wrapper.task.add_done_callback(lambda t: _on_done(task_wrapper))
        return task_wrapper.task

    async def start(self):
        await self._setup()
        self.logging.log("AsyncTaskManager started; running tasks.")
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
        self.logging.log("Shutdown complete, all tasks cancelled.")

    def stop(self):
        self.shutdown_event.set()