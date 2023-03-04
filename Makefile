# Define variables
PYTHON = python
PIP = pip
FLAKE8 = flake8
MYPY = mypy ./aws_explorer
PYTEST = pytest --cov --exitfirst --disable-warnings --verbose --no-header --continue-on-collection-errors
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

.PHONY: install
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: lint
lint:
	$(PYLINT)

.PHONY: format
format:
	$(BLACK)

.PHONY: typecheck
typecheck:
	$(MYPY)

.PHONY: test
test:
	$(PYTEST) 

.PHONY: all
all: 
	make lint 
	make test 
	make typecheck 