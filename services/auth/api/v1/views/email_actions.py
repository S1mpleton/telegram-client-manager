import logging
import secrets
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from shared_http.responses import (
    http_200_ok,
    http_500_internal_server_error,
    http_401_unauthorized,
    http_202_accepted, http_404_not_found, http_400_bad_request, http_409_conflict,
)

from api.v1.schemas import RequestUpdateEmailSchema, RequestVerifyEmailSchema
from core.config import BASE_URL
from core.jwt_token.config import EMAIL_UPDATE_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from core.jwt_token.utils import create_jwt
from core.verification_email.send_letters import (
    send_email_update_confirmation,
    send_verification_email_code
)
from core.jwt_token.validate import ValidateToken, http_bearer, ValidateQueryToken
from infrastructure.broker.fs_broker import email_update
from infrastructure.broker.schemas.user import EmailUpdateSchema
from infrastructure.database import UserOutSchema, CRUD, UserUpdateSchema
from infrastructure.storage.repositories import pyload_repository

router = APIRouter()


@router.post(
    "/changeEmail",
    dependencies=[Depends(http_bearer)],
    responses={
        200: {
            "model": http_200_ok().model
        },
        202: {
            "model": http_202_accepted().model
        },
        401: {
            "model": http_401_unauthorized().model
        },
        409: {
            "model": http_409_conflict().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def email_change(
        auth_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=ACCESS_TOKEN_TYPE))],
        update_email_schema: Annotated[RequestUpdateEmailSchema, Body(...)],
):
    if await CRUD.check_user_exist_by_email(update_email_schema.email):
        raise http_409_conflict()(message=f"Email {update_email_schema.email} already exist")

    if not auth_out_schema.is_email_verified:
        await CRUD.update_user_by_email(auth_out_schema.email, UserUpdateSchema(email=update_email_schema.email))

        await email_update.publish(
            message=EmailUpdateSchema(
                auth_id=auth_out_schema.id,
                old_email=auth_out_schema.email,
                new_email=update_email_schema.email
            )
        )

        raise http_200_ok()(
            message=f"Email has been changed to {update_email_schema.email}",
            detail=f"Your previous email wasn't verified, so hackers could exploit this and change your email. "
                   f"Don't forget to verify your new email."
        )

    try:
        await pyload_repository.set_payload(
            str(auth_out_schema.id),
            {
                "email": update_email_schema.email
            },
            prefix="email-update",
            ttl=1 * 60
        )

        confirmation_token = create_jwt(
            token_type=EMAIL_UPDATE_TOKEN_TYPE,
            payload={"sub": str(auth_out_schema.id), },
            expire_timedelta=timedelta(hours=1)
        )

        email_sent = await send_email_update_confirmation(
            old_email=auth_out_schema.email,
            new_email=update_email_schema.email,
            token=confirmation_token
        )

        if not email_sent:
            raise http_500_internal_server_error()(message="Confirmation message was not sent")

        return http_202_accepted()(
            detail="A confirmation email has been sent to your email address."
        ).json_response

    except Exception as e:
        logging.error(f"Email change error: {e}")
        raise http_500_internal_server_error()(message=f"Email change error: {e}")


@router.get(
    "/confirmEmailUpdate",
    # dependencies=[Depends(http_bearer)],
    responses={
        200: {
            "model": http_200_ok().model
        },
        401: {
            "model": http_401_unauthorized().model
        },
        404: {
            "model": http_404_not_found().model
        },
        409: {
            "model": http_409_conflict().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def confirm_email_update(
        auth_out_schema: Annotated[UserOutSchema, Depends(ValidateQueryToken(token_type=EMAIL_UPDATE_TOKEN_TYPE))]
):
    try:
        update_email_data = await pyload_repository.get_payload(auth_out_schema.id, "email-update")

        if not update_email_data:
            return http_404_not_found()(
                message=f"Data not found. Try again"
            ).json_response

        if await CRUD.check_user_exist_by_email(update_email_data.get("email")):
            return http_409_conflict()(
                message=f"Email {update_email_data.get("email")} already exist"
            ).json_response

        await pyload_repository.delete_payload(auth_out_schema.id, "email-update")

        await CRUD.update_user_by_email(
            auth_out_schema.email,
            UserUpdateSchema(
                email=update_email_data.get("email"),
                is_email_verified=False
            )
        )

        await email_update.publish(
            message=EmailUpdateSchema(
                auth_id=auth_out_schema.id,
                old_email=auth_out_schema.email,
                new_email=update_email_data.get("email")
            )
        )

        return http_200_ok()(message="The email has been changed").json_response

    except Exception as e:
        logging.error(f"Email verification error: {e}")
        raise http_500_internal_server_error()(detail="Verification failed")


@router.post(
    "/verifyEmail",
    dependencies=[Depends(http_bearer)],
    responses={
        200: {
            "model": http_200_ok().model
        },
        400: {
            "model": http_400_bad_request().model
        },
        401: {
            "model": http_401_unauthorized().model
        },
        404: {
            "model": http_404_not_found().model
        },
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def verify_email(
        auth_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=ACCESS_TOKEN_TYPE))],
        verify_email_schema: Annotated[RequestVerifyEmailSchema, Body(...)]
):
    try:
        verify_email_data = await pyload_repository.get_payload(auth_out_schema.id, "email-verify")

        print("verify_email_data", verify_email_data)

        if not verify_email_data:
            return http_404_not_found()(
                message=f"First, make a request to {BASE_URL}/api/v1/sendCodeForVerifyEmail"
            ).json_response

        if verify_email_schema.verification_code != verify_email_data.get("verification_code"):
            return http_400_bad_request()(message="Invalid verification code").json_response

        await CRUD.update_user_by_email(auth_out_schema.email, UserUpdateSchema(is_email_verified=True))
        await pyload_repository.delete_payload(auth_out_schema.id, "email-verify")

        return http_200_ok()(message="Email confirmed").json_response

    except Exception as e:
        logging.error(f"Email verification error: {e}")
        raise http_500_internal_server_error()(detail="Verification failed")
