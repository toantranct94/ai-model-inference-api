import uuid
from unittest.mock import patch

from app.models.enums import Status
from fastapi import status


def test_health(client):
    # Arrange

    # Act
    response = client.get("/api/health")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": Status.OK.value}


@patch('app.services.rabbitmq_client.publish_message')
def test_inference(mock_publish_message, client, image_file):
    response = client.post(
        "/api/inference/requests",
        files={"image": ("image.png", image_file, "image/png")},
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert "request_id" in response.json()
    assert "status" in response.json()
    mock_publish_message.assert_called_once()


def test_inference_result_success(client, completed_request_id):
    # Arrange
    url = f"/api/inference/requests/{completed_request_id}/result"
    # Act
    response = client.get(url)
    data = response.json()
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data["status"] == Status.COMPLETED.value
    assert data["inference_class"] == 'Normal'


def test_inference_result_not_found(client):
    # Arrange
    request_id = str(uuid.uuid4())
    # Act
    response = client.get(f"/api/inference/requests/{request_id}/result")
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
