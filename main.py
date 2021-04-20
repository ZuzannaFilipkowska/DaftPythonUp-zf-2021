from fastapi import FastAPI, Response
from pydantic import BaseModel
import hashlib
import datetime
from datetime import timedelta


app = FastAPI()


class MethodResp(BaseModel):
    msg: str


# 1.1

@app.get("/")
def root():
    return {"message": "Hello world!"}

# 1.2


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
    if not password_hash or password == "" or password_hash == "" or str(password_hash) != hashlib.sha512(str(password).encode("utf-8")).hexdigest() or not password:
        return Response(status_code=401)


# 1.4

app.id = 0


class Patient(BaseModel):
    name: str
    surname: str


class RegisteredPatient(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


def count_letters(word):
    number = 0
    for letter in word:
        if letter.isalpha():
            number += 1
    return number


@app.post('/register', response_model=RegisteredPatient, status_code=201)
def register(patient: Patient):
    app.id += 1
    app.dateTime = datetime.date.today()
    delta = timedelta(days=len(count_letters(patient.name) + count_letters(patient.surname)))
    vacc_date = app.dateTime + delta
    reg_patient = {
            "id": app.id,
            "name": patient.name,
            "surname": patient.surname,
            "register_date": str(app.dateTime),
            "vaccination_date": str(vacc_date)}
    return reg_patient
