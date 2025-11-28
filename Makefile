# Makefile
DC = docker compose
APP = web

.PHONY: up down logs migrate superuser test shell build

build:
	$(DC) build --no-cache

up:
	$(DC) up -d

down:
	$(DC) down

logs:
	$(DC) logs -f

migrate:
	$(DC) exec $(APP) python manage.py makemigrations
	$(DC) exec $(APP) python manage.py migrate

superuser:
	$(DC) exec $(APP) python manage.py createsuperuser

test:
	$(DC) exec $(APP) python manage.py test

shell:
	$(DC) exec $(APP) python manage.py shell

init: build up migrate superuser