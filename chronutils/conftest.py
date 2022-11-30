from datetime import datetime

import pytest


@pytest.fixture
def records():
    current_year = datetime.now().year
    next_year = current_year + 1

    return [
        {
            'input': '31/12 (23:15 0:00)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 12, 31, 23, 15),
                datetime(next_year, 1, 1, 0, 0),
            ],
            'expected_calculate_elapsed_hours_output': '00:45',
        },
        {
            'input': '31/12 (23:15 0:15)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 12, 31, 23, 15),
                datetime(next_year, 1, 1, 0, 15),
            ],
            'expected_calculate_elapsed_hours_output': '01:00',
        },
        {
            'input': '31/12 (23:15 23:14)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 12, 31, 23, 15),
                datetime(next_year, 1, 1, 23, 14),
            ],
            'expected_calculate_elapsed_hours_output': '23:59',
        },
        {
            'input': '31/12 (23:15 23:15)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 12, 31, 23, 15),
                datetime(current_year, 12, 31, 23, 15),
            ],
            'expected_calculate_elapsed_hours_output': '00:00',
        },
        {
            'input': '31/12 (23:15 23:16)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 12, 31, 23, 15),
                datetime(current_year, 12, 31, 23, 16),
            ],
            'expected_calculate_elapsed_hours_output': '00:01',
        },
        {
            'input': '31/12/1999 (23:15 23:14)',
            'expected_parsed_timestamps_output': [
                datetime(1999, 12, 31, 23, 15),
                datetime(2000, 1, 1, 23, 14),
            ],
            'expected_calculate_elapsed_hours_output': '23:59',
        },
        {
            'input': '30/01 (06:50 11:43 12:20 18:32)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 1, 30, 6, 50),
                datetime(current_year, 1, 30, 11, 43),
                datetime(current_year, 1, 30, 12, 20),
                datetime(current_year, 1, 30, 18, 32),
            ],
            'expected_calculate_elapsed_hours_output': '11:05',
        },
        {
            'input': '30/01 (23:50 01:43 01:44 03:15)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 1, 30, 23, 50),
                datetime(current_year, 1, 31, 1, 43),
                datetime(current_year, 1, 31, 1, 44),
                datetime(current_year, 1, 31, 3, 15),
            ],
            'expected_calculate_elapsed_hours_output': '03:24',
        },
        {
            'input': f'30/01/{current_year} (06:50 11:43 12:20 18:32)',
            'expected_parsed_timestamps_output': [
                datetime(current_year, 1, 30, 6, 50),
                datetime(current_year, 1, 30, 11, 43),
                datetime(current_year, 1, 30, 12, 20),
                datetime(current_year, 1, 30, 18, 32),
            ],
            'expected_calculate_elapsed_hours_output': '11:05',
        },
    ]


@pytest.fixture
def balance_records():
    return [
        {'input': '31/12 - 08:00', 'expected_hours_balance_output': '00:00'},
        {'input': '31/12 - 07:15', 'expected_hours_balance_output': '-00:45'},
        {'input': '31/12 - 23:15', 'expected_hours_balance_output': '15:15'},
        {'input': '31/12 - 04:00', 'expected_hours_balance_output': '-04:00'},
        {'input': '31/12 - 07:01', 'expected_hours_balance_output': '-00:59'},
        {'input': '31/12 - 07:59', 'expected_hours_balance_output': '-00:01'},
        {'input': '31/12 - 08:01', 'expected_hours_balance_output': '00:01'},
    ]
