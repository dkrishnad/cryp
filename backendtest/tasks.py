import threading

class TaskManager:
    def __init__(self):
        self.tasks = {}
    def run_task(self, name, func, *args, **kwargs):
        if name in self.tasks and self.tasks[name].is_alive():
            print(f"Task {name} already running.")
            return
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        self.tasks[name] = thread
    def is_running(self, name):
        return name in self.tasks and self.tasks[name].is_alive()
