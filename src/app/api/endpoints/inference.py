from fastapi import APIRouter, status
from app.models.schemas import Health

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def inference():
    """
    Check heath
    """
    return Health()


@router.get(
    "/result/{inferencer_id}",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def inference_result(
    inferencer_id: str,
):
    """
    Check heath
    """
    return Health()
