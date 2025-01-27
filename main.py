import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common.kafka_consumer import consume_messages
from crypto_api.main import crypto_api_router
from integrations.main import integrations_router
from common.config import KAFKA_TOPIC_INTEGRATIONS, ORIGINS


async def start_kafka_consumer():
    asyncio.create_task(consume_messages(KAFKA_TOPIC_INTEGRATIONS))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka_consumer()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(crypto_api_router, prefix="/api/v1")
app.include_router(integrations_router, prefix="/api/v1")
