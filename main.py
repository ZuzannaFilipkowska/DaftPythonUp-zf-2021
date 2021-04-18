from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class MethodResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/method/post", status_code=201)
def get_method_post():
    return {'method: POST'}


@app.get("/method/{type}")
def get_method(type: str):
    return {"method": f'{type}'.upper()}
