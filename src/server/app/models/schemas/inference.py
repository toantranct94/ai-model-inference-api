from pydantic import Field

from app.models.domains import Status


class InferenceProcess(Status):
    inference_id: str = Field(...)


class InferenceResult(Status):
    inference_class: str = Field('')
