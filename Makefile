install:
	poetry install

version:
	poetry run django-admin version

start:
	gunicorn task_manager.wsgi:application

dev:
	python manage.py runserver

commands:
	python manage.py


migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

shell:
	python manage.py shell

dbshell:
	python manage.py dbshell

admin:
	python manage.py createsuperuser

static_files:
	python manage.py collectstatic

loc:
	python manage.py makemessages -l ru

loc_comp:
	python manage.py compilemessages

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py