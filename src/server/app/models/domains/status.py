from pydantic import BaseModel, Field

from app.models.attributes.health import Health as HealthAttrs

from ..enums.status import Status as StatusEnum


class Status(BaseModel):
    status: str = Field(StatusEnum.OK.value, alias=HealthAttrs.status)
