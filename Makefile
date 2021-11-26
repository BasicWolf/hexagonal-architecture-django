MANAGEPY = src/manage.py
PYTEST = pytest
MYPY = mypy
ENV = PYTHONPATH=src/:./

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

mypy:
	$(MYPY) --namespace-packages -p myapp -p tests

test:
	$(ENV) $(PYTEST)

migrate:
	$(MANAGEPY) migrate

run:
	$(MANAGEPY) runserver
