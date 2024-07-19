from collections import defaultdict
from collections.abc import Iterable
from datetime import date

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from admon_connector.interface import AdMonCalc, AdMonCost, Connector, ConversionPage
from admon_connector.settings import settings


class AdmonConnector(Connector):
    client: Client

    def __init__(self, token=settings.admon_token):
        transport = AIOHTTPTransport(
            url="https://partner.letu.ru/api/graphql",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        self.client = Client(transport=transport, fetch_schema_from_transport=False)

    def __request(self, fields):
        return gql(
            f"""
        query conversions(
        $where: ConversionFilterInput,
        $order: String,
        $limit: Int,
        $offset: Int
        ) {{
            conversions(
                where: $where,
                order: $order,
                limit: $limit,
                offset: $offset
            ) {{
                count
                rows {{
                {'\n'.join(fields)}
                }}
            }}
        }}
        """
        )

    def __get_params(self, date_from: date, date_to: date, offset: int, limit=100):
        params = {
            "limit": limit,
            "offset": offset,
            "order": "reverse:time",
            "where": {
                "endTz": f"{date_to.isoformat()}T23:59:59.999+03:00",
                "startTz": f"{date_from.isoformat()}T00:00:00.000+03:00",
            },
        }
        return params

    async def load(self, date_from: date, date_to: date) -> Iterable[AdMonCost]:
        offset = 0
        limit = 100
        while True:
            response = await self.client.execute_async(
                document=self.__request(AdMonCost.model_fields.keys()),
                variable_values=self.__get_params(date_from=date_from, date_to=date_to, offset=offset, limit=limit),
            )

            page = ConversionPage(**response["conversions"])
            offset += limit
            for item in page.rows:
                yield item

            if offset > page.count:
                break

    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        offset = 0
        limit = 100
        result = []
        while True:
            response = await self.client.execute_async(
                document=self.__request(AdMonCalc.model_fields.keys()),
                variable_values=self.__get_params(date_from=date_from, date_to=date_to, offset=offset, limit=limit),
            )

            page = ConversionPage(**response["conversions"])
            offset += limit
            result.extend(page.rows)
            if offset > page.count:
                break
        agg_res = defaultdict(float)
        for item in result:
            agg_res[item.date.isoformat()] += item.reward

        return agg_res
