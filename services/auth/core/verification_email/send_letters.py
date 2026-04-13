# email_service.py
import logging
import smtplib
from typing import Union, Optional

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import pystache
from pydantic import EmailStr
from core.config import (
    BASE_URL,
    SETTINGS,
    BASE_PATH
)

letters_path = (
    BASE_PATH
    .joinpath("core")
    .joinpath("verification_email")
    .joinpath("letters")
)


async def send_verification_email_code(email: Union[EmailStr | str], verify_code: str) -> bool:
    template_data = {
        "app_name": "StepFatherBot",
        "code": verify_code,
        "expires_in_minutes": 60,
    }

    with open(letters_path.joinpath("email_verify.html"), 'r', encoding='utf-8') as file:
        template = file.read()

    content = pystache.render(template, template_data)

    message = MIMEMultipart()
    message["From"] = SETTINGS.email.SMTP_FROM_EMAIL
    message["To"] = str(email)
    message["Subject"] = "Verify email"

    message.attach(MIMEText(content, "html"))

    return await _send_email(message)


async def send_email_update_confirmation(
        old_email: Union[EmailStr, str],
        new_email: Union[EmailStr, str],
        token: str
):
    template_data = {
        "app_name": "StepFatherBot",
        "old_email": old_email,
        "new_email": new_email,
        "token": token,
        "confirmation_link": f"http://{BASE_URL}/api/v1/confirmEmailUpdate?token={token}",
        "expires_in_minutes": 60,
    }

    with open(letters_path.joinpath("email_update_confirmation.html"), 'r', encoding='utf-8') as file:
        template = file.read()

    content = pystache.render(template, template_data)

    message = MIMEMultipart()
    message["From"] = SETTINGS.email.SMTP_FROM_EMAIL
    message["To"] = old_email
    message["Subject"] = "Confirming email change"

    message.attach(MIMEText(content, "html"))

    return await _send_email(message)


async def _send_email(message: MIMEMultipart) -> bool:
    try:
        await aiosmtplib.send(
            message,
            hostname=SETTINGS.email.SMTP_HOST,
            port=SETTINGS.email.SMTP_PORT,
            username=SETTINGS.email.SMTP_USERNAME,
            password=SETTINGS.email.SMTP_PASSWORD,
            use_tls=True
        )
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
