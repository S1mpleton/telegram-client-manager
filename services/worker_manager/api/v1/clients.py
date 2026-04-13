import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from api.v1.schemas import (
    BotAuthSchema,
    http_202_accepted,
    http_500_internal_server_error, ClientAuthSchema,
)
from api.v1.schemas.tasks import TaskIDSchema
from broker import broker
from broker.schemas import (
    BotAuthMessageSchema,
    BotAuthPayloadSchema,
    ClientAuthMessageSchema,
    ClientAuthPayloadSchema,
    StorgeCommandStatuses,
)

from core.dependencies import get_user_id_from_header
from core.worker_manager import WorkerManager
from storage import task_repo

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["clients"],
    prefix="/client",
)


@router.post(
    "/authBot",
    summary="Telegram bot authentication",
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        200: {
            "description": "Not used - the successful response for this endpoint is code 202"
        },
        202: {
            "model": http_202_accepted(TaskIDSchema).model,
            "description": "The Telegram bot authentication data has been accepted"
        },
    }
)
async def bot_authentication(
        user_id: Annotated[int, Depends(get_user_id_from_header)],
        auth_data: Annotated[BotAuthSchema, Body()]
):
    message = BotAuthMessageSchema(
        payload=BotAuthPayloadSchema(
            user_id=user_id,
            **auth_data.model_dump()
        )
    )

    try:
        available_worker = await WorkerManager().get_available_worker()

        await broker.publish(
            queue=available_worker.worker_id,
            message=message,
            message_type=BotAuthMessageSchema
        )

        await task_repo.set_payload(message.command_id, {
            "status": StorgeCommandStatuses.execution,
            "user_id": user_id
        })

        return http_202_accepted(TaskIDSchema)(payload=TaskIDSchema(
            task_id=message.command_id)
        ).json_response

    except Exception as e:
        logger.error(f"Route /authBot error: {e}")
        raise http_500_internal_server_error()(detail=f"Route /authBot error: {e}")


@router.post(
    "/authClient",
    summary="Telegram client authentication",
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        200: {
            "description": "Not used - the successful response for this endpoint is code 202"
        },
        202: {
            "model": http_202_accepted(TaskIDSchema).model,
            "description": "The Telegram client authentication data has been accepted"
        },
    }
)
async def client_authentication(
        user_id: Annotated[int, Depends(get_user_id_from_header)],
        auth_data: Annotated[ClientAuthSchema, Body()]
):
    message = ClientAuthMessageSchema(
        payload=ClientAuthPayloadSchema(
            user_id=user_id,
            **auth_data.model_dump()
        )
    )

    try:
        available_worker = await WorkerManager().get_available_worker()

        await broker.publish(
            queue=available_worker.worker_id,
            message=message,
            message_type=ClientAuthMessageSchema
        )

        await task_repo.set_payload(message.command_id, {
            "status": StorgeCommandStatuses.execution,
            "user_id": user_id
        })

        return http_202_accepted(TaskIDSchema)(payload=TaskIDSchema(
            task_id=message.command_id)
        ).json_response

    except Exception as e:
        logger.error(f"Route /authClient error: {e}")
        raise http_500_internal_server_error()(detail=f"Route /authClient error: {e}")
