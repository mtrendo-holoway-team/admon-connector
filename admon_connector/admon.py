import csv
from collections import defaultdict
from collections.abc import Iterator
from datetime import date

import requests

from admon_connector.interface import *
from admon_connector.settings import settings


class AdmonConnector(Connector):
    def __init__(self, token=settings.admon_token) -> None:
        self.token = token

    def __request(self, params: dict) -> str:
        url = "https://partner.letu.ru/api/exports/conversions"

        payload = {
            "format": "csv",
            "dimension": "conversions",
            "order": "reverse:time",
            "withoutItem": "true",
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, params={**payload, **params}, headers=headers, timeout=7200)
        response.encoding = response.apparent_encoding
        return response.text

    def __get_admon_csv(self, date_from: date, date_to: date) -> list[dict]:
        where = {
            "where": f'{{"startTz" : "{date_from}T00:00:00.000+03:00","endTz": "{date_to}T23:59:59.000+03:00"}}',
            "fieldsToInclude[]": AdMonCost.model_fields.keys(),
        }
        response = self.__request(where)
        return csv.DictReader(response.splitlines(), delimiter=",")

    async def load(self, date_from: date, date_to: date) -> AsyncGenerator[AdMonCost]:
        for row in self.__get_admon_csv(date_from, date_to):
            res = AdMonCost.model_validate(row)
            yield res

    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        agg_res = defaultdict(float)
        for row in self.__get_admon_csv(date_from, date_to):
            row = AdMonCost.model_validate(row)
            agg_res[row.time.date().isoformat()] += row.reward
        return dict(agg_res)
