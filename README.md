# Hours Calculator

This script implements an hours calculator which has 3 modes that can be piped to each other to achieve the desired results.

Below are the modes description:

- elapsed_hours: Given a date's hours range record, returns the total elapsed hours on that day.  E.g.:

```
COMMAND:
	$ echo '# 14/01 (09:00 12:50 13:55 18:30)' | python calculator.py --mode elapsed_hours
OUTPUTS:
	14/01 - 08:25
```

- hours_balance: Given a date and a sum of hours, calculates the hours balance, using 8 hours as a reference.  E.g.:

```
COMMAND:
	$ echo '14/01 - 08:25' | python calculator.py --mode hours_balance
OUTPUTS:
	14/01 - 00:25
```

- total_hours: Given hours records, return the sum of all of them. E.g.:

```
COMMAND:
	$ echo -e '20/01 - 01:30\n19/01 - 00:35\n18/01 - -00:20\n15/01 - 00:45\n14/01 - 00:25\n' | python calculator.py --mode total_hours
OUTPUTS:
	2:55
```

The commands can be piped between them, so that you can get what you want from a file with time records (you can be smart here using grep to get the desired records from any file, since it has lines on the desired format ;).

A [sample input file](input_file_sample.txt) is included on this directory so that you can experiment with the possibilities. There are also make commands you can run from this folder to get the idea:

```bash
$ make example-run-elapsed-hours-mode-on-sample-file        # runs "elapsed hours" mode on the sample input file
$ make example-run-hours-balance-mode-on-sample-file        # runs "hours_balance" mode on the sample input file
$ make example-run-total-hours-balance-mode-on-sample-file  # runs "total-hours" mode on the sample input file
```

