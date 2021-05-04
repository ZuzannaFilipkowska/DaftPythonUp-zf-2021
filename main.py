from fastapi import FastAPI, Response, status, Request, HTTPException
from pydantic import BaseModel
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi_mako import FastAPIMako

app = FastAPI()
app.__name__ = "templates"
mako = FastAPIMako(app)


# 3.1


@app.get("/hello", response_class=HTMLResponse)
@mako.template("index_mako.html")
def index_static(request: Request):
    date = datetime.now().date()
    setattr(request, "mako", "test")
    return {"curr_date": date}


# 3.2

@app.post("/login_session", status_code=201)
def login(user: str, password: str, response: Response):
    if user != "4dm1n" or password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    random_string = "".join(random.choice(string.ascii_letters) for i in range(20))
    token = random_string
    response.set_cookie(key="session_token", value=token)


@app.post("/login_token", status_code=201)
def get_token(user: str, password: str, response: Response):
    if user != "4dm1n" or password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    random_string = "".join(random.choice(string.ascii_letters) for i in range(20))
    token = random_string
    response.set_cookie(key="session_token", value=token)
    return {"token": token}