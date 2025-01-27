import time
import hmac
import hashlib
from bson import ObjectId
import httpx
from common.mongo_client import db
from common.redis_service import CacheService


class BybitService:
    BASE_URL = "https://api.bybit.com"

    @staticmethod
    async def get_account_info(user_id: str) -> dict:
        redis_key = f'integrations_bybit_account_{user_id}'
        data = await CacheService.get_data_from_redis(redis_key)
        if data:
            return data
        
        bybit_credentials = await BybitService.get_bybit_data(user_id)

        if not bybit_credentials:
            return {"message", "No ByBit credentials found"}

        endpoint = "/v5/account/wallet-balance"
        timestamp = str(int(time.time() * 1000))
        recv_window = "20000"
        query_params = "accountType=UNIFIED"

        origin_string = (
            f"{timestamp}{bybit_credentials['api_key']}{recv_window}{query_params}"
        )
        signature = hmac.new(
            bybit_credentials["secret_key"].encode('utf-8'),
            origin_string.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": bybit_credentials["api_key"],
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BybitService.BASE_URL}{endpoint}?{query_params}", headers=headers
            )
            response.raise_for_status()
            result = response.json().get("result", {})
            total_wallet_balance = result.get("list", [{}])[0].get("totalWalletBalance")

            if total_wallet_balance:
                total_wallet_balance = round(float(total_wallet_balance), 2)

            await CacheService.set_data_to_redis(redis_key, total_wallet_balance, ttl=1200)
            return total_wallet_balance

    @staticmethod
    async def get_bybit_data(user_id: str):
        integration = await db.integrations.find_one(
            {'user_id': ObjectId(user_id), 'platform': 'bybit'}
        )
        if not integration:
            return None

        return {
            'api_key': integration['api_key'],
            'secret_key': integration['secret_key'],
        }
