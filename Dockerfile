
FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
