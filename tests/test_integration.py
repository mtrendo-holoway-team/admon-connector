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
            {"2024-07-01": pytest.approx(57_018, abs=1)},
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
    "date_from, date_to, expected_sum, expected_amount",
    [
        (date(2024, 10, 25), date(2024, 10, 27), pytest.approx(9_415_394, abs=1), 1468),
    ],
)
async def test_load(date_from, date_to, expected_sum, expected_amount):
    settings = Settings()
    connector = AdmonConnector(settings.admon_token)

    result = [item async for item in connector.load(date_from, date_to)]
    assert len(result) == expected_amount
    assert sum([item.totalPrice for item in result]) == expected_sum
