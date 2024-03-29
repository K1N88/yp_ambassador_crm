FROM python:3.10-alpine
WORKDIR /crm_app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
COPY backend/ .
COPY app_frontend/ ./app_frontend/
CMD ["poetry", "run", "gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
