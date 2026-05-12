import csv
from collections import defaultdict
from collections.abc import AsyncIterator
from datetime import date

import requests

from admon_connector.interface import AdMonCost, AdMonCostRef, AdMonCostRefRaw, Connector


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
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, params={**payload, **params}, headers=headers, timeout=7200)
        response.encoding = response.apparent_encoding
        return str(response.text)

    def __get_admon_csv(self, date_from: date, date_to: date, fields: list[str]) -> csv.DictReader:
        where = {
            "where": (f'{{ "withAttribution": true, "startTz" : "{date_from}T00:00:00.000+03:00","endTz": "{date_to}T23:59:59.000+03:00"}}'),
            "fieldsToInclude[]": fields,
        }
        response = self.__request(where)
        return csv.DictReader(response.splitlines(), delimiter=",")

    async def load(self, date_from: date, date_to: date) -> AsyncIterator[AdMonCost]:
        for row in self.__get_admon_csv(date_from, date_to, fields=list(AdMonCost.model_fields.keys())):
            print(row)
            res = AdMonCost.model_validate(row)
            yield res

    async def load_ref(self, date_from: date, date_to: date) -> AsyncIterator[AdMonCostRef]:
        result: dict[date, AdMonCostRef] = {}
        for row in self.__get_admon_csv(date_from, date_to, fields=list(AdMonCostRefRaw.model_fields.keys())):
            item = AdMonCostRefRaw.model_validate(row)
            day = item.time.date()
            if day not in result:
                result[day] = AdMonCostRef(date=day)
            cost = result[day]
            cost.totalPrice += item.totalPrice
            cost.reward += item.reward

        for cost in result.values():
            yield AdMonCostRef.model_validate(
                {
                    "totalPrice": round(cost.totalPrice, 2),
                    "reward": round(cost.reward, 2),
                    "date": cost.date,
                }
            )

    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        agg_res: defaultdict = defaultdict(float)
        for row in self.__get_admon_csv(date_from, date_to, fields=list(AdMonCost.model_fields.keys())):
            row_model = AdMonCost.model_validate(row)
            agg_res[row_model.time.date().isoformat()] += row_model.reward
        return dict(agg_res)
