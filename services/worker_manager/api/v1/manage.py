import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from api.v1.schemas import (
    http_202_accepted,
    http_500_internal_server_error,
)
from api.v1.schemas.client_management import ClientLaunchSchema
from api.v1.schemas.tasks import TaskIDSchema
from broker import broker
from broker.schemas import (
    StorgeCommandStatuses,
    ClientStartMessageSchema,
    ClientStartPayloadSchema,
    ClientStopMessageSchema,
    ClientStopPayloadSchema,
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
    "/start",
    summary="Launch the Telegram client",
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        200: {
            "description": "Not used - the successful response for this endpoint is code 202"
        },
        202: {
            "model": http_202_accepted(TaskIDSchema).model,
            "description": "The data for launching the Telegram bot has been accepted"
        },
        500: {
            "model": http_500_internal_server_error().model,
            "description": "Internal server error"
        }
    }
)
async def client_start(
        user_id: Annotated[int, Depends(get_user_id_from_header)],
        auth_data: Annotated[ClientLaunchSchema, Body()]
):
    message = ClientStartMessageSchema(
        payload=ClientStartPayloadSchema(
            user_id=user_id,
            session_string="asdf",
            **auth_data.model_dump()
        )
    )

    try:
        available_worker = await WorkerManager().get_available_worker()

        await broker.publish(
            queue=available_worker.worker_id,
            message=message,
            message_type=ClientStartMessageSchema
        )

        await task_repo.set_payload(message.command_id, {
            "status": StorgeCommandStatuses.execution,
            "user_id": user_id
        })

        return http_202_accepted(TaskIDSchema)(payload=TaskIDSchema(
            task_id=message.command_id)
        ).json_response

    except Exception as e:
        logger.error(f"Route /start error: {e}")
        raise http_500_internal_server_error()(detail=f"Route /start error: {e}")


@router.post(
    "/stop",
    summary="Stop the Telegram client",
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        200: {
            "description": "Not used - the successful response for this endpoint is code 202"
        },
        202: {
            "model": http_202_accepted(TaskIDSchema).model,
            "description": "The data for stopping the Telegram bot has been accepted"
        },
        500: {
            "model": http_500_internal_server_error().model,
            "description": "Internal server error"
        }
    }
)
async def client_start(
        user_id: Annotated[int, Depends(get_user_id_from_header)],
        auth_data: Annotated[ClientLaunchSchema, Body()]
):
    message = ClientStopMessageSchema(
        payload=ClientStopPayloadSchema(
            user_id=user_id,
            **auth_data.model_dump()
        )
    )

    try:
        available_worker = await WorkerManager().get_available_worker()

        await broker.publish(
            queue=available_worker.worker_id,
            message=message,
            message_type=ClientStartMessageSchema
        )

        await task_repo.set_payload(message.command_id, {
            "status": StorgeCommandStatuses.execution,
            "user_id": user_id
        })

        return http_202_accepted(TaskIDSchema)(payload=TaskIDSchema(
            task_id=message.command_id)
        ).json_response

    except Exception as e:
        logger.error(f"Route /stop error: {e}")
        raise http_500_internal_server_error()(detail=f"Route /stop error: {e}")
