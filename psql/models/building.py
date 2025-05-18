from sqlalchemy.orm import Mapped

from psql.models import BaseDBModel


class BuildingModel(BaseDBModel):
    __tablename__ = "buildings"

    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
