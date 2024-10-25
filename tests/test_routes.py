from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_data():
    response = client.get("/data")
    assert response.status_code == 200

def test_get_data_by_id():
    response = client.get("/data/0")
    assert response.status_code == 200

def test_add_data_entry():
    new_entry = {
        "year": 2023,
        "lat": 37.7749,
        "lon": -122.4194,
        "GWRPM25": 12.5
    }
    response = client.post("/data", json=new_entry)
    assert response.status_code == 200

def test_update_data_entry():
    new_entry = {
        "year": 2020,
        "lat": 0,
        "lon": 0,
        "GWRPM25": 0
    }
    response = client.post("/data", json=new_entry)

    updated_entry = {
        "year": 2023,
        "lat": 37.7749,
        "lon": -122.4194,
        "GWRPM25": 15.0
    }
    response = client.put("/data/0", json=updated_entry)
    assert response.status_code == 200

def test_delete_data_entry():
    response = client.delete("/data/0")
    assert response.status_code == 200
