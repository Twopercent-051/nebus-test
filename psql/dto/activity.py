from pydantic import Field

from psql.dto._base import _BaseDTO


class ActivityDTO(_BaseDTO):
    title: str
    children: list["ActivityDTO"] = Field(default_factory=list)


ActivityDTO.model_rebuild()
