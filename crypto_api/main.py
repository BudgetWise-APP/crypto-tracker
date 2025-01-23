from fastapi import Depends, HTTPException, APIRouter
from crypto_api.models import CryptoCurrencyModel
from crypto_api.services import CryptoApiService
from crypto_api.kafka_producer import send_message
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

crypto_api_router = APIRouter()


@crypto_api_router.get('/crypto-api/coinmarketcap')
async def get_cryptocurrencies(symbol: str = None, limit: int = 100):
    try:
        coins = await CryptoApiService.fetch_cryptocurrencies(
            symbol=symbol, limit=limit
        )
        return coins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@crypto_api_router.post('/crypto-api/cryptocurrencies')
async def create_cryptocurrency(
    crypto: CryptoCurrencyModel, token: str = Depends(oauth2_scheme)
):
    user_email = CryptoApiService.get_email_from_jwt(token)
    created_crypto = await CryptoApiService.add_cryptocurrency(crypto)
    if user_email:
        send_message(
            key="new_coin_added",
            value={
                "user_email": user_email,
                "message": f"{crypto.symbol}-{crypto.name}",
            },
        )
    return created_crypto


@crypto_api_router.delete('/crypto-api/cryptocurrencies/{coin_id}')
async def delete_cryptocurrency(coin_id: int):
    try:
        await CryptoApiService.delete_cryptocurrency(coin_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@crypto_api_router.get('/crypto-api/cryptocurrencies')
async def get_cryptocurrencies_from_db(limit: int = 100):
    try:
        coins = await CryptoApiService.get_cryptocurrencies_from_db(limit)

        send_message('user_coins', coins)
        return coins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
