FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

# Сначала копируем весь проект, чтобы файлы гарантированно были в контейнере
COPY . .

# Затем копируем Poetry-зависимости отдельно, чтобы использовать кэш
COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
