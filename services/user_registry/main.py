from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise
from shared_http import register_app

from api import router_api
from core.config import SETTINGS
from infrastructure.broker import broker


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    db = RegisterTortoise(
        app=api_app,
        config_file=SETTINGS.database.path_to_config,
        use_tz=True,
        timezone=SETTINGS.database.timezone,
        generate_schemas=True
    )

    await db.init_orm()
    await broker.start()

    yield

    await db.close_orm()
    await broker.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(router_api)

register_app(app)


origins = [
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
