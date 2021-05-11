from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_method_post():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}


def test_method_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_method_put():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_method_options():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


def test_method_delete():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


def test_password_auth_correct():
    response = client.get("/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204


def test_password_auth_incorrect():
    response = client.get("/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401


def test_password_auth_empty():
    response = client.get("/auth?password=&password_hash=cos")
    assert response.status_code == 401

    response = client.get("/auth?password_hash=cos")
    assert response.status_code == 401

    response = client.get("/auth?password=password&password_hash=")
    assert response.status_code == 401


def test_register_1():
    patient = {
        "name": "Jan",
        "surname": "Kowalski"
    }
    response = client.post("/register", json=patient)
    reg_patient = {
        "id": 1,
        "name": "Jan",
        "surname": "Kowalski",
        "register_date": "2021-04-20",
        "vaccination_date": "2021-05-01"
    }
    assert response.status_code == 201
    assert response.json() == reg_patient


def test_register_2():
    patient = {
        "name": "Karol",
        "surname": "Kowalski"
    }
    response = client.post("/register", json=patient)
    reg_patient = {
        "id": 2,
        "name": "Karol",
        "surname": "Kowalski",
        "register_date": "2021-04-20",
        "vaccination_date": "2021-05-03"
    }
    assert response.status_code == 201
    assert response.json() == reg_patient


def test_get_patient_1():
    response = client.get("/patient/1")
    assert response.status_code == 200
    reg_patient = {
        "id": 1,
        "name": "Jan",
        "surname": "Kowalski",
        "register_date": "2021-04-20",
        "vaccination_date": "2021-05-01"
    }
    assert response.json() == reg_patient



def test_get_patient_incorrect():
    response = client.get("/patient/-1")
    assert response.status_code == 400


def test_get_patient_not_exists():
    response = client.get("/patient/5")
    assert response.status_code == 404
