from datetime import datetime

from ensoserver.domain import model


def test_create_new_enso_value_entry(session):
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso_value = model.Enso(ts, meiv2)

    session.add(enso_value)
    session.commit()

    enso_query = session.query(model.Enso).all()
    assert enso_value in enso_query


def test_create_multiple_enso_value_entries(session):
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso_value1 = model.Enso(ts, meiv2)
    session.add(enso_value1)

    ts = datetime(year=2020, month=10, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso_value2 = model.Enso(ts, meiv2)
    session.add(enso_value2)

    session.commit()

    enso_query = session.query(model.Enso).all()
    assert enso_value1 in enso_query
    assert enso_value2 in enso_query
