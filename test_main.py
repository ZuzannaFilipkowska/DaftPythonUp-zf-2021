from fastapi.testclient import TestClient
from main import app

# client = TestClient(app)

def test_get_categories():
    with TestClient(app) as client:
        response = client.get("/categories")
        assert response.status_code == 200
        dict = response.json()
        assert dict["categories"][0] == {"id": 1, "name": "Beverages"}



def test_get_client():
    with TestClient(app) as client:
        response = client.get("/customers")
        assert response.status_code == 200
        dict = response.json()
        answer = {
            "id": "ALFKI",
            "name": "Alfreds Futterkiste",
            "full_address":  "Obere Str. 57 12209 Berlin Germany",
        }
        assert dict["customers"][0] == answer
