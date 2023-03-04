# Define variables
PYTHON = python
PIP = pip
FLAKE8 = flake8
MYPY = mypy ./aws_explorer
PYTEST = pytest --disable-warnings --verbose --no-header
BLACK = black ./aws_explorer
PYLINT = pylint --exit-zero --output-format colorized ./aws_explorer

# Define targets
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage:"
	@echo "  make lint         Lint code with flake8"
	@echo "  make typecheck    Type check code with mypy"
	@echo "  make test         Run tests with pytest"

# ----------------------------------- BUILD ---------------------------------- #

.PHONY: build
build: 
	python setup.py sdist bdist_wheel

# ---------------------------------- INSTALL --------------------------------- #

# Standard install (CI/CD)
.PHONY: install
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Install in editable mode (local development)
.PHONY: install_editable
install_editable:
	python -m pip install --upgrade pip
	pip install -e ./

# ----------------------------------- CLEAN ---------------------------------- #

.PHONY: clean
clean: 
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./aws_explorer.egg-info

# ---------------------------------------------------------------------------- #

.PHONY: precommit
precommit:
	pre-commit run --all-files

.PHONY: format
format:
	$(BLACK)

.PHONY: lint
lint:
	$(PYLINT) || true

.PHONY: typecheck
typecheck:
	$(MYPY) || true

.PHONY: test
test:
	$(PYTEST) || true

# ---------------------------------------------------------------------------- #

all: format	lint typecheck test 