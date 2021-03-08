#!/bin/bash

cat input_file_sample.txt | \
	grep -E -o '^# [0-9]{2}\/[0-9]{2} \([0-9]{2}.+\)' | \
	python chronator/calculator.py --mode elapsed_hours | \
	python chronator/calculator.py --mode hours_balance | \
	python chronator/calculator.py --mode total_hours
