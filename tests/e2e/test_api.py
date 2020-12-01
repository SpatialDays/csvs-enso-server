from ensoserver.entrypoints.api import app

from fastapi.testclient import TestClient


def test_update_enso_values():
    client = TestClient(app)
    response = client.put("/enso")
    assert response.status_code == 200
    assert response.headers.get('content-type') == 'application/json'
    assert isinstance(response.json().get('number_enso_values'), int)


def test_get_enso_values():
    client = TestClient(app)
    response = client.get("/enso")
    assert response.status_code == 200
    assert response.headers.get('content-type') == 'text/csv; charset=utf-8'
    assert response.headers.get('content-disposition') == 'attachment;filename=enso.csv'