from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from psql.models.base import BaseDBModel


class OrganizationModel(BaseDBModel):
    __tablename__ = "organizations"

    title: Mapped[str]
    description: Mapped[str | None]
    building_id: Mapped[int] = mapped_column(ForeignKey(column="buildings.id"))
    building = relationship(argument="BuildingModel")
    phones = relationship(argument="PhoneModel", back_populates="organization", lazy="selectin")
    activities = relationship(
        argument="ActivityModel", secondary="organization_activities", back_populates="organizations"
    )
