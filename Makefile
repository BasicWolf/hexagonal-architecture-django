MANAGEPY = src/manage.py

help:
	@echo 'Usage:'
	@echo '   make migrate'
	@echo '   make run'
	@echo 'Development: '
	@echo '   make test        run unit and integration tests'
	@echo '   make flake8      run flake8 style checker'
	@echo '   make mypy        run mypy static typing checker'
	@echo '   make buidl       run linters and tests'

buidl: build

build: mypy test

static-analysis: flake8 mypy

flake8:
	flake8

mypy:
	mypy --namespace-packages --check-untyped-defs -p myapp -p tests
test:
	DJANGO_SETTINGS_MODULE="hexarch_project.test_settings" \
	PYTHONPATH=src/:./ \
	pytest

migrate:
	$(MANAGEPY) migrate

run: migrate
	$(MANAGEPY) runserver
