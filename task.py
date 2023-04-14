import argparse
import threading
import uuid
from typing import Optional

from accelerate import notebook_launcher

import instance
from train_network import setup_parser, train


class Task:
    def __init__(self, id: str, task_type: str, config: dict):
        self.id = id
        self.task_type = task_type
        self.config = config
        self.result = None
        self.status = "pending"
        self.error = None
        self.output = []
        self.epoch: int = 0
        self.steps: int = 0
        self.total_steps: int = 0
        self.total_epochs: int = 0
        self.interrupt = False

    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "config": self.config,
            "result": self.result,
            "status": self.status,
            "error": self.error,
            "output": self.output,
            "epoch": self.epoch,
            "steps": self.steps,
            "total_steps": self.total_steps,
            "total_epochs": self.total_epochs,
        }


class TaskPool:
    def __init__(self):
        self.tasks = []
        self.task_count = 0
        self.task_index = 0
        self.current_task: Optional[Task] = None

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.task_count += 1

    def process(self):
        while True:
            if self.task_index < self.task_count:
                print("Processing task %s" % self.task_index)
                self.current_task = self.tasks[self.task_index]
                self.task_index += 1
                self.current_task.status = "running"
                try:
                    parser = setup_parser()
                    config_args = argparse.Namespace(**self.current_task.config)
                    args = parser.parse_args(namespace=config_args)
                    train(args)
                except Exception as e:
                    self.current_task.error = str(e)
                    self.current_task.status = "error"
                    print("Error: %s" % e)
                    continue
                if not self.current_task.interrupt:
                    self.current_task.result = self.current_task.config
                    self.current_task.status = "success"
            else:
                continue

    def run(self):
        print("Starting task pool...")
        thread = threading.Thread(target=self.process, args=())
        thread.start()

    def remove_task_by_id(self, remove_id: int):
        if self.current_task is not None and self.current_task.id == remove_id:
            raise Exception("Cannot remove current task")
        self.tasks = [task for task in self.tasks if task.id != remove_id]

    def interrupt_current_task(self):
        if self.current_task is not None:
            self.current_task.interrupt = True
            self.current_task.status = "interrupted"


def create_task(config):
    uid = str(uuid.uuid4())
    task = Task(uid, "train", config)
    instance.TaskPoolInstance.add_task(task)
    return task



