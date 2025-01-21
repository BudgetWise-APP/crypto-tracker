from pydantic import BaseModel


class CryptoCurrencySchema(BaseModel):
    coin_id: int
    name: str
    symbol: str
