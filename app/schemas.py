from pydantic import BaseModel


class AirQualityEntry(BaseModel):
    year: int
    lat: float
    lon: float
    GWRPM25: float
