from fastapi import APIRouter, Security

from .organizations import router as organizations_router
from ..utils import check_api_key

router = APIRouter(dependencies=[Security(check_api_key)], prefix="/api")

router.include_router(router=organizations_router, prefix="/organizations")
