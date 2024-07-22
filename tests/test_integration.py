from datetime import date

import pytest

from admon_connector.admon import AdmonConnector


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_from,date_to,expected",
    [
        (
            date(2024, 7, 1),
            date(2024, 7, 1),
            {date(2024, 7, 1): 1598019.4295},
        ),
    ],
)
async def test_check(date_from, date_to, expected):
    connector = AdmonConnector()

    result = await connector.check(date_from, date_to)

    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_from,date_to,expected_sum, expected_amount",
    [
        (date(2024, 7, 1), date(2024, 7, 1), 1598019.4295, 4938),
    ],
)
async def test_load(date_from, date_to, expected_sum, expected_amount):
    connector = AdmonConnector()

    result = [item async for item in connector.load(date_from, date_to)]
    assert len(result) == expected_amount
    assert sum([item.cost for item in result]) == expected_sum
