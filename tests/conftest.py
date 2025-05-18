import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.bootstrap import DATABASE_URL


@pytest_asyncio.fixture(autouse=True)
async def patch_session_maker(monkeypatch):
    print(">>> patch_session_maker FIXTURE USED <<<")
    import psql.dao.organization

    engine = create_async_engine(url=DATABASE_URL, future=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(psql.dao.organization, "async_session_maker", session_maker)
    yield
    await engine.dispose()
