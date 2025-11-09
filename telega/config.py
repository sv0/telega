import os

from dotenv import load_dotenv


class Config:

    telegram_api_id = None
    telegram_api_hash = None
    telegram_api_phone_number = None

    telegram_session_dc_id = None
    telegram_session_server_address = None
    telegram_session_port = 443
    telegram_session_auth_key = ''

    def __init__(self):
        load_dotenv()

        self.telegram_api_id = os.getenv('TELEGRAM_API_ID')
        self.telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
        self.telegram_api_phone_number = os.getenv('TELEGRAM_API_PHONE_NUMBER')
        self.telegram_session_dc_id = os.getenv('TELEGRAM_SESSION_DC_ID')
        self.telegram_session_server_address = os.getenv('TELEGRAM_SESSION_SERVER_ADDRESS')
        self.telegram_session_port = os.getenv('TELEGRAM_SESSION_PORT', 443)
        self.telegram_session_auth_key = os.getenv('TELEGRAM_SESSION_AUTH_KEY')
