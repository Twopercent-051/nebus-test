from sqlalchemy import func, select
from sqlalchemy.orm import aliased, selectinload

from psql.dao._base import _BaseDAO, async_session_maker, retry_on_disconnect
from psql.dto import OrganizationDTO
from psql.models import ActivityModel, BuildingModel, OrganizationModel


class OrganizationsDAO(_BaseDAO[OrganizationDTO]):
    model = OrganizationModel
    dto = OrganizationDTO

    __select_options = [
        selectinload(model.building),
        selectinload(model.phones),
        selectinload(model.activities)
        .selectinload(ActivityModel.children)
        .selectinload(ActivityModel.children)
        .selectinload(ActivityModel.children),
    ]

    @classmethod
    @retry_on_disconnect()
    async def get_one_or_none(cls, **filter_by) -> OrganizationDTO | None:
        async with async_session_maker() as session:
            query = select(cls.model).options(*cls.__select_options).filter_by(**filter_by).limit(1)
            result = await session.execute(query)
            row = result.scalars().one_or_none()
            if row:
                return cls.dto.model_validate(obj=row, from_attributes=True)
            return None

    @classmethod
    @retry_on_disconnect()
    async def get_many(cls, **filter_by) -> list[OrganizationDTO]:
        async with async_session_maker() as session:
            query = select(cls.model).options(*cls.__select_options).filter_by(**filter_by).order_by(cls.model.id)
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]

    @classmethod
    async def get_by_activity_id(cls, activity_id: int) -> list[OrganizationDTO]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .join(cls.model.activities)
                .options(*cls.__select_options)
                .filter(ActivityModel.id == activity_id)
            )
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]

    @classmethod
    async def get_in_bounding_box(
        cls,
        min_lat: float,
        max_lat: float,
        min_lng: float,
        max_lng: float,
    ) -> list[OrganizationDTO]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .join(cls.model.building)
                .where(
                    BuildingModel.latitude >= min_lat,
                    BuildingModel.latitude <= max_lat,
                    BuildingModel.longitude >= min_lng,
                    BuildingModel.longitude <= max_lng,
                )
                .options(*cls.__select_options)
            )
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]

    @classmethod
    async def get_in_radius(cls, center_lat: float, center_lng: float, radius_m: float) -> list[OrganizationDTO]:
        earth_radius_m = 6371000
        async with async_session_maker() as session:
            distance_expr = earth_radius_m * func.acos(
                func.cos(func.radians(center_lat))
                * func.cos(func.radians(BuildingModel.latitude))
                * func.cos(func.radians(BuildingModel.longitude) - func.radians(center_lng))
                + func.sin(func.radians(center_lat)) * func.sin(func.radians(BuildingModel.latitude))
            )
            query = (
                select(cls.model)
                .join(cls.model.building)
                .where(distance_expr <= radius_m)
                .options(*cls.__select_options)
            )
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]

    @classmethod
    async def get_by_activity_with_children(cls, activity_id: int) -> list[OrganizationDTO]:
        async with async_session_maker() as session:
            ids_cte = select(ActivityModel.id).where(ActivityModel.id == activity_id).cte(recursive=True)
            ids_alias = aliased(ActivityModel)
            ids_cte = ids_cte.union_all(select(ids_alias.id).where(ids_alias.parent_id == ids_cte.c.id))
            ids_query = select(ids_cte.c.id)
            result = await session.execute(ids_query)
            activity_ids = [row.id for row in result.all()]
            query = (
                select(cls.model)
                .join(cls.model.activities)
                .options(*cls.__select_options)
                .filter(ActivityModel.id.in_(activity_ids))
                .distinct()
            )
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]

    @classmethod
    @retry_on_disconnect()
    async def find_by_title(cls, find_title: str) -> list[OrganizationDTO]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(*cls.__select_options)
                .filter(cls.model.title.ilike(f"%{find_title}%"))
                .order_by(cls.model.id)
            )
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]
