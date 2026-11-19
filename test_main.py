from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_region_cities():
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_unknown_region():
    response = client.get("/regions/spain")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}


def test_region_cities_post_method_not_allowed():
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_region_cities_in_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/regions/{region}" in response.json()["paths"]


def test_region_monthly_weather():
    response = client.get("/regions/Spain/Seville/January")
    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}