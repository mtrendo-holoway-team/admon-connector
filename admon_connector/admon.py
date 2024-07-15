from datetime import date
from admon_connector.interface import AdMonCost, ConversionPage, Connector
from gql.transport.aiohttp import (AIOHTTPTransport, TransportQueryError) # в зависимости
from gql import gql, Client

class AdmonConnector(Connector):
    transport = AIOHTTPTransport(
        url='https://partner.letu.ru/api/graphql',
        headers={
            "Authorization": f"Bearer {token}", #из окружения
            "Content-Type": "application/json"
        }
    )
    
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )
    
    request = gql(
        '''
        query conversions(
          $where: ConversionFilterInput,
          $order: String,
          $limit: Int,
          $offset: Int
        ) {
          conversions(
            where: $where,
            order: $order,
            limit: $limit,
            offset: $offset
          ) {
            count
            rows {
              id
              offerId
              date
              status
              comment
              totalPrice
              reward
              hold
              type
            }
          }
        }
      '''
    )
    
    def get_params(self, date_from : date, date_to : date, offset : int, limit = 100, order = "reverse:time"):
        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "where": {
                "endTz": f"{date_to.isoformat()}T23:59:59.999+03:00",
                "startTz": f"{date_from.isoformat()}T00:00:00.000+03:00"
            }
        }
        return params
    
    async def load(self, date_from: date, date_to: date) -> list[AdMonCost]:
        
        #def request
        offset = 0
        limit = 100
        
        while True: #Do while
            response = await self.client.execute_async(
                    self.request, 
                    variable_values=self.get_params(
                        date_from=date_from, 
                        date_to=date_to, 
                        offset=offset,
                        limit=limit
                )
            )
            #except TransportQueryError
            
            print(offset) # debug
            page = ConversionPage(**response['conversions'])
            offset+=limit
            if offset > page.count:
                break
            #    return page.rows load method / reduce page.rows.reward check method
            
        
        return await super().load(date_from, date_to)
    
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        
        return await super().check(date_from, date_to)
