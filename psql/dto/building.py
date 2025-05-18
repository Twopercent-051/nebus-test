from psql.dto._base import _BaseDTO


class BuildingDTO(_BaseDTO):

    address: str
    latitude: float
    longitude: float
