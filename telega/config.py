import os

from dotenv import load_dotenv


class Config:

    telegram_api_id = None
    telegram_api_hash = None
    telegram_api_phone_number = None

    def __init__(self):
        load_dotenv()

        self.telegram_api_id = os.getenv('TELEGRAM_API_ID')
        self.telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
        self.telegram_api_phone_number = os.getenv('TELEGRAM_API_PHONE_NUMBER')
