from ensoserver.domain.model import Enso
from datetime import datetime


def test_user_can_create_enso():
    ts = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    meiv2 = 0.47
    enso = Enso(ts, meiv2)
    assert enso.ts == ts
    assert enso.meiv2 == meiv2
