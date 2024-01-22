from dataobjects.task import Task
from dataobjects.user import User
from dataobjects.model import Model
from .models import Task as orm_Task, User as orm_User, Model as orm_Model

from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa


main_engine = sa.create_engine(
    "sqlite:///billing.db",
    echo=False,
)

Session = sessionmaker(bind=main_engine)


class DataAccessModule:
    def __init__(self) -> None:
        self.session = Session()
        
    def get_user(self, username):
        orm_user = self.session.get(orm_User, username)
        tasks = []
        for task in orm_user.tasks:
            tasks.append(Task(task.job_id, task.model, task.status, [task.seqn, task.riagendr, task.paq605, task.bmxbmi, task.lbxglu, task.diq010, task.lbxglt, task.lbxin], task.result))
        user = User(username=orm_user.username, balance=orm_user.balance, tasks=tasks)
        return user
    
    def check_user(self, username):
        orm_user = self.session.get(orm_User, username)
        if orm_user:
            return True
        return False
    
    def get_password(self, username):
        orm_user = self.session.get(orm_User, username)
        return orm_user.password
    
    def add_user(self, username, password, balance):
        orm_user = orm_User(username=username, balance=balance, password=password)
        self.session.add(orm_user)
        self.session.commit()

    def change_balance(self, username, amount):
        orm_user = self.session.get(orm_User, username)
        orm_user.balance = orm_user.balance + amount
        self.session.commit()
    
    def add_task(self, username, task):
        orm_t = self.session.get(orm_Task, task.job_id)
        if orm_t:
            orm_t.model = task.model
            orm_t.username = username
            orm_t.seqn = task.data[0]
            orm_t.riagendr = task.data[1]
            orm_t.paq605 = task.data[2]
            orm_t.bmxbmi = task.data[3]
            orm_t.lbxglu = task.data[4]
            orm_t.diq010 = task.data[5]
            orm_t.lbxglt = task.data[6]
            orm_t.lbxin = task.data[7]
        else:
            orm_user = self.session.get(orm_User, username)
            orm_task = orm_Task(job_id=task.job_id, model=task.model, username=username, status=task.status,
                                seqn=task.data[0], riagendr=task.data[1], paq605=task.data[2], 
                                bmxbmi=task.data[3], lbxglu=task.data[4], diq010=task.data[5], 
                                lbxglt=task.data[6], lbxin=task.data[7])
            orm_user.tasks.append(orm_task)
        self.session.commit()

    def update_task(self, job_id, status,  result=None):
        print(job_id)
        orm_task = self.session.get(orm_Task, job_id)
        if not orm_task:
            orm_task = orm_Task(job_id=job_id, status=status, result=result)
            self.session.add(orm_task)
        else:
            if result:
                orm_task.result = result
            orm_task.status = status
        self.session.commit()

    def get_task(self, job_id):
        orm_task = self.session.get(orm_Task, job_id)
        task = Task(orm_task.job_id, orm_task.model, orm_task.status,
                    [orm_task.seqn, orm_task.riagendr, 
                     orm_task.paq605, orm_task.bmxbmi, 
                     orm_task.lbxglu, orm_task.diq010, 
                     orm_task.lbxglt, orm_task.lbxin])
        return task
    
    def get_models(self):
        orm_models = self.session.query(orm_Model).all()
        print(f"MODELS FROM ORM: {orm_models}")
        models = []
        for model in orm_models:
            models.append(Model(model.name, model.path, model.price))
        print(models)
        return models

    def add_model(self, model):
        try:
            orm_model = orm_Model(name=model.name, path=model.path, price=model.price)
            self.session.add(orm_model)
            self.session.commit()
        except:
            print("already exists")
