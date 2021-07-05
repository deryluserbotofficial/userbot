import glob
from pathlib import Path
from sys import argv

import telethon.utils
from telethon import TelegramClient

from . import LOGS, bot
from .Config import Config
from .utils import load_module


async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)


if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Config.BOT_TOKEN is not None:
        LOGS.info("Menginstall inlinebot sistem")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
        ).start(bot_token=Config.BOT_TOKEN)
        LOGS.info("Selesai dengan sempurna")
        LOGS.info("Memulai userbot")
        bot.loop.run_until_complete(add_bot(Config.BOT_TOKEN))
        LOGS.info("Startup Completed")
    else:
        bot.start()

path = "derylbot/fungsi/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        if shortname.replace(".py", "") not in Config.NO_LOAD:
            load_module(shortname.replace(".py", ""))

LOGS.info("Yay sudah aktif.!!!")
LOGS.info(
    "Sekarang ketik .aktif untuk memastikan userbot hidup\
    \nBantuan di https://t.me/deryluserbotsupport ( slow respone )"
)


async def startupmessage():
    try:
        if Config.LOG_GROUP:
            await bot.send_message(
                Config.LOG_GROUP,
                "**Sekarang ketik .aktif untuk memastikan userbot hidup\
    \nBantuan di https://t.me/derylitteam ( slow respone )",
                link_preview=False,
            )
    except Exception as e:
        LOGS.info(str(e))


bot.loop.create_task(startupmessage())

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()
