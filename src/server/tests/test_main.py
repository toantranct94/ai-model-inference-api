import io
import uuid

import pytest
from PIL import Image
from starlette.testclient import TestClient

from app.main import app
from app.models.enums import Status
from app.services import rabbitmq_client

client = TestClient(app)


@pytest.fixture(scope='module')
async def rabbitmq_connection():
    await rabbitmq_client.connect()


@pytest.fixture
def inference_response():
    # Create an image in memory
    img = Image.new('RGB', (60, 30), color=(73, 109, 137))
    data = io.BytesIO()
    img.save(data, 'PNG')
    data.seek(0)

    # Create a multipart request with the image
    response = client.post(
        "/api/inference/requests",
        files={"image": ("image.png", data, "image/png")},
    )
    return response


def test_health(test_app):
    # Arrange

    # Act
    response = client.get("/api/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": Status.OK.value}


def test_inference_success(inference_response):
    # Arrange
    # Act
    data = inference_response.json()
    # Assert
    assert inference_response.status_code == 200
    assert "request_id" in data
    assert data["status"] == Status.PROCESSING.value


def test_inference_result_success(inference_response):
    # Arrange
    request_id = inference_response.json()["request_id"]
    # Act
    response = client.get(f"/api/inference/requests/{request_id}/result")
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data["status"] == Status.COMPLETED.value


def test_inference_result_not_found(inference_response):
    # Arrange
    request_id = str(uuid.uuid4())
    # Act
    response = client.get(f"/api/inference/requests/{request_id}/result")
    # Assert
    assert response.status_code == 404
