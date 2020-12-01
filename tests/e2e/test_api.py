import requests

from ensoserver import config


def test_update_enso_values():
    url = config.get_api_url()
    r = requests.put(f'{url}/enso')
    assert r.status_code == 200
    assert r.headers.get('content-type') == 'application/json'
    assert isinstance(r.json().get('number_enso_values'), int)


def test_get_enso_values(session):
    url = config.get_api_url()
    r = requests.get(f'{url}/enso')
    assert r.status_code == 200
    assert r.headers.get('content-type') == 'text/csv; charset=utf-8'
    assert r.headers.get('content-disposition') == 'attachment;filename=enso.csv'
