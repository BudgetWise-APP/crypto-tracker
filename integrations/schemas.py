from pydantic import BaseModel


class LinkPlatformRequest(BaseModel):
    platform: str
    api_key: str
    secret_key: str
