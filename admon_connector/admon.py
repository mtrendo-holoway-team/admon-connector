import csv
from collections import defaultdict
from collections.abc import AsyncIterator
from datetime import date

import requests

from admon_connector.interface import AdMonCost, Connector


class AdmonConnector(Connector):
    def __init__(self, token: str):
        self.token = token

    def __request(self, params: dict) -> str:
        url = "https://partner.letu.ru/api/exports/conversions"

        payload = {
            "format": "csv",
            "dimension": "conversions",
            "order": "reverse:time",
            "withoutItem": "true",
            "withAttribution": "true",
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, params={**payload, **params}, headers=headers, timeout=7200)
        response.encoding = response.apparent_encoding
        return str(response.text)

    def __get_admon_csv(self, date_from: date, date_to: date) -> csv.DictReader:
        where = {
            "where": f'{{"startTz" : "{date_from}T00:00:00.000+03:00","endTz": "{date_to}T23:59:59.000+03:00"}}',
            "fieldsToInclude[]": AdMonCost.model_fields.keys(),
        }
        response = self.__request(where)
        return csv.DictReader(response.splitlines(), delimiter=",")

    async def load(self, date_from: date, date_to: date) -> AsyncIterator[AdMonCost]:
        for row in self.__get_admon_csv(date_from, date_to):
            res = AdMonCost.model_validate(row)
            yield res

    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        agg_res: defaultdict = defaultdict(float)
        for row in self.__get_admon_csv(date_from, date_to):
            row_model = AdMonCost.model_validate(row)
            agg_res[row_model.time.date().isoformat()] += row_model.reward
        return dict(agg_res)
