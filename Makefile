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

test-matching: clean  ## Run only tests matching pattern. E.g.: make test-matching test=TestClassName
	@py.test -k $(test) -s -vvv

example-run-elapsed-hours-mode-on-sample-file: clean  ## runs "elapsed hours" mode on the sample input file
	@cat samples/input_file_sample.txt | grep -E -o '^# [0-9]{2}\/[0-9]{2} \([0-9]{2}.+\)' | python chronutils/calculator.py --mode elapsed_hours

example-run-hours-balance-mode-on-sample-file: clean  ## runs "hours_balance" mode on the sample input file
	@cat samples/input_file_sample.txt | grep -E -o '^# [0-9]{2}\/[0-9]{2} \([0-9]{2}.+\)' | python chronutils/calculator.py --mode elapsed_hours | python chronutils/calculator.py --mode hours_balance

example-run-total-hours-balance-mode-on-sample-file: clean  ## runs "total-hours" mode on the sample input file
	@cat samples/input_file_sample.txt | grep -E -o '^# [0-9]{2}\/[0-9]{2} \([0-9]{2}.+\)' | python chronutils/calculator.py --mode elapsed_hours | python chronutils/calculator.py --mode hours_balance | python chronutils/calculator.py --mode total_hours
