from dataclasses import dataclass


RMC Parser:

@dataclass
class RMCData:
lat: float
lon: float
sog: float
cog: int
