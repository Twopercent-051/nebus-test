from psql.dto.activity import ActivityDTO
from psql.dto.building import BuildingDTO
from psql.dto.phone import PhoneDTO
from psql.dto._base import _BaseDTO


class OrganizationDTO(_BaseDTO):
    title: str
    description: str | None
    building: BuildingDTO
    phones: list[PhoneDTO]
    activities: list[ActivityDTO]
