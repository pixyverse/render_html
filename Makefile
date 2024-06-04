INSTALL_STAMP := .install.stamp
POETRY = $(shell which poetry)

.ONESHELL:

all: venv lint pie test

build: $(INSTALL_STAMP)
	$(POETRY) build

.PHONY: poetrysetup
poetrysetup:
	pipx install poetry

deps: $(INSTALL_STAMP) poetrysetup
$(INSTALL_STAMP): pyproject.toml poetry.lock
	$(POETRY) install
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
	$(POETRY) run coverage run -m src.tests
	$(POETRY) run coverage report
	$(POETRY) run coverage xml
	$(POETRY) run coverage html
	$(POETRY) run genbadge tests -i $(shell find junit -name '*.xml')
	$(POETRY) run genbadge coverage -i coverage.xml

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP)
	rm -rf build
	rm -rf dist
	rm -rf test

