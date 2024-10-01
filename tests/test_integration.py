from datetime import date

import pytest

from admon_connector.admon import AdmonConnector
from admon_connector.settings import Settings


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
    settings = Settings()
    connector = AdmonConnector(settings.admon_token)

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
    settings = Settings()
    connector = AdmonConnector(settings.admon_token)

    result = [item async for item in connector.load(date_from, date_to)]
    print(result)
    assert len(result) == expected_amount
    assert sum([item.totalPrice for item in result]) == expected_sum
