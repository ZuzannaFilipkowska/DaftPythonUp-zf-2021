from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class MethodResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/method/{type}", response_model=MethodResp)
def method_type(type: str):
    return MethodResp(msg=f'{type}'.upper())