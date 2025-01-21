from fastapi import HTTPException, APIRouter
from common.mongo_client import db
from crypto_api.models import CryptoCurrencyModel
from crypto_api.services import fetch_cryptocurrencies
from crypto_api.kafka_producer import send_message
from crypto_api.kafka_consumer import consume_messages
import threading

crypto_api_router = APIRouter()


@crypto_api_router.get('/crypto-api/coinmarketcap')
async def get_cryptocurrencies(symbol: str = None, limit: int = 100):
    try:
        coins = fetch_cryptocurrencies(symbol=symbol, limit=limit)
        send_message('coins', coins)
        return coins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@crypto_api_router.post('/crypto-api/cryptocurrencies')
async def create_cryptocurrency(crypto: CryptoCurrencyModel):
    print(crypto)
    existing = await db.crypto_currency.find_one({'coin_id': crypto.coin_id})
    if existing:
        raise HTTPException(status_code=400, detail='Cryptocurrency already exists')
    result = await db.crypto_currency.insert_one(crypto.model_dump(by_alias=True))
    crypto.id = result.inserted_id
    return crypto


@crypto_api_router.delete('/crypto-api/cryptocurrencies/{coin_id}')
async def delete_cryptocurrency(coin_id: int):
    result = await db.crypto_currency.delete_one({'coin_id': coin_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail='Cryptocurrency not found')
    return {'message': 'Cryptocurrency deleted'}


@crypto_api_router.get('/crypto-api/cryptocurrencies')
async def get_cryptocurrencies_from_db(limit: int = 100):
    try:
        saved_crypto = await db.crypto_currency.find().to_list(limit)
        coin_symbols = [crypto['symbol'] for crypto in saved_crypto]

        params = {'symbol': ",".join(coin_symbols), 'limit': limit}

        coins = fetch_cryptocurrencies(**params)

        if not isinstance(coins, list):
            raise HTTPException(
                status_code=500, detail="Unexpected response from CoinMarketCap API"
            )

        send_message('user_coins', coins)
        return coins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_kafka_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()


if __name__ == '__main__':
    start_kafka_consumer()
