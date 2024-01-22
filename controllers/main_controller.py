import numpy as np

from controllers.model_controller import ModelProvider

from .task_module import task

class MainController:
    def __init__(self, model_controller, user_controller, job_controller, auth_controller) -> None:
        self.model_controller = model_controller
        self.user_controller = user_controller
        self.job_controller = job_controller
        self.auth_controller = auth_controller

        self.models = self.model_controller.get_models()
    
    def submit_task(self, username: str, model_name: str, data_provided: list) -> int: # returns task id, -1 if no money
        model_provider = self.model_controller.get_model(model_name)
        if not self.user_controller.check_balance(username, model_provider.price):
            return -1
        self.user_controller.change_balance(username, -model_provider.price)

        refund_method = lambda: self.user_controller.change_balance(username, model_provider.price)

        job_id = self.job_controller.submit(task, [data_provided, model_provider.instance], username=username, refund=model_provider.price)
        self.user_controller.add_task(username, model_name, data_provided, job_id)
        return job_id

    def get_models(self):
        models = self.model_controller.get_models()
        return models
    
    def get_user(self, username):
        user = self.user_controller.get_user(username)
        return user

    def sign_inup(self, username, password):
        start_balance = 1000
        token = self.auth_controller.sign(username, password, start_balance)
        return token
    
    def get_current_user(self, token):
        return self.auth_controller.get_current_user(token)

