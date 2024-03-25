FROM --platform=linux/amd64 python:3.8.19-slim-bullseye

WORKDIR /code

COPY . /code/

# Install Redis and RabbitMQ dependencies
RUN apt-get update && apt-get install -y rabbitmq-server netcat

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY wait-rabbitmq.sh /code/wait-rabbitmq.sh
RUN chmod +x /code/wait-rabbitmq.sh

CMD ["./wait-rabbitmq.sh"]
