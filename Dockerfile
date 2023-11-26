
    FROM python:3.8-slim-buster

    RUN pip install poetry==1.6.1

    WORKDIR /app

    COPY . .

    RUN poetry install

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1


    CMD [ "poetry",  "run",  "python", "-m", "backend.manage", "runserver",  "0.0.0.0:8000"] 
