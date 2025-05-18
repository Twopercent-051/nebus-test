from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from psql.models.base import BaseDBModel


class PhoneModel(BaseDBModel):
    __tablename__ = "phones"

    value: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey(column="organizations.id", ondelete="CASCADE"))
    organization = relationship(argument="OrganizationModel", back_populates="phones")
