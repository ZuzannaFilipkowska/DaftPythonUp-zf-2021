from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class MethodResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.post("/method", status_code=201)
def get_method_post():
    return {"method": "POST"}


@app.get("/method")
def get_method_get():
    return {"method": "GET"}


@app.put("/method")
def get_method_put():
    return {"method": "PUT"}


@app.options("/method")
def get_method_options():
    return {"method": "OPTIONS"}


@app.delete("/method")
def get_method_delete():
    return {"method": "DELETE"}
