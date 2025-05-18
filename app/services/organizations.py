from app.services._base import ServiceResponse
from psql.dao.organization import OrganizationsDAO
from psql.dto import OrganizationDTO


class OrganizationsService:

    @staticmethod
    async def get_by_building_id(building_id: int) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.get_many(building_id=building_id)
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)

    @staticmethod
    async def get_by_activity_id(activity_id: int) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.get_by_activity_id(activity_id=activity_id)
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)

    @staticmethod
    async def get_in_bounding_box(
        min_lat: float,
        max_lat: float,
        min_lng: float,
        max_lng: float,
    ) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.get_in_bounding_box(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lng=min_lng,
            max_lng=max_lng,
        )
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)

    @staticmethod
    async def get_in_radius(
        center_lat: float, center_lng: float, radius_m: float
    ) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.get_in_radius(
            center_lat=center_lat, center_lng=center_lng, radius_m=radius_m
        )
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)

    @staticmethod
    async def get_one_by_id(organization_id: int) -> ServiceResponse[OrganizationDTO]:
        organization = await OrganizationsDAO.get_one_or_none(id=organization_id)
        if organization:
            return ServiceResponse(data=organization)
        return ServiceResponse(error="No organization found", status_code=404)

    @staticmethod
    async def get_by_activity_id_with_children(activity_id: int) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.get_by_activity_with_children(activity_id=activity_id)
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)

    @staticmethod
    async def get_by_title(find_title: str) -> ServiceResponse[list[OrganizationDTO]]:
        organizations = await OrganizationsDAO.find_by_title(find_title=find_title)
        if organizations:
            return ServiceResponse(data=organizations)
        return ServiceResponse(error="No organizations found", status_code=404)
