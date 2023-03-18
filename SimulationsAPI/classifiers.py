import importlib

class Model():
    def __init__(self, model_name, dic_args, import_list):
        self.model = self.get_model(model_name, dic_args, import_list)

    def train(self):
        None
    
    def test(self):
        None



