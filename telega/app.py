#!/usr/bin/env python3
"""
Web API to check if phone number is connected to Telegram account.
"""
import logging
import json

import falcon.asgi
from telethon.sync import TelegramClient
from telethon.sessions import SQLiteSession

from .config import Config
from .utils import get_user_by_phone

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


async def login(
    api_id: str,
    api_hash: str,
    phone_number: str,
    interactive: bool = False
) -> TelegramClient:
    """Create a telethon session or reuse existing one.
    """
    client = TelegramClient(phone_number, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        logger.info("Not authorized")
        return
    return client


class HomeResource:

    async def on_get(self, req, resp):
        """Home page"""
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = (
            '\nSup. Wanna search some shit on Telegram?\n'
            'You are on the right way. It is telega API home page.\n\n'
            'Usage examples:\n'
            '\n'
            f'curl http://{req.netloc}/search/420720100500\n\n'
        )


class SearchTelegramPhoneNumber:
    """Search phone number on Telegram"""

    def __init__(self, config):
        self.config = config

    async def on_get(self, req, resp, phone):
        result = await self.find(phone)
        logger.debug(result)
        resp.set_header('Access-Control-Allow-Origin', '*')
        if result.get('error'):
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
        resp.text = json.dumps(result)

    async def find(self, query: str):
        """Look for phone number"""
        try:
            client = await login(
                self.config.telegram_api_id,
                self.config.telegram_api_hash,
                self.config.telegram_api_phone_number,
            )
            result = await get_user_by_phone(client, query)
            await client.disconnect()
            return result
        except Exception as err:
            return {'error': str(err)}


def create_app(config=None):
    config = config or Config()

    # create session
    session = SQLiteSession(config.telegram_api_phone_number)

    app = falcon.asgi.App()
    app.add_route('/', HomeResource())
    app.add_route('/search/{phone}', SearchTelegramPhoneNumber(config))

    return app


app = create_app()
