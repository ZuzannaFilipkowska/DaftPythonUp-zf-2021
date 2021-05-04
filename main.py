from fastapi import FastAPI, Response, status, Request, HTTPException
from pydantic import BaseModel
import hashlib
from datetime import date, datetime, timedelta
from typing import Dict, Optional, List
from fastapi import Query
from fastapi.responses import HTMLResponse


class Patient(BaseModel):
    id: Optional[int]
    name: str
    surname: str
    register_date: Optional[date]
    vaccination_date: Optional[date]

    def __init__(self, **data):
        super().__init__(
            register_date=datetime.now().date(),
            vaccination_date=datetime.now().date()
            + timedelta(
                days=Patient.vaccination_timedelta(
                    data.get("name"), data.get("surname")
                )
            ),
            **data
        )

    @classmethod
    def vaccination_timedelta(cls, name, surname):
        name_letters = "".join(filter(str.isalpha, name))
        surname_letters = "".join(filter(str.isalpha, surname))
        return len(name_letters) + len(surname_letters)


app = FastAPI()
app.counter: int = 1
app.storage: Dict[int, Patient] = {}

# 1.1


@app.get("/")
def root():
    return {"message": "Hello world!"}

# 1.2 lepsze rozwiazanie


@app.api_route(
    path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200
)
def read_request(request: Request, response: Response):
    request_method = request.method

    if request_method == "POST":
        response.status_code = status.HTTP_201_CREATED

    return {"method": request_method}

'''
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
'''
# 1.3


@app.get("/auth")
def auth_request(password: str = "", password_hash: str = ""):
    authorized = False
    if password and password_hash:
        phash = hashlib.sha512(bytes(password, "utf-8")).hexdigest()
        authorized = phash == password_hash
    if authorized:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# 1.4

@app.post('/register', status_code=201)
def create_patient(patient: Patient):
    patient.id = app.counter
    app.storage[app.counter] = Patient
    app.counter += 1
    return patient


# 1.5


@app.get('/patient/{patient_id}')
def show_patient(patient_id: int):
    if patient_id < 1:
        raise HTTPException(status_code=400, detail="Invalid patient id")
    if patient_id not in app.storage:
        raise HTTPException(status_code=404, detail="Patient not found")

    return app.storage.get(patient_id)


######### WEEEK 3 ##########


@app.get("/hello", response_class=HTMLResponse)
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello! Today date is 2001-05-04</h1>
        </body>
    </html>
    """
