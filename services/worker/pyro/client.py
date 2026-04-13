from typing import Optional

from pyrogram import Client


class TelegramClient:
    def __init__(
            self,
            name: str,
            api_id: int = None,
            api_hash: str = None,
            phone_number: str = None,
            phone_code: str = None,
            session_string: str = None,
            bot_token: str = None,
            in_memory: bool = True
    ):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.session_string = session_string
        self.bot_token = bot_token
        self.in_memory = in_memory

        self._app: Optional[Client] = None

    @property
    def app(self) -> Client:
        if self._app is None:
            self._app = Client(
                self.name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number,
                phone_code=self.phone_code,
                session_string=self.session_string,
                bot_token=self.bot_token,
                in_memory=self.in_memory
            )
        return self._app

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def start(self):
        try:
            await self.app.start()
        except Exception as e:
            print(f"Failed to start client {self.name}: {e}")
            raise

    async def stop(self):
        try:
            if self._app and self._app.is_connected:
                await self.app.stop()
        except Exception as e:
            print(f"Failed to stop client {self.name}: {e}")
            raise

    async def connect(self):
        try:
            await self.app.connect()
        except Exception as e:
            print(f"Failed to connect client {self.name}: {e}")
            raise

    async def disconnect(self):
        try:
            if self._app and self._app.is_connected:
                await self.app.disconnect()

        except Exception as e:
            print(f"Failed to disconnect client {self.name}: {e}")
            raise

    def is_connected(self) -> bool:
        return self._app is not None and self._app.is_connected

