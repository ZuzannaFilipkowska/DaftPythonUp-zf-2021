from fastapi import FastAPI, Response, status, Request, HTTPException
import random
import string
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi_mako import FastAPIMako
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends, Cookie

app = FastAPI()
app.__name__ = "templates"
mako = FastAPIMako(app)
security = HTTPBasic()

app.s_token = "token_session"
app.t_token = "token_login"

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
    app.s_token = token
    response.set_cookie(key="session_token", value=token)


@app.post("/login_token", status_code=201)
def get_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    random_string = "".join(random.choice(string.ascii_letters) for i in range(20))
    token = random_string
    app.t_token = token
    return {"token": token}


# 3.3
def welcome_response(format: str = None):
    if format == "json":
        return JSONResponse(content={"message": "Welcome!"})
    if format == "html":
        text = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Welcome!</h1>
        </body>
    </html>
    """
        return HTMLResponse(content=text)
    else:
        return PlainTextResponse(content='Welcome!')


@app.get("/welcome_session")
def welcome(*, response: Response, session_token: str = Cookie(None), format: str = None):
    if session_token != app.s_token:
        raise HTTPException(status_code=401)
    return welcome_response(format)


@app.get("/welcome_token")
def welcome_token(*, response: Response, token: str = Cookie(None), format: str = None):
    if token != app.t_token:
        raise HTTPException(status_code=401)
    return welcome_response(format)
