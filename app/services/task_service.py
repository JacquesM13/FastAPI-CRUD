tasks = []

def create_task(task):
    task_dict = task.dict()
    task_dict["id"] = len(tasks) + 1
    tasks.append(task_dict)
    return task_dict

def get_tasks():
    return tasks


def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(task_id, updated_task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    return None


def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False

