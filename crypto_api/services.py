import requests
import json
from jose import jwt, JWTError
from fastapi import HTTPException
from common.config import COINMAKERCAP_TOKEN, JWT_SECRET, ALGORITHM
from common.mongo_client import db
from common.redis_service import CacheService
from crypto_api.models import CryptoCurrencyModel

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/'


class CryptoApiService:
    @staticmethod
    async def fetch_data_from_coinmaketcap(symbol: str = None, limit: int = 100):
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

    @staticmethod
    async def fetch_cryptocurrencies(symbol: str = None, limit: int = 100):
        redis_key = f'cryptocurrencies_{symbol}_{limit}'
        data = await CacheService.get_data_from_redis(redis_key)
        if data:
            return data
        data = await CryptoApiService.fetch_data_from_coinmaketcap(symbol, limit)
        CacheService.set_data_to_redis(redis_key, json.dumps(data), ex=3600)
        print(f"Data saved to Redis for key: {redis_key}")
        return data

    @staticmethod
    def get_email_from_jwt(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise HTTPException(status_code=401, detail="Email not found in token")
            return email
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    async def add_cryptocurrency(crypto: CryptoCurrencyModel):
        existing = await db.crypto_currency.find_one({'coin_id': crypto.coin_id})
        if existing:
            raise HTTPException(status_code=400, detail='Cryptocurrency already exists')
        await db.crypto_currency.insert_one(crypto.model_dump(by_alias=True))
        return existing

    @staticmethod
    async def delete_cryptocurrency(coin_id: int):
        result = await db.crypto_currency.delete_one({'coin_id': coin_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Cryptocurrency not found')
        return {'message': 'Cryptocurrency deleted'}

    @staticmethod
    async def get_cryptocurrencies_from_db(limit: int):
        saved_crypto = await db.crypto_currency.find().to_list(limit)
        if not saved_crypto:
            return []

        coin_ids = [str(crypto['coin_id']) for crypto in saved_crypto]
        coin_symbols = [crypto['symbol'] for crypto in saved_crypto]
        params = {'symbol': ",".join(coin_symbols), 'limit': limit}
        coins = await CryptoApiService.fetch_cryptocurrencies(**params)
        if not isinstance(coins, list):
            raise HTTPException(
                status_code=500, detail="Unexpected response from CoinMarketCap API"
            )
        filtered_coins = [
            coin for coin in coins if str(coin.get('coin_id')) in coin_ids
        ]

        if not filtered_coins:
            return []
        return filtered_coins
