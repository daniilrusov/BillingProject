import numpy as np
from celery import Celery
from data_access.data_access_module import DataAccessModule

app = Celery('tasks', 
             broker='redis://redis:6379/0', 
             backend='redis://redis:6379/0')

app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']

@app.task(bind=True)
def task(self, input: list, instance) -> str:
    print("TASKTASKTASK")
    x = np.array(input).reshape(1, -1)
    if (x < 0).any():
        raise Exception("incorrect data")
    result = instance.predict(x).flatten()[0]
    return self.request.id, result

@app.task()
def result_to_db(id_res, status):
    id, result = id_res
    print(f"STATUS {status}, ID{id}, RESULT{result}")
    dam = DataAccessModule()
    #id = "cd0a72ee-d2b7-4f47-8b98-45872ffb88b6"
    dam.update_task(id, status, result)
    print('DONE')
    return 1

@app.task()
def error_to_db(*args, **kwargs):
    print(args)
    print(kwargs)
    print(kwargs['status'])
    id = args[0].id
    dam = DataAccessModule()
    dam.update_task(id, kwargs['status'])
    dam.change_balance(kwargs['username'], kwargs['refund'])
    return 2
