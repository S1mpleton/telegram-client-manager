import pika

RMQ_HOST = "127.0.0.1"
RMQ_PORT = 5600

RMQ_USER = "guest"
RMQ_PASSWORD = "guest"

connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(username=RMQ_USER, password=RMQ_PASSWORD)
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=connection_params
    )
