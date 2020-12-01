from dataclasses import dataclass
from datetime import datetime


@dataclass
class Enso:
    ts: datetime
    meiv2: float
