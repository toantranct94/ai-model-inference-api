import pickle
import uuid

from aio_pika import Message
from fastapi import APIRouter, HTTPException, UploadFile, status
from PIL import Image

from app.models.enums import Status
from app.models.schemas import InferenceProcess, InferenceResult
from app.services import rabbitmq_client, redis_client

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=InferenceProcess,
)
async def inference(
    image: UploadFile
):
    """
    Perform inference on the given image.

    Args:
        image (UploadFile): The image file to perform inference on.

    Returns:
        InferenceProcess: An object representing the inference process,
            including the status and inference ID.
    """
    inference_id = str(uuid.uuid4())
    x = Image.open(image.file).convert('RGB')

    message = Message(pickle.dumps(x))

    message.headers = {
        "inference_id": inference_id,
    }

    await rabbitmq_client.publish_message(message)

    return InferenceProcess(
        status=Status.PROCESSING.value,
        inference_id=inference_id
    )


@router.get(
    "/result/{inference_id}",
    status_code=status.HTTP_200_OK,
    response_model=InferenceResult,
)
async def inference_result(
    inference_id: str,
):
    """
    Get the result of an inference by its ID.

    Parameters:
    - inference_id (str): The ID of the inference.

    Returns:
    - InferenceResult: The result of the inference.

    Raises:
    - HTTPException: If the inference ID is not found.
    """
    if not redis_client.exists(inference_id):
        return InferenceResult(status=Status.PROCESSING.value)

    result = redis_client.get(inference_id)

    if result is None:
        raise HTTPException(status_code=404)

    return InferenceResult(
        status=Status.COMPLETED.value, inference_class=result)
