import asyncio
from queue import Queue

class Hub:
    def __init__(self):
        self.queue = Queue()
        self.all_functions = []

    def register_function(self, limb):
        self.all_functions.append(limb)

    def push_task(self, task_json):
        self.queue.put(task_json)

    async def run(self):
        tasks = []

        while not self.queue.empty():
            task = self.queue.get()
            for function in self.all_functions:
                if function.can_handle(task):
                    # Start task immediately in background
                    t = asyncio.create_task(function.execute(task))
                    tasks.append(t)
                    break

        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(f"Hub received result: {result}")

