import requests

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/'
API_KEY = '32c0bf9f-0d6e-42b8-8d24-6cfee67e77e6'

def fetch_cryptocurrencies(symbol: str = None, limit: int = 100):
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    params = {
        'limit': limit
    }
    if symbol:
        params['symbol'] = symbol
    url = f'{COINMARKETCAP_API_URL}cryptocurrency/map'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from CoinMarketCap: {response.status_code}')
    data = response.json()
    return [{'coin_id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol']} for coin in data['data']]