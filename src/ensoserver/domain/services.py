import logging
from datetime import datetime
from typing import Tuple, List

import requests
from ensoserver.config import enso_invalid_value, LOG_LEVEL, LOG_FORMAT
from urllib3 import HTTPResponse

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)


def download_enso_values(url: str) -> HTTPResponse:
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(f'HTTP error occurred trying to download enso'
                     f' values: {err}')
        raise DownloadError
    return r.raw


class DownloadError(Exception):
    pass


def decode_enso_line(line: bytes) -> List[str]:
    """
    Deletes extra blank spaces and splits every single value in line
    Args:
        line: encoded line in UTF-8 from enso data file.

    Returns:
    List that contains every single value for that year, being the
    year the first element.
    """
    return " ".join(line.decode('utf-8').split()).split(' ')


def get_enso_interval(data: list) -> Tuple[str, str]:
    enso_interval = data[0]
    enso_start_year = enso_interval[0]
    enso_end_year = enso_interval[1]
    return enso_start_year, enso_end_year


def obtain_enso_data_from_url(url: str) -> Tuple[datetime, float]:

    try:
        enso_data = [decode_enso_line(line) for line in download_enso_values(url)]
        enso_start_year, enso_end_year = get_enso_interval(enso_data)

        for row in enso_data[1:]:
            year = row[0]
            if enso_start_year <= year <= enso_end_year:
                for month, meiv2_value in enumerate(row[1:]):
                    if meiv2_value != enso_invalid_value:
                        yield datetime(year=int(year),
                                       month=month+1,
                                       day=1, hour=0, minute=0, second=0).isoformat(),\
                              float(meiv2_value)
    except DownloadError:
        logger.error('ENSO data could not be obtained.')
