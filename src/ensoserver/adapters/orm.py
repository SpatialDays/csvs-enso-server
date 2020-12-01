from sqlalchemy import Table, DateTime, Column, Float, MetaData
from sqlalchemy.orm import mapper

from ensoserver.domain import model

metadata = MetaData()

enso_values = Table(
    'enso_values', metadata,
    Column('ts', DateTime, primary_key=True),
    Column('meiv2', Float)
)


def start_mappers():
    mapper(model.Enso, enso_values)
