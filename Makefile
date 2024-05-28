VENV = $(poetry env info -p)
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
POETRY = poetry

all: venv lint pie test

parser: $(genparser)

venv: $(VENV)/bin/activate

build: venv
	$(PYTHON) -m build


$(VENV)/bin/activate: pyproject.toml
	$(POETRY) install

lint:
	# stop the build if there are Python syntax errors or undefined names
	$(POETRY) run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	$(POETRY) run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

pie:
	# type check with mypy
	MYPYPATH=src $(POETRY) run mypy --namespace-packages --explicit-package-bases .

test:
	cd src && $(POETRY) run python -m unittest

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf build
	rm -rf dist
	rm -rf test

.PHONY: all build clean test lint pie