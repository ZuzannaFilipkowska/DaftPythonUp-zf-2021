from fastapi import FastAPI, Response, status, Request, HTTPException
from pydantic import BaseModel
import hashlib
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


