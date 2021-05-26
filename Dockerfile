FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs on Google Cloud.
ENV PYTHONUNBUFFERED True

ENV PROJECT_ROOT=/app
WORKDIR $PROJECT_ROOT

RUN apt-get update -y && apt-get install -y --fix-missing build-essential gfortran git && rm -rf /var/lib/apt/lists/*

# We can include python tools directly from NREL repo
RUN pip install git+https://github.com/OpenFAST/python-toolbox.git

COPY requirements-dev.txt .
COPY setup.py .
COPY . .

RUN pip install --upgrade pip && pip install -r requirements-dev.txt

EXPOSE $PORT

ARG _SERVICE_ID
ENV SERVICE_ID=$_SERVICE_ID

ARG _GUNICORN_WORKERS=1
ENV _GUNICORN_WORKERS=$_GUNICORN_WORKERS

ARG _GUNICORN_THREADS=8
ENV _GUNICORN_THREADS=$_GUNICORN_THREADS

# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers $_GUNICORN_WORKERS --threads $_GUNICORN_THREADS --timeout 0 octue.cloud.deployment.google.cloud_run:app
