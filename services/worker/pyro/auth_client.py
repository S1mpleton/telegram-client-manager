from pyro.auth_base import AuthBase, AuthMethod, AuthCredentials


class BotAuth(AuthBase):
    def __init__(self):
        super().__init__()

    def get_auth_method(self) -> AuthMethod:
        return AuthMethod.BOT

    async def sign_in(self) -> str:
        if not self._credentials or not self._credentials.bot_token:
            raise ValueError("Bot token not set")

        async with self:
            await self.client.app.sign_in_bot(self._credentials.bot_token)
            await self._update_auth_data()

        return self.get_session_string()


class UserAuth(AuthBase):
    def __init__(self):
        super().__init__()
        self._verification_handler = None

    def get_auth_method(self) -> AuthMethod:
        return AuthMethod.USER

    def set_verification_handler(self, handler):
        self._verification_handler = handler

    async def send_code(self) -> str:
        if not self._credentials or not self._credentials.phone_number:
            raise ValueError("Phone number not set")

        await self.connect()

        try:
            sent_code = await self.client.app.send_code(self._credentials.phone_number)
            self._state.phone_code_hash = sent_code.phone_code_hash
            print(f"Code sent to {self._credentials.phone_number}")
            return sent_code.phone_code_hash
        except Exception as e:
            await self.disconnect()
            raise e

    async def verify_code(self, code: str) -> str:
        if not self._state.phone_code_hash:
            raise ValueError("No active code request. Call send_code() first.")

        try:
            await self.client.app.sign_in(
                self._credentials.phone_number,
                self._state.phone_code_hash,
                code
            )
            await self._update_auth_data()

            return self.get_session_string()
        except Exception as e:
            raise e
        finally:
            await self.disconnect()

    async def sign_in_with_handler(self) -> str:
        if not self._verification_handler:
            raise ValueError("Verification handler not set")

        await self.send_code()
        code = await self._verification_handler()
        return await self.verify_code(code)


class AuthFactory:
    @staticmethod
    def create_bot_auth(
            name: str,
            api_id: int,
            api_hash: str,
            bot_token: str
    ) -> BotAuth:
        credentials = AuthCredentials(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token
        )
        auth = BotAuth()
        auth.set_credentials(credentials)
        return auth

    @staticmethod
    def create_user_auth(
            name: str,
            api_id: int,
            api_hash: str,
            phone_number: str
    ) -> UserAuth:
        credentials = AuthCredentials(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number
        )
        auth = UserAuth()
        auth.set_credentials(credentials)
        return auth
