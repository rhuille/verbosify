.DEFAULT_GOAL := all

format:
	isort verbosify/ tests/
	black -S -l 80 verbosify/ tests/

lint:
	flake8 --max-line-length=80 verbosify/ tests/
	isort --check-only --df verbosify/ tests/
	black -S -l 80 --check --diff verbosify/ tests/

test:
	pytest --cov=verbosify

install:
	pip install -e .
	pip install -r tests/requirements-testing.txt

clean:
	rm -rf `cat .gitignore`

all: format lint test
