from fastapi import FastAPI, Response
from pydantic import BaseModel
import hashlib


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

# 1.3


@app.get("/auth",  status_code=204)
def password_auth(password=None, password_hash=None):
    if not password_hash or password == "" or password_hash == "" or str(password_hash) != hashlib.sha512(str(password).encode("utf-8")).hexdigest()  or not password:
        return Response(status_code=401)
