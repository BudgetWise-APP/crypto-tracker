import time
import hmac
import hashlib
from bson import ObjectId
import httpx
from urllib.parse import urlencode
from common.mongo_client import db


class BinanceService:
    BASE_URL = 'https://api.binance.com'

    @staticmethod
    async def get_account_info(user_id: str) -> dict:
        binance_credentials = await BinanceService.get_binance_data(user_id)

        if not binance_credentials:
            return {"message": "No Binance credentials found"}

        endpoint = "/api/v3/account"
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp}

        query = urlencode(params)
        signature = BinanceService.sign(query, binance_credentials["secret_key"])

        headers = {"X-MBX-APIKEY": binance_credentials["api_key"]}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BinanceService.BASE_URL}{endpoint}?{query}&signature={signature}",
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_total_balance_in_usd(user_id: str) -> float:
        account_info = await BinanceService.get_account_info(user_id)
        prices = await BinanceService.get_prices()

        total_in_usd = sum(
            float(asset["free"]) * float(prices.get(f'{asset["asset"]}USDT', "0"))
            for asset in account_info.get("balances", [])
        )

        return total_in_usd

    @staticmethod
    async def get_binance_data(user_id: str):
        integration = await db.integrations.find_one(
            {'user_id': ObjectId(user_id), 'platform': 'binance'}
        )
        if not integration:
            return None

        return {
            'api_key': integration['api_key'],
            'secret_key': integration['secret_key'],
        }

    @staticmethod
    async def get_prices() -> dict:
        endpoint = "/api/v3/ticker/price"

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BinanceService.BASE_URL}{endpoint}")
            response.raise_for_status()

            prices = response.json()
            return {price["symbol"]: price["price"] for price in prices}

    @staticmethod
    def sign(query: str, secret_key: str) -> str:
        return hmac.new(
            secret_key.encode("utf-8"), query.encode("utf-8"), hashlib.sha256
        ).hexdigest()
