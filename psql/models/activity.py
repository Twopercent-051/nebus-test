from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from psql.models import BaseDBModel


class ActivityModel(BaseDBModel):
    __tablename__ = "activities"

    title: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey(column="activities.id"), nullable=True)
    parent: Mapped[Optional["ActivityModel"]] = relationship(
        argument="ActivityModel",
        remote_side="ActivityModel.id",
        back_populates="children",
    )
    children: Mapped[list["ActivityModel"]] = relationship(
        argument="ActivityModel", back_populates="parent", cascade="all, delete"
    )
    organizations = relationship(
        argument="OrganizationModel", secondary="organization_activities", back_populates="activities"
    )
