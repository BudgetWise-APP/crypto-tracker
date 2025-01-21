from pydantic import BaseModel


class LinkPlatformRequest(BaseModel):
    user_id: str
    platform: str
    api_key: str
    secret_key: str
