import logging

import pytest

from chronutils.calculator import (
    calculate_elapsed_hours,
    calculate_hours_balance,
    calculate_total_hours,
    parse_timestamps,
)

logger = logging.getLogger(__name__)


def test_parse_timestamps(records):
    for index, scenario in enumerate(records):
        input = scenario['input']
        logger.info(f'Running scenario {index+1}/{len(records)}::{input}')
        output = parse_timestamps(input)
        expected_output = scenario['expected_parsed_timestamps_output']
        assert output == expected_output


def test_calculate_elapsed_hours(records):
    for index, scenario in enumerate(records):
        input = scenario['input']
        logger.info(f'Running scenario {index+1}/{len(records)}::{input}')
        output = calculate_elapsed_hours(input)
        expected_output = scenario['expected_calculate_elapsed_hours_output']
        assert output == expected_output


def test_calculate_hours_balance(balance_records):
    for index, scenario in enumerate(balance_records):
        input = scenario['input']
        logger.info(
            f'Running scenario {index+1}/{len(balance_records)}::{input}'
        )
        output = calculate_hours_balance(input)
        expected_output = scenario['expected_hours_balance_output']
        assert output == expected_output


# TODO: refactor to use pytest parametrize instead of conftest here
@pytest.mark.parametrize(
    "index,records,expected",
    [
        (0, ['16/02 - -00:15', '17/02 - -02:00'], '-2:15'),
        (1, ['16/02 - 00:15', '17/02 - -02:00'], '-1:45'),
        (2, ['16/02 - -00:15', '17/02 - 02:00'], '1:45'),
        (3, ['16/02 - -08:00', '17/02 - 02:00'], '-6:00'),
        (4, ['16/02 - 12:00', '17/02 - -02:00'], '10:00'),
        (
            5,
            [
                '16/02 - -08:00',
                '17/02 - 02:00',
                '18/02 - 08:00',
                '19/02 - 08:00',
                '20/02 - 12:00',
                '21/02 - 8:00',
            ],
            '30:00',
        ),
    ],
)
def test_calculate_total_hours(index, records, expected):
    output = calculate_total_hours(records)
    assert output == expected
