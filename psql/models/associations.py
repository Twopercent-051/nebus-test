from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from psql.models import ActivityModel, OrganizationModel
from psql.models import BaseDBModel


class OrganizationActivityModel(BaseDBModel):
    __tablename__ = "organization_activities"

    organization_id: Mapped[int] = mapped_column(ForeignKey(column=OrganizationModel.id, ondelete="CASCADE"))
    organization: Mapped[OrganizationModel] = relationship(
        argument=OrganizationModel,
        foreign_keys=[organization_id],
        lazy="joined",
        passive_deletes=True,
        overlaps="activities,organizations",
    )
    activity_id: Mapped[int] = mapped_column(ForeignKey(column=ActivityModel.id, ondelete="CASCADE"))
    activity: Mapped[ActivityModel] = relationship(
        argument=ActivityModel,
        foreign_keys=[activity_id],
        lazy="joined",
        passive_deletes=True,
        overlaps="activities,organizations",
    )
