INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

all: venv lint pie test

build: $(INSTALL_STAMP)
	$(POETRY) run python -m build


install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: lint
lint:
	# stop the build if there are Python syntax errors or undefined names
	$(POETRY) run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	$(POETRY) run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: pie
pie: $(INSTALL_STAMP)
	# type check with mypy
	MYPYPATH=src $(POETRY) run mypy --namespace-packages --explicit-package-bases .

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run python -m src.tests

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP)
	rm -rf build
	rm -rf dist
	rm -rf test

