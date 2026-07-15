PYTHON ?= python3
TRACK ?=

.PHONY: preflight check-navigation check-remote-navigation test

preflight:
	@$(PYTHON) scripts/curriculum.py preflight --registry tracks/curriculum.json --track "$(TRACK)"

check-navigation:
	@$(PYTHON) scripts/curriculum.py check --registry tracks/curriculum.json --root .

check-remote-navigation: check-navigation
	@$(PYTHON) scripts/curriculum.py check-remote --registry tracks/curriculum.json --root .

test:
	@$(PYTHON) -m unittest discover -s scripts/tests -p 'test_*.py'
