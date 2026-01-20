python
from dataclasses import dataclass


@dataclass(frozen=True)
class RMCData:
    lat: float
    lon: float
    sog: float
    cog: int

