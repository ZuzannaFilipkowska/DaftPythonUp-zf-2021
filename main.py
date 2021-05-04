from fastapi import FastAPI, Response, status, Request, HTTPException
from pydantic import BaseModel
import random
import string
from datetime import datetime
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi_mako import FastAPIMako
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends

app = FastAPI()
app.__name__ = "templates"
mako = FastAPIMako(app)
security = HTTPBasic()


# 3.1


@app.get("/hello", response_class=HTMLResponse)
@mako.template("index_mako.html")
def index_static(request: Request):
    date = datetime.now().date()
    setattr(request, "mako", "test")
    return {"curr_date": date}


# 3.2

@app.post("/login_session", status_code=201)
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    random_string = "".join(random.choice(string.ascii_letters) for i in range(20))
    token = random_string
    response.set_cookie(key="session_token", value=token)


@app.post("/login_token", status_code=201)
def get_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    random_string = "".join(random.choice(string.ascii_letters) for i in range(20))
    token = random_string
    response.set_cookie(key="session_token", value=token)
    return {"token": token}