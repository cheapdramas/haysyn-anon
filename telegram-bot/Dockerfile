FROM python:3.12.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DATABASE_URL="sqlite:///./db.sqlite3"

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==1.8.2"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . . 
