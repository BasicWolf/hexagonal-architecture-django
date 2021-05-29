MANAGEPY = src/manage.py
PYTEST = pytest
MYPY = mypy
ENV = PYTHONPATH=src/:./

test:
	$(ENV) $(PYTEST)

migrate:
	$(MANAGEPY) migrate

run:
	$(MANAGEPY) runserver

mypy:
	MYPYPATH=src/ $(MYPY) --namespace-packages -p myapp
