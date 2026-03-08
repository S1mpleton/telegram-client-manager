from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(api_app: FastAPI):
        yield


app = FastAPI(lifespan=lifespan)



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
