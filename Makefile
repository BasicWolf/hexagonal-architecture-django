MANAGEPY = src/manage.py
PYTEST = pytest
MYPY = mypy
ENV = PYTHONPATH=src/:./

help:
	@echo 'Usage:'
	@echo '   make migrate'
	@echo '   make run'
	@echo 'Development: '
	@echo '   make test'
	@echo '   make flake8'
	@echo '   make mypy'

build: mypy test

mypy:
	$(MYPY) --namespace-packages -p myapp -p tests

test:
	$(ENV) $(PYTEST)

migrate:
	$(MANAGEPY) migrate

run:
	$(MANAGEPY) runserver
