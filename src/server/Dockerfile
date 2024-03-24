FROM python:3.8.19-slim-bullseye

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./.env /usr/src/app/.env

RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
