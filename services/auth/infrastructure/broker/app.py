from faststream import FastStream
from infrastructure.broker.fs_broker import broker

app = FastStream(broker)
