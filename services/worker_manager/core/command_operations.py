from broker.schemas import (
    QueueResponseCreateMessageSchema,
    ResponseCommandStatuses,
    CommandTypes,
    ClientResponseAuthMessageSchema, StorgeCommandStatuses, ClientResponseStartMessageSchema,
    ClientResponseStopMessageSchema
)
from core.worker_manager import WorkerManager
from storage import task_repo


async def create_queue_action(data: QueueResponseCreateMessageSchema):
    if data.status == ResponseCommandStatuses.error:
        raise ValueError(f"Create queue error: {data}")


    await WorkerManager().register_worker(data.payload.queue_name)


async def auth_client_action(data: ClientResponseAuthMessageSchema):
    if data.status == ResponseCommandStatuses.error:
        raise ValueError(f"Auth client error: {data}")

    await task_repo.set_payload(data.command_id, {
        "status": StorgeCommandStatuses.completed
    })


async def start_client_action(data: ClientResponseStartMessageSchema):
    if data.status == ResponseCommandStatuses.error:
        raise ValueError(f"Auth client error: {data}")

    await task_repo.set_payload(data.command_id, {
        "status": StorgeCommandStatuses.completed
    })


async def stop_client_action(data: ClientResponseStopMessageSchema):
    if data.status == ResponseCommandStatuses.error:
        raise ValueError(f"Auth client error: {data}")

    await task_repo.set_payload(data.command_id, {
        "status": StorgeCommandStatuses.completed
    })



command_route = {
    CommandTypes.queue_create: create_queue_action,

    CommandTypes.auth_bot: auth_client_action,
    CommandTypes.auth_client: auth_client_action,

    CommandTypes.client_start: start_client_action,
    CommandTypes.client_stop: stop_client_action,
}
