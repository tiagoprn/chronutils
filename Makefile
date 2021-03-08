.PHONY: help
SHELL := /bin/bash

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, cache...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf

requirements-dev:  ## Install the app requirements (dev mode)
	@pip install --upgrade pip
	@pip install -r requirements.dev

requirements-prod:  ## Install the app requirements (prod mode)
	@pip install --upgrade pip
	@pip install -r requirements.all

test: clean  ## Run test suite and coverage report
	@py.test --cov -s -vvvv --cov-report term-missing

sample-run: clean ## runs the script on a sample input file
	@/bin/bash sample_run.sh
