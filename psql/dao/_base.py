import asyncio
from typing import Generic, TypeVar

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import InterfaceError, OperationalError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.bootstrap import logger, DATABASE_URL
from psql.models import BaseDBModel

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

DTOType = TypeVar("DTOType")


def retry_on_disconnect(max_retries: int = 7, delay: int = 1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (InterfaceError, OperationalError) as e:
                    retries += 1
                    error_message = str(e)
                    error_text = f"Connection error: {error_message}. Retry {retries}/{max_retries}..."
                    logger.warning(msg=error_text)
                    await asyncio.sleep(delay)
            return None

        return wrapper

    return decorator


class _BaseDAO(Generic[DTOType]):
    model: type[BaseDBModel]
    dto: type[DTOType]

    @classmethod
    @retry_on_disconnect()
    async def create_one_return_id(cls, **data) -> int:
        async with async_session_maker() as session:
            try:
                stmt = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(stmt)
                created_id = result.scalar()
                await session.commit()
                return created_id
            except IntegrityError as e:
                await session.rollback()
                raise e

    @classmethod
    @retry_on_disconnect()
    async def update_by_id(cls, item_id: int, **data) -> bool:
        async with async_session_maker() as session:
            try:
                stmt = update(cls.model).where(cls.model.id == item_id).values(**data)
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount > 0
            except IntegrityError as e:
                await session.rollback()
                raise e

    @classmethod
    @retry_on_disconnect()
    async def delete_by_id(cls, item_id: int) -> bool:
        async with async_session_maker() as session:
            try:
                stmt = delete(cls.model).where(cls.model.id == item_id)
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount > 0
            except IntegrityError as e:
                await session.rollback()
                raise e

    @classmethod
    @retry_on_disconnect()
    async def get_one_or_none(cls, **filter_by) -> DTOType | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).limit(1)
            result = await session.execute(query)
            row = result.scalars().one_or_none()
            if row:
                return cls.dto.model_validate(obj=row, from_attributes=True)
            return None

    @classmethod
    @retry_on_disconnect()
    async def get_many(cls, **filter_by) -> list[DTOType]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).order_by(cls.model.id)
            data = await session.execute(query)
            return [cls.dto.model_validate(obj=row, from_attributes=True) for row in data.scalars().all()]
