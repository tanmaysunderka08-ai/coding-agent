FROM python:3.10-slim

RUN pip install --no-cache-dir pytest==9.2.0

# no .pyc or .pytest_cache in the mounted folder (they change the test hash)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTEST_ADDOPTS="-p no:cacheprovider"

RUN useradd --create-home runner
USER runner

WORKDIR /app

# docker build -t sandbox sandbox/
