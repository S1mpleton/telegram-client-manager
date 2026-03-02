from fastapi import FastAPI
import uvicorn
from pydantic import EmailStr, BaseModel

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def hello():
    return {
        "message": "HELLO"
    }


@app.post("/users/")
def hello(user: CreateUser):
    return {
        "email": user.email
    }


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
