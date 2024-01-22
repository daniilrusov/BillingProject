from dataobjects.task import Task
from dataobjects.user import User


class UserController:
    def __init__(self, dam) -> None:
        self.dam = dam

    def get_user(self, username):
        user = self.dam.get_user(username)
        return user
    
    def get_tasks(self, username):
        tasks = self.dam.get_tasks(username=username)
        return tasks

    def create_user(self, username, balance=1000):
        user = User(username, balance, [])
        self.dam.add_user(user)

    def check_balance(self, username, price):
        user = self.get_user(username)
        return user.balance > price
    
    def change_balance(self, username, amount):
        print(f"CHANGING WITH {amount}")
        self.dam.change_balance(username, amount)

    def add_task(self, username, model, data_provided, job_id):
        status = "Submitted"
        task = Task(job_id, model, status, data_provided)
        self.dam.add_task(username, task)

    def get_task(self, job_id):
        task = self.dam.get_task(job_id)
        return task
    
    def change_task_status(self, job_id, status):
        self.dam.update_task(job_id, status)
