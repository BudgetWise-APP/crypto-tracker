from common.mongo_client import db
from bson import ObjectId


class IntegrationsService:
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

    @staticmethod
    async def unlink_platform(user_id: str, platform: str):
        await db.integrations.delete_one(
            {'user_id': ObjectId(user_id), 'platform': platform}
        )

    @staticmethod
    async def get_platforms(user_id: str):
        return await db.integrations.find({'user_id': ObjectId(user_id)}).to_list(None)
