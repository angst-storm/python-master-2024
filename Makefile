init:
	python -m venv venv

install:
	pip install -r requirements.txt

create:
	python -m django --version
	django-admin startproject parseq
	python parseq/manage.py startapp cron

runserver:
	python parseq/manage.py runserver

rundramatiq:
	python parseq/manage.py rundramatiq

migrate:
	python parseq/manage.py migrate

.PHONY: deploy
deploy:
	docker compose -f deploy/docker-compose.yaml up -d

destroy:
	docker compose -f deploy/docker-compose.yaml kill