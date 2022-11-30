#!/bin/bash

cat input_file_sample.txt | \
	grep -E -o '^# [0-9]{2}\/[0-9]{2} \([0-9]{2}.+\)' | \
	python chronutils/calculator.py --mode elapsed_hours | \
	python chronutils/calculator.py --mode hours_balance | \
	python chronutils/calculator.py --mode total_hours
