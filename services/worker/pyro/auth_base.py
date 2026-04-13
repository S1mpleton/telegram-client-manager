import re
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from pyro.client import TelegramClient


class AuthMethod(Enum):
    BOT = "bot"
    USER = "user"


@dataclass
class AuthCredentials:
    name: str
    api_id: int
    api_hash: str
    bot_token: Optional[str] = None
    phone_number: Optional[str] = None

    def validate(self):
        """Validation of input fields"""

        if not re.match(r'^[а-яА-Яa-zA-Z0-9_]{1,16}$', self.name):
            raise ValueError("Name must contain only letters/numbers and be 1-16 chars")

        if not re.match(r'^[0-9]{4,9}$', str(self.api_id)):
            raise ValueError("api_id must consist of 4-9 numbers")

        if not re.match(r"^[0-9a-fA-F]{32}$", self.api_hash):
            raise ValueError("Invalid api_hash format")

        if self.bot_token:
            if not re.match(r'^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$', self.bot_token):
                raise ValueError("Invalid bot token format")
        elif self.phone_number:
            if not re.match(r'^\+\d{1,15}$', self.phone_number.replace(" ", "")):
                raise ValueError("Invalid phone number format")
        else:
            raise ValueError("Either bot_token or phone_number must be provided")


class AuthState:
    def __init__(self):
        self.phone_code_hash: Optional[str] = None
        self.session_string: Optional[str] = None
        self.user_id: Optional[int] = None

    def clear(self):
        self.phone_code_hash = None
        self.session_string = None
        self.user_id = None


class AuthBase(ABC):
    def __init__(self):
        self._credentials: Optional[AuthCredentials] = None
        self._state = AuthState()
        self._client: Optional[TelegramClient] = None
        self._is_connected = False

    @property
    def client(self) -> Optional[TelegramClient]:
        if self._client is None and self._credentials:
            client_kwargs = {
                "name": self._credentials.name,
                "api_id": self._credentials.api_id,
                "api_hash": self._credentials.api_hash,
            }

            if self._credentials.bot_token:
                client_kwargs["bot_token"] = self._credentials.bot_token
            elif self._credentials.phone_number:
                client_kwargs["phone_number"] = self._credentials.phone_number

            self._client = TelegramClient(**client_kwargs)

        return self._client

    @abstractmethod
    def get_auth_method(self) -> AuthMethod:
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        if not self._client:
            raise ValueError("Client not initialized. Call set_credentials() first.")

        if not self._is_connected:
            await self.client.connect()
            self._is_connected = True
            print(f"Connected as {self.get_auth_method().value}")

    async def disconnect(self):
        if self._is_connected and self._client:
            await self.client.disconnect()
            self._is_connected = False
            print("Disconnected")

    def set_credentials(self, credentials: AuthCredentials):
        credentials.validate()
        self._credentials = credentials
        self._client = None

    async def _update_auth_data(self):
        try:
            me = await self.client.app.get_me()
            self._state.user_id = me.id
            self._state.session_string = await self.client.app.export_session_string()
        except Exception as e:
            print(f"Failed to update auth data: {e}")
            raise

    def get_session_string(self) -> Optional[str]:
        return self._state.session_string

    def get_user_id(self) -> Optional[int]:
        return self._state.user_id

    def clear_state(self):
        self._state.clear()
