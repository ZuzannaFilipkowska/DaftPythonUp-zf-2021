from fastapi import FastAPI, Response, status, Request, HTTPException
import random
import string
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
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
    app.s_token = "token_session"
    response.set_cookie(key="session_token", value="token_session")


@app.post("/login_token", status_code=201)
def get_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    app.t_value = "token"
    return {"token": app.t_value}


# 3.3
def welcome_response(format):
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


# 3.4


def goodbye(format):
    if format == "json":
        return JSONResponse(content={"message": "Logged out!"})
    if format == "html":
        text = """
    <html>
        <head>
            <title>More HTML</title>
        </head>
        <body>
            <h1>Logged out!</h1>
        </body>
    </html>
    """
        return HTMLResponse(content=text)
    else:
        return PlainTextResponse(content='Logged out!')


@app.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: str = None):
    if session_token not in app.s_token:
        raise HTTPException(status_code=401)
    for element in app.s_token:
        if session_token == element:
            app.t_token.remove(element)
            break
    if format == 'html':
        return RedirectResponse(url="/logged_out?format=html", status_code=302)
    if format == 'json':
        return RedirectResponse(url="/logged_out?format=json", status_code=302)
    return RedirectResponse(url="/logged_out", status_code=302)


@app.delete("/logout_token")
def logout(token: str = None, format: str = None):
    if token not in app.t_token:
        raise HTTPException(status_code=401)
    for element in app.t_token:
        if token == element:
            app.t_token.remove(element)
            break
    if format == 'html':
        return RedirectResponse(url="/logged_out?format=html", status_code=302)
    if format == 'json':
        return RedirectResponse(url="/logged_out?format=json", status_code=302)
    return RedirectResponse(url="/logged_out", status_code=302)


@app.get("/logged_out")
def logged_out(format: str = None):
    return goodbye(format)
