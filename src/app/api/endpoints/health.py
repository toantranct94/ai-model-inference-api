from fastapi import APIRouter, status
from app.models.schemas import Health

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def health():
    """
    Check heath
    """
    return Health()
