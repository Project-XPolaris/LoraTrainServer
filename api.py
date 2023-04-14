from fastapi import FastAPI

from instance import TaskPoolInstance
from task import create_task

app = FastAPI()


@app.get("/info")
def info():
    return {
        "success": True,
        "name": "Lora Train API",
    }


@app.post("/train")
def train(config: dict):
    new_task = create_task(config)
    return {
        "success": True,
        "data": {
            "config": config,
            "id": new_task.id,
        }
    }


@app.get("/tasks")
def tasks(status: str = None):
    result = []
    for task in TaskPoolInstance.tasks:
        if status is None or task.status == status:
            result.append(task.to_dict())
    return {
        "success": True,
        "data": result
    }


@app.get("/task/{task_id}")
def task(task_id: str):
    for task in TaskPoolInstance.tasks:
        if task.id == task_id:
            return {
                "success": True,
                "data": task.to_dict()
            }
    return {
        "success": False,
        "data": None
    }

@app.get("/task/{task_id}/interrupt")
def task(task_id: str):
    for task in TaskPoolInstance.tasks:
        if task.id == task_id:
            if task.id == TaskPoolInstance.current_task.id:
                TaskPoolInstance.interrupt_current_task()
                return {
                    "success": True,
                    "data": "task interrupted"
                }

    return {
        "success": False,
        "data": "task not found"
    }