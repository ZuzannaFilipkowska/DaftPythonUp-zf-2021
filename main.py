from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class MethodResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/method/{type}")
def get_method(type: str):
    return {"method": f'{type}'.upper()}
