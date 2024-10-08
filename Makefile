init:
	python -m venv venv

install:
	pip install -r requirements.txt

create:
	python -m django --version
	django-admin startproject parseq
	python parseq/manage.py startapp cron

runserver:
	(cd parseq && python manage.py runserver)

rundramatiq:
	(cd parseq && python manage.py rundramatiq)

createsuperuser:
	python parseq/manage.py createsuperuser --no-input

migrate:
	python parseq/manage.py migrate

.PHONY: deploy
deploy:
	docker compose -f deploy/docker-compose.yaml up -d

destroy:
	docker compose -f deploy/docker-compose.yaml kill