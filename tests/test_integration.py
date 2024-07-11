from datetime import date

import pytest

from admon_connector.admon import AdmonConnector


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_from,date_to,expected",
    [
        (
            date(2024, 1, 1),
            date(2024, 1, 2),
            {date(2024, 1, 1): 0, date(2024, 1, 2): 0},
        ),
    ],
)
async def test_check(date_from, date_to, expected):
    connector = AdmonConnector()

    result = await connector.check(date_from, date_to)

    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_from,date_to,expected",
    [
        (
            date(2024, 1, 1),
            date(2024, 1, 2),
            100,
        ),
    ],
)
async def test_load(date_from, date_to, expected):
    connector = AdmonConnector()

    result = await connector.load(date_from, date_to)

    assert sum([item.cost for item in result]) == expected
