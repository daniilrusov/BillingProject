import pickle
import numpy as np


class ModelController:
    def __init__(self, dam) -> None:
        self.dam = dam
        self.models = self.dam.get_models()
        print(self.models)
        self.instances = {}
        for model in self.models:
            self.instances[model.name] = ModelProvider(model.name, model.price, model.path)
    
    def get_model(self, model_name):
        return self.instances[model_name]
    
    def get_models(self):
        return self.models


class ModelProvider:
    def __init__(self, name, price, path) -> None:
        self.name = name
        self.price = price
        self.instance = pickle.load(open(path, 'rb'))
