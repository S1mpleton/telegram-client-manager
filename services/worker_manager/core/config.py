import logging

from pydantic import BaseModel, Field

MQ_WORKERS_QUEUE = "worker_responses"


class RabbitMQConfig(BaseModel):
    message_type: str = Field(default="application/json")
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=5600)
    login: str = Field(default="guest")
    password: str = Field(default="guest")

    def get_amqp_url(self):
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/"


class RedisConfig(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=6300)
    password: str = Field(default="guest")
    db: int = Field(default=0)


class LoggingConfig(BaseModel):
    level: int = Field(default=logging.INFO)


class Settings(BaseModel):
    rabbit_mq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)


SETTINGS = Settings()
