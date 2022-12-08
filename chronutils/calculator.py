import logging
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import click
import frontmatter
from dateutil.parser import parse

CURRENT_SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
LOG_LEVEL = logging.INFO
LOG_FORMAT = (
    "[%(asctime)s PID %(process)s "
    "%(filename)s:%(lineno)s - %(funcName)s()] "
    "%(levelname)s -> \t"
    "%(message)s\n"
)
logging.basicConfig(
    format=LOG_FORMAT,
    level=LOG_LEVEL,
    handlers=[logging.FileHandler(f"/tmp/{CURRENT_SCRIPT_NAME}.log")],
)


def parse_timestamps(input: str) -> List[datetime]:
    timestamps = []

    try:
        reference_date, time_records = input.split("(")
    except ValueError:
        raise Exception(
            f"\n\nExpected 2 or 4 records (1 or 2 interval pairs).\n"
            f"E.g.: \n"
            f"# 14/01 (09:00 12:50 13:55 18:30)\n"
            f"# 14/01 (09:00 18:30)\n"
        )

    time_records = time_records.replace(")", "")

    pairs = int(len(time_records.split()) / 2)

    if pairs not in [1, 2]:
        message = (
            f"Invalid time record. It must contain "
            f"1 or 2 pairs, with start and "
            f"finish times on each one. "
            f'input="{input}", pairs={pairs}'
        )
        raise Exception(message)

    index_on_pair = 1
    previous_datetime_object = None
    for record in time_records.split():
        timestamp = f"{reference_date}{record}"
        datetime_object = parse(timestr=timestamp, dayfirst=True)

        if previous_datetime_object and (
            datetime_object < previous_datetime_object
        ):
            datetime_object = datetime_object + timedelta(days=1)

        timestamps.append(datetime_object)

        previous_datetime_object = datetime_object
        index_on_pair += 1
        if index_on_pair == 3:
            index_on_pair = 1

    return timestamps


def convert_seconds_to_hours_minutes(seconds: int) -> str:
    return time.strftime("%H:%M", time.gmtime(seconds))


def calculate_elapsed_hours(input: str) -> str:
    """
    Given time intervals on a day,
    calculates the total number of hours elapsed
    summing the 2 pairs elapsed times.
    """
    timestamps = parse_timestamps(input)
    delta_str = ""
    total_records = len(timestamps)

    if total_records not in [2, 4]:
        raise Exception(
            f"Parsed timestamps amount not supported: {total_records}. "
            f"You must have 2 or 4 timestamps total (1 or 2 pairs "
            f"of time intervals)."
        )

    delta = timestamps[1] - timestamps[0]
    if total_records == 4:
        delta += timestamps[3] - timestamps[2]

    delta_str = convert_seconds_to_hours_minutes(delta.seconds)

    return delta_str


def calculate_total_hours(records: []) -> str:
    elapsed_seconds = 0

    logging.debug(f"records=\n{str(records)}")

    for record in records:
        logging.debug(f"record={record}")

        if not record:
            continue

        elapsed_time = record[8:]

        logging.debug(f"elapsed_time={elapsed_time}")

        is_negative_time = elapsed_time.startswith("-")

        hours, minutes = elapsed_time.split(":")

        seconds = timedelta(
            hours=int(hours), minutes=int(minutes)
        ).total_seconds()

        if int(hours) == 0 and is_negative_time:
            seconds *= -1

        elapsed_seconds += seconds

    total_minutes = int(elapsed_seconds / 60)
    is_total_minutes_negative = True if total_minutes < 0 else False
    if is_total_minutes_negative:
        total_minutes *= -1

    total_in_hours = "{:d}:{:02d}".format(*divmod(total_minutes, 60))
    return (
        total_in_hours
        if not is_total_minutes_negative
        else f"-{total_in_hours}"
    )


def calculate_hours_balance(record: str, expected_hours: str = "08:00") -> str:
    """
    Given a record with a number of hours,
    check if it reaches or exceeds the expected hours.

    E.g. records:
    14/01 - 08:25
    15/01 - 07:15
    """
    record_as_parsed_time_object = datetime.strptime(record, "%d/%m - %H:%M")

    hours, minutes = expected_hours.split(":")
    expected_time_object = datetime(
        day=int(record_as_parsed_time_object.day),
        month=int(record_as_parsed_time_object.month),
        year=int(record_as_parsed_time_object.year),
        hour=int(hours),
        minute=int(minutes),
    )

    delta_minutes = (
        record_as_parsed_time_object - expected_time_object
    ).total_seconds() / 60

    delta_minutes = int(delta_minutes)

    negative_balance = False
    if delta_minutes < 0:
        negative_balance = True
        delta_minutes *= -1

    delta_hours = "{:02d}:{:02d}".format(*divmod(delta_minutes, 60))
    if negative_balance:
        delta_hours = f"-{delta_hours}"

    return delta_hours


def output_calculated_elapsed_hours_for_record(record: str):
    record = record[2:]
    original_date = record[:5]
    output = calculate_elapsed_hours(record)
    sys.stdout.write(f"{original_date} - {output}\n")


def output_calculated_hours_balance_for_record(record: str):
    original_date = record[:5]
    output = calculate_hours_balance(record)
    sys.stdout.write(f"{original_date} - {output}\n")


def output_calculated_total_hours_for_record(records=[]):
    output = calculate_total_hours(records)
    sys.stdout.write(f"{output}\n")


def get_record_from_journal_file(journal_file_path: str) -> str:
    with open(journal_file_path, "r") as input_file:
        journal_file = frontmatter.load(input_file)
    keys = journal_file.keys()

    expected_keys = {"date", "hours"}
    if not (set(keys) == expected_keys):
        raise Exception(
            f"Expected keys: '{expected_keys}', "
            f"but found these instead: '{set(keys)}'"
        )

    total_timestamps = len(journal_file["hours"])
    timestamps_are_paired = total_timestamps % 2 == 0

    timestamps = " ".join(journal_file["hours"])
    if not timestamps_are_paired:
        raise Exception(
            f"Timestamps are odd - there is a total of {total_timestamps} "
            f"timestamps. There should be {total_timestamps-1} or "
            f"{total_timestamps+1} (timestamps: {timestamps})"
        )

    record_date = journal_file["date"].strftime("%d/%m")
    return f"{record_date} ({timestamps})"


def get_records_from_journal_files_in_folder(folder_path: str) -> list[str]:
    files = Path(folder_path).glob("*")
    records = []
    for file_name in files:
        try:
            record = get_record_from_journal_file(file_name)
        except TypeError as ex:
            message = (
                f'Exception getting records from file "{file_name}": '
                f"{ex}. Fix that and re-run this script."
            )
            print(message)
            sys.exit(1)
        records.append(record)
    return records


MODES = ["elapsed_hours", "hours_balance", "total_hours"]


@click.command()
@click.option(
    "--mode",
    type=click.Choice(MODES),
    help=("Available modes: {})".format(", ".join(MODES))),
)
def run(mode):
    data = sys.stdin.read()
    records = data.split("\n")

    if mode == "total_hours":
        output_calculated_total_hours_for_record(records)
    else:
        for record in records:
            if not record:
                continue

            if mode == "elapsed_hours":
                output_calculated_elapsed_hours_for_record(record)
            elif mode == "hours_balance":
                output_calculated_hours_balance_for_record(record)


if __name__ == "__main__":
    run()
