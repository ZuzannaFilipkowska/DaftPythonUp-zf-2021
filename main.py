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
    return {"method": "POST"}


@app.get("/method/get")
def get_method_get():
    return {"method": "GET"}


@app.get("/method/put")
def get_method_put():
    return {"method": "PUT"}


@app.get("/method/options")
def get_method_options():
    return {"method": "OPTIONS"}


@app.get("/method/delete")
def get_method_delete():
    return {"method": "DELETE"}
