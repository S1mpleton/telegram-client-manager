from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from api import router_api
from broker import broker
from core.model_creator import ApiErrorContainer
from storage import get_basic_redis_client


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    await broker.start()
    await get_basic_redis_client().connect()
    yield
    await broker.stop()
    await get_basic_redis_client().disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router_api)



@app.exception_handler(ApiErrorContainer)
async def global_handler(request: Request, exc: ApiErrorContainer):
    return JSONResponse(
        status_code=exc._model_instance.status_code,
        content=exc._model_instance.model_dump(exclude_none=True)
    )

app.add_exception_handler(ApiErrorContainer, global_handler)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    print("Type response ", type(response))
    print("Response ", response)


    return response


origins = [
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
