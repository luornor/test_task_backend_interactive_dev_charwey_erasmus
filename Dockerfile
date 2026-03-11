FROM python:3.12-slim As base
#Stage 1 base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/tmp/poetry_cache' \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./

#stage two development

FROM base As development

RUN apt-get update && apt-get install -y build-essential
RUN poetry install --no-root
COPY . .
CMD ["python","manage.py","runserver","0.0.0.0:8000"]

#Stage three for development
FROM base As production
RUN poetry install --no-root --only main
COPY . .
RUN python manage.py collectstatic --noinput
RUN pip install gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]


