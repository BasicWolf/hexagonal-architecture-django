MANAGEPY = src/manage.py
PYTEST = pytest
PYTEST_ENV = PYTHONPATH=src/:./

test:
	$(PYTEST_ENV) $(PYTEST)

migrate:
	$(MANAGEPY) migrate

run:
	$(MANAGEPY) runserver
