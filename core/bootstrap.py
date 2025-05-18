import logging

import betterlogging
from sqlalchemy import URL


from core.config import config


logger = logging.getLogger(__name__)
betterlogging.basic_colorized_config(level=logging.INFO)


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=config.postgres.user,
    password=config.postgres.password,
    host=config.postgres.host,
    port=config.postgres.port,
    database=config.postgres.db,
).render_as_string(hide_password=False)
