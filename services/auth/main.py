from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from api.v1.views import router as main_router
from core.config import SETTINGS


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    async with RegisterTortoise(
        app=api_app,
        config_file=SETTINGS.database.path_to_config,
        use_tz=True,
        timezone=SETTINGS.database.timezone,
        generate_schemas=True
    ):
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)




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
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
