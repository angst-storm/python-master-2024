init:
	python -m venv venv
	pip install -r requirements.txt

create:
	python -m django --version
	django-admin startproject master