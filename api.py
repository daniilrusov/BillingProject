from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, Header
from fastapi.staticfiles import StaticFiles

from controllers.main_controller import MainController
from controllers.user_controller import UserController
from controllers.job_controller import JobController
from controllers.model_controller import ModelController, ModelProvider
from controllers.auth_controller import AuthController
from data_access.data_access_module import DataAccessModule

from dataobjects.model import Model
from data_access.models import Base, User as orm_User, Model as orm_Model, Task as orm_Task

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

import json
import numpy as np


#Base = declarative_base()
main_engine = sa.create_engine(
"sqlite:///billing.db",
echo=True)

Base.metadata.create_all(main_engine)

dam = DataAccessModule()

if len(dam.get_models()) == 0:
    models = json.load(open("models.json"))
    print(models)
    for item in models['models']:
        dam.add_model(Model(item['name'], item['path'], item['price']))


user_controller = UserController(dam=dam)
job_controller = JobController(dam=dam)
model_controller = ModelController(dam=dam)
auth_controller = AuthController(dam=dam)

main_controller = MainController(model_controller=model_controller, 
                                 user_controller=user_controller, 
                                 job_controller=job_controller,
                                 auth_controller=auth_controller)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_token_from_header(*, token: str = Header(None)) -> str:
    username = main_controller.get_current_user(token)
    return username

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}

@app.get('/user')
def get_user(username: Annotated[str, Depends(get_token_from_header)]):
    #username = 'user1'
    result = main_controller.get_user(username)
    return result

@app.get('/models')
def get_models():
    models_list = main_controller.get_models()
    print(models_list)
    return models_list


class ModelPayload(BaseModel):
    model: str
    seqn: float
    riagendr: float
    paq605: float
    bmxbmi: float
    lbxglu: float
    diq010: float
    lbxglt:float
    lbxin: float

@app.post('/models')
def post_models(model_payload: ModelPayload, username: Annotated[str, Depends(get_token_from_header)]):
    #username = 'user1'
    models = main_controller.get_models()
    found = False
    for model in models:
        if model.name == model_payload.model:
            found = True
    if not found:
        raise HTTPException(status_code=400, detail="no such model go away")

    job_id = main_controller.submit_task(username, model_payload.model, 
                                [model_payload.seqn, model_payload.riagendr, 
                                 model_payload.paq605, model_payload.bmxbmi, 
                                 model_payload.lbxglu, model_payload.diq010,
                                 model_payload.lbxglt, model_payload.lbxin])
    return job_id


class Token(BaseModel):
    access_token: str
    token_type: str

def get_token_from_header(*, token: str = Header(None)) -> str:
    username = main_controller.get_current_user(token)
    return username

@app.post("/user")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    token = main_controller.sign_inup(form_data.username, form_data.password)
    return Token(access_token=token, token_type="bearer")


app.mount("/", StaticFiles(directory="static",html = True), name="static")
