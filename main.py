import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.bootstrap import logger
from core.config import config
from app.routers import router
from starlette.middleware.cors import CORSMiddleware


async def on_startup():
    logger.info("App started")


async def on_shutdown():
    logger.info("App stopped")


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await on_startup()
        yield
    finally:
        await on_shutdown()


app = FastAPI(lifespan=lifespan, title="Nebus test App", debug=config.app.debug)
app.include_router(router=router)

origins = ["*"]
methods = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
headers = ["*"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


async def main():
    app_config = uvicorn.Config(app=app, host="0.0.0.0", port=config.app.inner_port, log_level="info")
    server = uvicorn.Server(config=app_config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("App stopped")
