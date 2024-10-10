init:
	python -m venv venv

install:
	pip install -r requirements.txt

create:
	python -m django --version
	django-admin startproject parseq
	python parseq/manage.py startapp cron

runsever:
	python parseq/manage.py runserver

runsever:
	python parseq/manage.py rundramatiq

migrate:
	python parseq/manage.py migrate

deploy:
	docker compose -f deploy/docker-compose.yaml up -d