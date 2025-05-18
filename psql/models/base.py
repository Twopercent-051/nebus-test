from datetime import datetime

from typing import Annotated

from sqlalchemy import MetaData, text
from sqlalchemy.orm import mapped_column, as_declarative, Mapped

_intpk = Annotated[int, mapped_column(primary_key=True)]
_created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


@as_declarative()
class BaseDBModel:
    metadata = MetaData()

    id: Mapped[_intpk]
    created_at: Mapped[_created_at]
