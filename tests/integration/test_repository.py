from datetime import datetime

from ensoserver.domain import model
from ensoserver.adapters import repository


def test_repository_can_save_enso_value(session):
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso_value = model.Enso(ts, meiv2)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(enso_value)
    session.commit()

    rows = list(session.execute(
        'SELECT ts, meiv2 FROM "enso_values"'
    ))
    assert rows == [(ts.strftime("%Y-%m-%d %H:%M:%S.%f"), meiv2)]


def test_repository_can_update_enso_value(session):
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso_value = model.Enso(ts, meiv2)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(enso_value)

    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.5
    enso_value = model.Enso(ts, meiv2)

    repo.add(enso_value)

    session.commit()

    rows = list(session.execute(
        'SELECT ts, meiv2 FROM "enso_values"'
    ))
    assert rows == [(ts.strftime("%Y-%m-%d %H:%M:%S.%f"), meiv2)]


def insert_enso_value(session, ts, meiv2):
    session.execute(
        'INSERT INTO enso_values (ts, meiv2)'
        f' VALUES ("{ts.strftime("%Y-%m-%d %H:%M:%S.%f")}", {meiv2})'
    )


def test_repository_can_retrieve_enso_value(session):
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47

    insert_enso_value(session, ts=ts, meiv2=meiv2)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get(ts)

    assert retrieved.ts == ts
    assert retrieved.meiv2 == meiv2
