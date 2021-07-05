import os
import sys
import time
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger

import heroku3
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession

from .Config import Config

StartTime = time.time()
catversion = "1.0.0"

if Config.STRING_SESSION:
    session_name = str(Config.STRING_SESSION)
    if session_name.endswith("="):
        bot = TelegramClient(
            StringSession(session_name), Config.APP_ID, Config.API_HASH
        )
    else:
        bot = TelegramClient(
            "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
        ).start(bot_token=Config.STRING_SESSION)
else:
    session_name = "startup"
    bot = TelegramClient(session_name, Config.APP_ID, Config.API_HASH)


DER_ID = ["1614229158", "1380685409"]

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
    )
LOGS = getLogger(__name__)

try:
    if Config.API_KEY is not None or Config.NAMA_APP is not None:
        NAMA_APP = heroku3.from_key(Config.API_KEY).apps()[
            Config.NAMA_APP
        ]
    else:
        NAMA_APP = None
except Exception:
    NAMA_APP = None

# Global Configiables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}
