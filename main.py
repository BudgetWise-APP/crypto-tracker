from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crypto_api.main import crypto_api_router
from integrations.main import integrations_router
from common.config import ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(crypto_api_router, prefix="/api/v1")
app.include_router(integrations_router, prefix="/api/v1")
