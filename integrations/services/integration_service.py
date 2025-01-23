from common.mongo_client import db
from bson import ObjectId
from fastapi import HTTPException
from jose import jwt, JWTError
from common.config import JWT_SECRET, ALGORITHM


class IntegrationsService:
    @staticmethod
    def get_user_id_from_jwt(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("userId")
            if user_id is None:
                raise HTTPException(status_code=401, detail="UserID not found in token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    async def link_platform(user_id: str, platform: str, api_key: str, secret_key: str):
        existing = await db.integrations.find_one(
            {'user_id': ObjectId(user_id), 'platform': platform}
        )

        if existing:
            await db.integrations.update_one(
                {'_id': existing['_id']},
                {'$set': {'api_key': api_key, 'secret_key': secret_key}},
            )
        else:
            await db.integrations.insert_one(
                {
                    'user_id': ObjectId(user_id),
                    'platform': platform,
                    'api_key': api_key,
                    'secret_key': secret_key,
                }
            )
        return {"message": "Platform linked successfully"}

    @staticmethod
    async def unlink_platform(user_id: str, platform: str):
        await db.integrations.delete_one(
            {'user_id': ObjectId(user_id), 'platform': platform}
        )
        return {"message": "Platform unlinked successfully"}

    @staticmethod
    async def get_platforms(user_id: str):
        integrations = await db.integrations.find( {"user_id": ObjectId(user_id)}, {"_id": 0, "user_id": 0}).to_list(length=10)
        return integrations
