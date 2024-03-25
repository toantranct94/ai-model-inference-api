import io
import uuid

import pytest
from app.services import redis_client
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from PIL import Image


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv("./tests/.env.test", override=True)


@pytest.fixture
def client():
    from app.main import app

    client = TestClient(app)
    print("FastAPI client created")
    return client


@pytest.fixture
def image_file():
    img = Image.new('RGB', (60, 30), color=(73, 109, 137))
    data = io.BytesIO()
    img.save(data, 'PNG')
    data.seek(0)
    return data


@pytest.fixture
def completed_request_id():
    request_id = str(uuid.uuid4())
    redis_client.set(request_id, 'Normal')
    return request_id
