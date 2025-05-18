from fastapi import APIRouter, HTTPException

from app.services import OrganizationsService
from psql.dto import OrganizationDTO

router = APIRouter()


@router.get(path="/by_building_id", response_model=list[OrganizationDTO])
async def get_by_building_id(building_id: int):
    result = await OrganizationsService.get_by_building_id(building_id=building_id)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/by_activity_id", response_model=list[OrganizationDTO])
async def get_by_action_id(activity_id: int):
    result = await OrganizationsService.get_by_activity_id(activity_id=activity_id)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/by_bounding_box", response_model=list[OrganizationDTO])
async def get_by_bounding_box(
    min_lat: float,
    max_lat: float,
    min_lng: float,
    max_lng: float,
):
    result = await OrganizationsService.get_in_bounding_box(
        min_lat=min_lat,
        max_lat=max_lat,
        min_lng=min_lng,
        max_lng=max_lng,
    )
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/by_radius", response_model=list[OrganizationDTO])
async def get_by_radius(center_lat: float, center_lng: float, radius_m: float):
    result = await OrganizationsService.get_in_radius(center_lat=center_lat, center_lng=center_lng, radius_m=radius_m)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/one", response_model=OrganizationDTO)
async def get_one_by_id(organization_id: int):
    result = await OrganizationsService.get_one_by_id(organization_id=organization_id)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/by_activity_id_with_children", response_model=list[OrganizationDTO])
async def get_by_activity_id_with_children(activity_id: int):
    result = await OrganizationsService.get_by_activity_id_with_children(activity_id=activity_id)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get(path="/find_by_title", response_model=list[OrganizationDTO])
async def find_by_title(find_title: str):
    result = await OrganizationsService.get_by_title(find_title=find_title)
    if result.error:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data
