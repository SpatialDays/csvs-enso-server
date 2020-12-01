import os
from logging import INFO

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO

enso_source_url = os.environ.get(
    'ENSO_URL',
    'https://psl.noaa.gov/enso/mei/data/meiv2.data'
)
enso_invalid_value = '-999.00'


def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'ensoserver', 'ensoserver'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 8000 if host == 'localhost' else 80
    return f"http://{host}:{port}"