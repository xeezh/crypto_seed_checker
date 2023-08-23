import requests
import json
from asyncio import sleep

class AVAX:
    def __init__(self, token: str, offset: int):
        self.__token = token
        self.__offset = offset

    async def get_transactions(self, address):
        data = {
            'limit': self.__offset,
            'count': True,
            'ecosystem': 'avalanche'
        }
        resp_raw = requests.get(f'https://api-beta.avascan.info/v2/network/mainnet/evm/43114/address/{address[0]}/transactions', params=data)
        if resp_raw.status_code == 200:
            resp = json.loads(resp_raw.text)
            return len(resp['items'])
        else:
            await sleep(1)
            return await self.get_transactions(address)
