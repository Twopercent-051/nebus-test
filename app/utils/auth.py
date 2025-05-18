from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from core.config import config


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def check_api_key(api_key: str = Security(api_key_header)):
    if api_key != config.app.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
