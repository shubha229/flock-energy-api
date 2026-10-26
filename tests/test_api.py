
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_search_invalid_meter_returns_empty_results():
    response = client.get(
        "/meters",
        params={"q": "INVALID123", "page": 1}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"] == []
    assert data["total"] == 0


def test_search_rejects_invalid_page():
    response = client.get(
        "/meters",
        params={"q": "J100000", "page": 0}
    )

    assert response.status_code == 422


def test_meter_location_endpoint():
    response = client.get("/meters/J100000/location")

    assert response.status_code == 200

    data = response.json()
    assert data["meter_id"] == "J100000"
    assert "latitude" in data
    assert "longitude" in data


def test_meter_energy_endpoint():
    response = client.get("/meters/J100000/energy")

    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

    if data["data"]:
        reading = data["data"][0]
        assert "timestamp" in reading
        assert "kwh" in reading
        assert "kvah" in reading
        assert "volt_r" in reading

def test_invalid_meter_location_returns_404():
    response = client.get("/meters/INVALID123/location")
    assert response.status_code == 404


def test_invalid_meter_energy_returns_404():
    response = client.get("/meters/INVALID123/energy")
    assert response.status_code == 404