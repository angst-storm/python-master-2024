venv:
	python -m venv venv

install:
	pip install -r requirements.txt

create:
	python -m django --version
	django-admin startproject parseq
	python parseq/manage.py startapp cron

runserver:
	(cd parseq && python manage.py runserver --noreload)

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
	docker compose -f deploy/docker-compose.yaml rm --force

clear:
	rm -R deploy/.postgresql
	rm -R deploy/.rabbitmq
	rm -R parseq/media

debug-httpcat:
	python parsers/debug.py parsers/httpcat.py

debug-evewars:
	python parsers/debug.py parsers/evewars.py

parsers-test:
	(cd parsers && python -m unittest)

django-test:
	(cd parseq && python manage.py test)

test: parsers-test django-test

init: install migrate createsuperuser