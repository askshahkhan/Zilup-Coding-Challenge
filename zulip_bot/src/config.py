import os
from dotenv import load_dotenv

load_dotenv()

ZULIP_URL = os.getenv("ZULIP_URL")
ZULIP_EMAIL = os.getenv("ZULIP_EMAIL")
ZULIP_PASSWORD = os.getenv("ZULIP_PASSWORD")
