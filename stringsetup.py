from telethon.sessions import StringSession
from telethon.sync import TelegramClient

print(
    """Silahkan pergi ke @derylapibot"""
)
APP_ID = int(input("Masukkan APP_ID: "))
API_HASH = input("Masukkan API_HASH: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(client.session.save())
    client.send_message("me", client.session.save())
