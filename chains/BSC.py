import requests
import json
from asyncio import sleep

class BSC:
    def __init__(self, token: str, offset: int):
        self.__token = token
        self.__offset = offset

    async def get_transactions(self, address):
        data = {
            'module': 'account',
            'action': 'txlist',
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'sort': 'asc',
            'offset': self.__offset,
            'apikey': self.__token,
            'address': address[0]
        }
        resp_raw = requests.get('https://api.bscscan.com/api', params=data)
        resp = json.loads(resp_raw.text)
        if resp['status'] == '1':
            transactions_list = resp['result']
            return len(transactions_list)
        else:
            if not resp['message'] == 'No transactions found':
                await sleep(1)
                return await self.get_transactions(address)
            else:
                return 0

