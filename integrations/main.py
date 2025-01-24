from fastapi import Depends, HTTPException, APIRouter

from common.get_current_user import get_current_user
from .services.integration_service import IntegrationsService
from .services.binance_service import BinanceService
from .services.bybit_service import BybitService
from .schemas import LinkPlatformRequest
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
integrations_router = APIRouter()


@integrations_router.post('/integrations/link-platform')
async def link_platform(
    data: LinkPlatformRequest,
    user_id: str = Depends(get_current_user("userId")),
):
    try:
        await IntegrationsService.link_platform(
            user_id, data.platform, data.api_key, data.secret_key
        )
        return {"message": "Platform linked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@integrations_router.delete('/integrations/unlink-platform/{platform}')
async def unlink_platform(
    platform: str, user_id: str = Depends(get_current_user("userId"))
):
    try:
        await IntegrationsService.unlink_platform(user_id, platform)
        return {"message": "Platform unlinked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@integrations_router.get('/integrations')
async def get_platforms(user_id: str = Depends(get_current_user("userId"))):
    try:
        integrations = await IntegrationsService.get_platforms(user_id)
        print(integrations)
        return {"integrations": integrations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@integrations_router.get('/binance/account')
async def get_binance_account(user_id: str = Depends(get_current_user("userId"))):
    try:
        total_balance = await BinanceService.get_total_balance_in_usd(user_id)
        return {"total_balance": total_balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@integrations_router.get('/bybit/account')
async def get_bybit_account(user_id: str = Depends(get_current_user("userId"))):
    try:
        total_balance = await BybitService.get_account_info(user_id)
        return {"total_balance": total_balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
