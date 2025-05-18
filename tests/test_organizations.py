import pytest

from app.services import OrganizationsService


class TestByBuildingId:

    @pytest.mark.asyncio
    async def test_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_by_building_id(building_id=1)
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_by_building_id(building_id=999999)
        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404


class TestByActivityId:

    @pytest.mark.asyncio
    async def test_id_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_by_activity_id(activity_id=2)
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_by_activity_id(activity_id=999999)
        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404


class TestByBoundingBox:

    @pytest.mark.asyncio
    async def test_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_in_bounding_box(
            min_lat=55.750244, max_lat=55.752244, min_lng=37.617423, max_lng=37.619423
        )
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_in_bounding_box(
            min_lat=56.750244, max_lat=57.752244, min_lng=37.617423, max_lng=37.619423
        )

        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404


class TestByRadius:

    @pytest.mark.asyncio
    async def test_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_in_radius(
            center_lat=55.751244, center_lng=37.618423, radius_m=100
        )
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_in_radius(
            center_lat=55.761244, center_lng=37.618423, radius_m=100
        )

        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404


class TestByActivityIdWithChildren:

    @pytest.mark.asyncio
    async def test_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_by_activity_id_with_children(activity_id=2)
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_by_activity_id(activity_id=999999)
        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404


class TestByTitle:

    @pytest.mark.asyncio
    async def test_found(self):
        expected_title = 'ООО "Ромашка"'
        organizations = await OrganizationsService.get_by_title(find_title='ОоОg "РомАшка"')
        assert organizations.data
        assert organizations.error is None
        assert expected_title in [org.title for org in organizations.data]

    @pytest.mark.asyncio
    async def test_not_found(self):
        organizations = await OrganizationsService.get_by_title(find_title='ОоО РомАшка"')
        assert organizations.data is None
        assert organizations.error
        assert organizations.status_code == 404
