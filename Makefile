
DC = docker compose
APP = $(DC) run --rm web

.PHONY: build up down logs shell migrate makemigrations test install restart format clean

# --- Docker Control ---
build:
	$(DC) build

up:
	$(DC) up

down:
	$(DC) down

logs:
	$(DC) logs -f

restart:
	$(DC) restart web

# --- Django Commands ---
migrate:
	$(APP) python manage.py migrate

makemigrations:
	$(APP) python manage.py makemigrations

superuser:
	$(APP) python manage.py createsuperuser

shell:
	$(APP) python manage.py shell

# --- Code Quality ---
format:
	$(APP) black .

# --- Package Management ---
# Usage: make install package=stripe
install:
	$(APP) poetry add $(package)
	$(DC) build

# --- Testing ---
test:
	$(APP) pytest

# --- Maintenance ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
