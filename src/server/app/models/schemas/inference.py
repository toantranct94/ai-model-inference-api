from pydantic import Field

from app.models.domains import Status


class InferenceProcess(Status):
    request_id: str = Field(...)


class InferenceResult(Status):
    inference_class: str = Field('')
