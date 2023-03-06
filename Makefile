# Define variables
PYTHON = python
PIP = pip
FLAKE8 = flake8
MYPY = mypy ./aws_explorer
PYTEST = pytest --disable-warnings --verbose --no-header 
BLACK = black ./aws_explorer
# PYLINT = pylint --persistent=yes --output-format colorized ./aws_explorer
PYLINT = pylint --jobs=4 --output-format colorized ./aws_explorer

# ----------------------------------- ALL ----------------------------------- #

# DEFAULT: Run all checks; Helpful to have closeby when developing
all: format	lint typecheck test 

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
	@$(PYLINT)

.PHONY: typecheck
typecheck:
	@mypy --follow-imports=silent --ignore-missing-imports --no-strict-optional --no-warn-no-return --no-warn-unused-ignores --show-column-numbers --pretty --no-implicit-optional --incremental ./aws_explorer

.PHONY: test
test:
	@pytest --disable-warnings --verbose --no-header