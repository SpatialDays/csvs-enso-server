import pytest
from ensoserver.domain.services import download_enso_values, DownloadError, \
    decode_enso_line, get_enso_interval, obtain_enso_data_from_url
import responses


def valid_enso_url():
    url = 'http://test.com'
    with open("/tests/meiv2.data", "rb") as enso_file:
        responses.add(
            responses.GET,
            url,
            status=200,
            stream=True,
            body=enso_file.read(),
            headers={'Content-Type': 'text/plain; charset=UTF-8'}
        )
    return url


def invalid_enso_url():
    url = 'http://test.com'
    responses.add(
        responses.GET,
        url,
        status=503,
    )
    return url


@responses.activate
def test_download_enso_values():
    resp = download_enso_values(valid_enso_url())
    assert resp.status == 200


@responses.activate
def test_download_enso_values_raises_download_error():
    with pytest.raises(DownloadError):
        download_enso_values(invalid_enso_url())


def test_decode_enso_line():
    file_line = '1979 1 0.4  0.7   0.2'.encode(encoding='UTF-8')
    line = decode_enso_line(file_line)
    assert line == ['1979', '1', '0.4', '0.7', '0.2']


def test_get_enso_interval():
    enso_first_line = [['1979', '2020'], ['1979', '0.7']]
    start, end = get_enso_interval(enso_first_line)
    assert start == '1979'
    assert end == '2020'


@responses.activate
def test_obtain_enso_data_from_url():
    enso_values = []
    for time_value, meiv2_value in obtain_enso_data_from_url(valid_enso_url()):
        enso_values.append((time_value, meiv2_value))
    assert enso_values


@responses.activate
def test_obtain_enso_data_from_url_download_error():
    enso_values = []
    for time_value, meiv2_value in obtain_enso_data_from_url(invalid_enso_url()):
        enso_values.append((time_value, meiv2_value))
    assert not enso_values
