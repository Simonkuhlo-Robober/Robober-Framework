import asyncio
from asyncio import AbstractEventLoop
from threading import Thread


class TaskManager:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.tasks: dict[str, TaskManagerTask] = {}
        self.thread = Thread(target=self._start_loop, daemon=True)
        self.task_index: int = 0

    def add_task(self, task: TaskManagerTask, start: bool = True ):
        asyncio.run_coroutine_threadsafe(self._add_task_threadsafe(task, start), self.loop)

    async def _add_task_threadsafe(self, task: TaskManagerTask, start: bool = True):
        if task.parent_manager:
            raise Exception("Trying to add a task that is already being managed by another taskmanager. Remove the task from the other taskmanager first.")
        task.parent_manager = self
        if not task.name:
            task.name = f"unnamed-task-{self.task_index}"
            self.task_index += 1
        self.tasks[task.name] = task
        if start:
            self.start_task(task.name)

    def remove_task(self, task_name:str):
        asyncio.run_coroutine_threadsafe(self._remove_task_threadsafe(task_name), self.loop)

    async def _remove_task_threadsafe(self, task_name: str):
        task = self.tasks.get(task_name)
        if task:
            self.stop_task(task_name)
            self.tasks.pop(task_name)

    def start_task(self, task_name: str):
        task = self.tasks.get(task_name)
        if task:
            task.start()

    def stop_task(self, task_name: str):
        task = self.tasks.get(task_name)
        if task:
            task.stop()

    def _start_loop(self):
        self.loop.run_forever()

    def start(self):
        self.thread.start()

    def start_blocking(self):
        self.start()
        self.thread.join()

    def stop(self):
        for task_name in self.tasks.keys():
            self.stop_task(task_name)
        self.loop.stop()
        self.loop.close()
        self.thread.join(10)


class TaskManagerTask:
    def __init__(self, name:str | None = None):
        self.name: str | None = name
        self.parent_manager: TaskManager | None = None
        self.thread = Thread(target=self._main_loop_start, daemon=True)

    @property
    def running(self):
        return self.thread.is_alive()

    def _main_loop_start(self):
        raise NotImplementedError

    def _before_stop(self):
        pass

    def start(self):
        if not self.running:
            self.thread.start()

    def stop(self):
        if self.running:
            print("Stopping task event loop!")
            self._before_stop()
            self.thread.join(5)

class ExampleTaskManagerTask(TaskManagerTask):
    def __init__(self, name: str | None = None):
        self.loop:AbstractEventLoop = asyncio.new_event_loop()
        super().__init__(name)

    def _main_loop_start(self):
        print(f"{self.name}: Starting task event loop!")
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _before_stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop.close()

manager = TaskManager()
task1 = ExampleTaskManagerTask("Task1")
task2 = ExampleTaskManagerTask()
manager.start()
manager.add_task(task1)
manager.add_task(task2)
manager.thread.join()
