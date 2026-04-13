import logging
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends
from shared_http.responses import (
    http_200_ok,
    http_409_conflict,
    http_500_internal_server_error,
    http_401_unauthorized, http_404_not_found,
)

from core.jwt_token.config import ACCESS_TOKEN_TYPE
from core.verification_email.send_letters import send_verification_email_code

from core.jwt_token.validate import ValidateToken, http_bearer
from infrastructure.database import UserOutSchema
from infrastructure.storage.repositories import pyload_repository

router = APIRouter()


@router.get(
    "/sendCodeForVerifyEmail",
    dependencies=[Depends(http_bearer)],
    responses={
        200: {
            "model": http_200_ok().model
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
async def send_code_for_verify_email(
        auth_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=ACCESS_TOKEN_TYPE))]
):
    if auth_out_schema.is_email_verified:
        raise http_409_conflict()(message="This email has already been confirmed")

    try:
        verification_code = f"{secrets.randbelow(100000):05d}"
        await pyload_repository.set_payload(
            str(auth_out_schema.id),
            {
                "verification_code": verification_code,
                "email": auth_out_schema.email
            },
            prefix="email-verify",
            ttl=1 * 60
        )

        email_sent = await send_verification_email_code(
            auth_out_schema.email,
            verification_code
        )

        if not email_sent:
            logging.warning(f"Failed to send verification email to {auth_out_schema.email}")
            return http_500_internal_server_error()(message="Send confirmation code fatal").json_response

        return http_200_ok()(message="The confirmation code has been sent").json_response

    except Exception as e:
        logging.error(f"Send confirmation code error: {e}")
        raise http_500_internal_server_error()(message="Send confirmation code fatal")


@router.get(
    "/resendCodeForVerifyEmail",
    dependencies=[Depends(http_bearer)],
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
        500: {
            "model": http_500_internal_server_error().model
        }
    }
)
async def resend_code_for_verify_email(
        auth_out_schema: Annotated[UserOutSchema, Depends(ValidateToken(token_type=ACCESS_TOKEN_TYPE))]
):
    try:

        send_code_data = await pyload_repository.get_payload(
            name=str(auth_out_schema.id),
            prefix="email-verify",
        )

        if not send_code_data:
            return http_404_not_found()(message="The code has never been sent yet").json_response

        if auth_out_schema.is_email_verified:
            if send_code_data.get("email") == auth_out_schema.email:
                return http_409_conflict()(message="This email has already been confirmed").json_response

        email_sent = await send_verification_email_code(
            send_code_data.get("email"),
            send_code_data.get("verification_code")
        )

        if not email_sent:
            logging.warning(f"Failed to send verification email to {auth_out_schema.email}")
            return http_500_internal_server_error()(message="Resend confirmation code fatal").json_response

        return http_200_ok()(message="The verification code has been sent again").json_response

    except Exception as e:
        logging.error(f"Resend confirmation code error: {e}")
        raise http_500_internal_server_error()(detail="Resend confirmation code fatal")
