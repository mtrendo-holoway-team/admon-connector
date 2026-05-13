from datetime import date

import pytest

from admon_connector.interface import AdMonCostRef


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
async def test_check(connector, date_from, date_to, expected):
    result = await connector.check(date_from, date_to)
    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_from, date_to, expected_sum, expected_amount",
    [
        (date(2024, 10, 25), date(2024, 10, 27), pytest.approx(9_415_394, abs=1), 1468),
    ],
)
async def test_load(connector, date_from, date_to, expected_sum, expected_amount):
    result = [item async for item in connector.load(date_from, date_to)]
    assert len(result) == expected_amount
    assert sum([item.totalPrice for item in result]) == expected_sum


@pytest.mark.asyncio
async def test_load_ref(connector):
    result = [item async for item in connector.load_ref(date(2024, 10, 25), date(2024, 10, 26))]
    assert len(result) == 2
    assert result == [
        AdMonCostRef(date=date(2024, 10, 26), totalPrice=2735354.91, reward=204221.5),
        AdMonCostRef(date=date(2024, 10, 25), totalPrice=3653263.83, reward=241017.44),
    ]
