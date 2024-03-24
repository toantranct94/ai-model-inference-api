# AI Model Inference

This document provides an overview of the AI Model Inference, which is designed to perform inference on images using a PyTorch model and FastAPI. The API is structured around two main endpoints, which interact with various components such as a RabbitMQ worker and a Redis database.

## Architecture

The image below shows the architecture of the API.

![Architecture](/docs/architecture.png)

## Endpoints

### POST: /api/inference/requests

This endpoint is used to upload an image for inference. Upon receiving an image, the API sends the image data to a worker via RabbitMQ and returns a `request_id` to the user. This `request_id` is unique to each inference request and is used to retrieve the result later.

### GET: /api/inference/requests/:request_id/results

Once the inference is complete, the user can retrieve the result using this endpoint. The user needs to provide the `request_id` that was returned by the POST endpoint. The API fetches the result from a Redis database using the `request_id` as the key.


## Workflow

1. The user uploads an image using the `POST` endpoint.
2. The API sends the image data to a RabbitMQ worker and returns a `request_id` to the user.
3. The worker receives the image data, performs inference using a PyTorch model, and stores the result in a Redis database with the `request_id` as the key.
4. The user retrieves the result using the `GET` endpoint and the `request_id`.


## Installation and Usage

This application is containerized using Docker and orchestrated with Docker Compose, which makes it easy to install and run.

### Dependencies

1. Ensure you have Docker installed on your machine.

2. Clone the repository to your local machine.

3. Navigate to the project directory.

### Usage

1. Run the Docker Compose command to start the application:

```bash
docker-compose up
```

2. The application will be accessible at `http://localhost:8000`.

3. Swagger documentation is available at `http://localhost:8000/api/docs`.


### Testing

To run the tests for the API and the worker, run the following command:

```bash
docker-compose exec server pytest
docker-compose exec workers pytest
```

### Cleanup

To stop the application and remove the containers, run the following command:

```bash
docker-compose down
```

## Folder Structure

The folder structure of the project is as follows:

```
.
├── README.md
├── docker-compose.yaml
├── docs
│   └── architecture.png
└── src
    ├── server
    │   ├── Dockerfile
    │   ├── app
    │   │   ├── api
    │   │   │   ├── __init__.py
    │   │   │   ├── endpoints
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── health.py
    │   │   │   │   └── inference.py
    │   │   │   └── routes.py
    │   │   ├── configs
    │   │   │   ├── __init__.py
    │   │   │   ├── config.py
    │   │   │   ├── rabbitmq.py
    │   │   │   └── redis.py
    │   │   ├── cores
    │   │   │   ├── __init__.py
    │   │   │   ├── singleton.py
    │   │   │   └── strings.py
    │   │   ├── main.py
    │   │   ├── models
    │   │   │   ├── __init__.py
    │   │   │   ├── attributes
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── health.py
    │   │   │   ├── domains
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── inference.py
    │   │   │   │   └── status.py
    │   │   │   ├── enums
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── status.py
    │   │   │   └── schemas
    │   │   │       ├── __init__.py
    │   │   │       ├── health.py
    │   │   │       └── inference.py
    │   │   ├── services
    │   │   │   ├── __init__.py
    │   │   │   ├── rabbitmq.py
    │   │   │   └── redis.py
    │   │   ├── validators
    │   │   │   ├── __init__.py
    │   │   │   └── upload.py
    │   │   └── workers
    │   │       └── __init__.py
    │   ├── requirements.txt
    │   └── tests
    │       ├── __init__.py
    │       ├── conftest.py
    │       └── test_main.py
    └── workers
        ├── Dockerfile
        ├── app
        │   ├── ai
        │   │   ├── __init__.py
        │   │   ├── checkpoints
        │   │   │   └── EfficientNet_B0_NS_320.pth
        │   │   ├── configs
        │   │   │   └── fully_connected.yaml
        │   │   ├── functions.py
        │   │   ├── model.py
        │   │   └── utils.py
        │   ├── cores
        │   │   ├── __init__.py
        │   │   └── singleton.py
        │   ├── main.py
        │   └── services
        │       ├── __init__.py
        │       ├── rabbitmq.py
        │       └── redis.py
        ├── requirements.txt
        ├── tests
        └── wait-rabbitmq.sh
```

### Explanation

- The `src` directory contains the source code for the API and the worker.
    - The `server` directory contains the source code for the FastAPI application.
    - The `workers` directory contains the source code for the worker that performs inference.
        - The `ai` directory contains the PyTorch model and related files.
- The `docs` directory contains the architecture diagram of the application.
