import requests
from common.config import COINMAKERCAP_TOKEN

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/'


def fetch_cryptocurrencies(symbol: str = None, limit: int = 100):
    headers = {'X-CMC_PRO_API_KEY': COINMAKERCAP_TOKEN}
    params = {'limit': limit}
    if symbol:
        params['symbol'] = symbol
    url = f'{COINMARKETCAP_API_URL}cryptocurrency/map'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from CoinMarketCap: {response.text}')
    data = response.json()
    return [
        {'coin_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']}
        for coin in data['data']
    ]
