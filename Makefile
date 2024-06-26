SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:

INSTALL_STAMP := .install.stamp
POETRY_STAMP := .poetry.stamp
POETRY = $(shell command -v poetry 2> /dev/null)
JUNIT_OUT = $(shell find ./junit -type f -name '*.xml')
GITHUB_PAGE := index.html


all: venv lint pie test

build: $(INSTALL_STAMP)
	$(POETRY) build

poetrysetup: $(POETRY_STAMP)
$(POETRY_STAMP):
	pipx install poetry
	poetry -V
	which poetry
	touch $(POETRY_STAMP)

deps: $(INSTALL_STAMP) poetrysetup
$(INSTALL_STAMP): pyproject.toml poetry.lock
	$(POETRY) install --with dev --sync
	touch $(INSTALL_STAMP)

.PHONY: lint
lint:
	# stop the build if there are Python syntax errors or undefined names
	mkdir -p ./reports/flake8
	$(POETRY) run flake8 . --count --select=E9,F63,F7,F82 --show-source --exit-zero --format=html --htmldir ./reports/flake8 --statistics --tee --output-file reports/flake8/flake8stats.txt
	$(POETRY) run genbadge flake8
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	$(POETRY) run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: pie
pie: $(INSTALL_STAMP)
	# type check with mypy
	MYPYPATH=src $(POETRY) run mypy --namespace-packages --explicit-package-bases .

.PHONY: test
test: $(INSTALL_STAMP)
	mkdir -p reports/junit
	$(POETRY) run coverage run -m src.tests
	$(POETRY) run coverage report
	$(POETRY) run coverage xml
	mv reports/junit/TEST-tests.test_render.TestRender.xml reports/junit/junit.xml
	$(POETRY) run coverage html


	$(POETRY) run genbadge tests
	$(POETRY) run genbadge coverage -i coverage.xml

.PHONY: pages
pages: $(GITHUB_PAGE)

$(GITHUB_PAGE): README.md deps
	$(POETRY) run python -m markdown README.md > index.html

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP)
	rm -rf build
	rm -rf dist
	rm -rf test

