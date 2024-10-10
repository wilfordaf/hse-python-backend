FROM python:3.12-slim
WORKDIR /root/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev \
    g++ \
    swig \
    bash \
    netcat-traditional \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip

COPY . .
RUN pip install poetry

RUN POETRY_VIRTUALENVS_CREATE=false poetry install && rm -rf /root/.cache/pypoetry/*

EXPOSE 8000
CMD ["uvicorn", "homework_4.api.main:app", "--host", "0.0.0.0", "--port", "8000"]