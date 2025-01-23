import requests
import json
from common.config import COINMAKERCAP_TOKEN
from common.redis_client import redis_client

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/'


def get_data_from_redis(redis_key: str):
    cached_data = redis_client.get(redis_key)
    if cached_data:
        print('Data fetched from Redis')
        return json.loads(cached_data)
    return None


def fetch_data_from_coinmaketcap(symbol: str = None, limit: int = 100):
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


def fetch_cryptocurrencies(symbol: str = None, limit: int = 100):
    redis_key = f'cryptocurrencies_{symbol}_{limit}'
    data = get_data_from_redis(redis_key)
    if data:
        return data
    data = fetch_data_from_coinmaketcap(symbol, limit)
    redis_client.set(redis_key, json.dumps(data), ex=3600)
    print(f"Data saved to Redis for key: {redis_key}")
    return data
