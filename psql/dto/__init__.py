from .building import BuildingDTO
from .phone import PhoneDTO
from .organization import OrganizationDTO
from .activity import ActivityDTO

OrganizationDTO.model_rebuild()
PhoneDTO.model_rebuild()
ActivityDTO.model_rebuild()
