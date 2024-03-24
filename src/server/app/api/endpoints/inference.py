import pickle
import uuid

from aio_pika import Message
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from PIL import Image

from app.models.enums import Status
from app.models.schemas import InferenceProcess, InferenceResult
from app.services import rabbitmq_client, redis_client
from app.validators import upload_image_validator

router = APIRouter()


@router.post(
    "/requests",
    status_code=status.HTTP_200_OK,
    response_model=InferenceProcess,
)
async def inference(
    image: UploadFile,
    _=Depends(upload_image_validator),
):
    """
    Perform inference on the given image.

    Args:
        image (UploadFile): The image file to perform inference on.

    Returns:
        InferenceProcess: An object representing the inference process,
            including the status and inference ID.
    """
    request_id = str(uuid.uuid4())
    x = Image.open(image.file).convert('RGB')

    message = Message(pickle.dumps(x))

    message.headers = {
        "request_id": request_id,
    }

    await rabbitmq_client.publish_message(message)

    return InferenceProcess(
        status=Status.PROCESSING.value,
        request_id=request_id
    )


@router.get(
    "/requests/{request_id}/result",
    status_code=status.HTTP_200_OK,
    response_model=InferenceResult,
)
async def inference_result(
    request_id: str,
):
    """
    Get the result of an inference by its ID.

    Parameters:
    - request_id (str): The ID of the inference.

    Returns:
    - InferenceResult: The result of the inference.

    Raises:
    - HTTPException: If the inference ID is not found.
    """
    result = redis_client.get(request_id)

    if result is None:
        if not redis_client.exists(request_id):
            raise HTTPException(status_code=404)
        else:
            return InferenceResult(status=Status.PROCESSING.value)

    return InferenceResult(
        status=Status.COMPLETED.value, inference_class=result)
