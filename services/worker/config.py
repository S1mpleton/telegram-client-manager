import pika
import shortuuid

RMQ_HOST = "127.0.0.1"
RMQ_PORT = 5600

RMQ_USER = "guest"
RMQ_PASSWORD = "guest"

MQ_EXCHANGE = ""

MQ_OUTPUT_QUEUE = "worker_responses"
MQ_INPUT_QUEUE = shortuuid.uuid()

MQ_ROUTING_KEY = "worker_responses"
MQ_WORKER_UNIQUE_ROUTING_KEY = shortuuid.uuid()

connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(username=RMQ_USER, password=RMQ_PASSWORD)
)


