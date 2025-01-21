from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crypto_api.database import db
from crypto_api.models import CryptoCurrencyModel
from crypto_api.services import fetch_cryptocurrencies
from crypto_api.kafka_producer import send_message
from crypto_api.kafka_consumer import consume_messages
import threading

app = FastAPI()

origins = [
  'http://localhost:8899',
  'http://10.0.11.165:8899',
  'http://10.2.0.2:8899', 
  'https://budgetwise-chi.vercel.app'
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=['*'],
   allow_headers=['*']
)

@app.get('/v1/crypto-api/coinmarketcap')
async def get_cryptocurrencies(
   symbol: str = None,
   limit: int = 100
):
   try:
      coins = fetch_cryptocurrencies(symbol=symbol, limit=limit)
      send_message('coins', coins)
      return coins
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
   
@app.post('/v1/crypto-api/cryptocurrencies')
async def create_cryptocurrency(crypto: CryptoCurrencyModel):
   print(crypto)
   existing = await db.crypto_currency.find_one({'coin_id': crypto.coin_id})
   if existing:
      raise HTTPException(status_code=400, detail='Cryptocurrency already exists')
   result = await db.crypto_currency.insert_one(crypto.model_dump(by_alias=True))
   crypto.id = result.inserted_id
   return crypto

@app.delete('/v1/crypto-api/cryptocurrencies/{coin_id}')
async def delete_cryptocurrency(coin_id: int):
   result = await db.crypto_currency.delete_one({'coin_id': coin_id})
   if result.deleted_count == 0:
      raise HTTPException(status_code=404, detail='Cryptocurrency not found')
   return {'message': 'Cryptocurrency deleted'}

@app.get('/v1/crypto-api/cryptocurrencies')
async def get_cryptocurrencies(limit: int = 100): 
   try:
      saved_crypto = await db.crypto_currency.find().to_list(limit)
      coin_symbols = [crypto['symbol'] for crypto in saved_crypto]

      params = {
         'symbol': ",".join(coin_symbols),
         'limit': limit
      }

      coins = fetch_cryptocurrencies(**params)
      
      if not isinstance(coins, list):
         raise HTTPException(status_code=500, detail="Unexpected response from CoinMarketCap API")
      
      send_message('user_coins', coins)
      return coins
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


def start_kafka_consumer():
   consumer_thread = threading.Thread(target=consume_messages)
   consumer_thread.start()

if(__name__ == '__main__'):
   start_kafka_consumer()