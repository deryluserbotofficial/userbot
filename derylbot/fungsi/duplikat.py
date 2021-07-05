import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from . import ALIVE_NAME, AUTONAME, DEFAULT_BIO

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO)
    if DEFAULT_BIO
    else "DERYL BOSK˙"
)
if Config.LOG_GROUP is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.LOG_GROUP


@bot.on(admin_cmd(pattern="duplikat ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(
        user_id, Config.FOLDER_DOWNLOAD
    )
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await event.client.upload_file(profile_pic)
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await event.delete()
    await event.client.send_message(
        event.chat_id, "**BERHASIL JADI 1**", reply_to=reply_message
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#BERHASIL\nBERHASIL MEENDUPLIKAT [{first_name}](tg://user?id={user_id })",
        )


@bot.on(admin_cmd(pattern="kembali$"))
async def _(event):
    if event.fwd_from:
        return
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    n = 1
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=n)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await event.edit("selamat datang info lama!")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"#BERHASIL\nBerhasil mengembalikan profilmu"
        )


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        return replied_user, None
    input_str = None
    try:
        input_str = event.pattern_match.group(1)
    except IndexError as e:
        return None, e
    if event.message.entities is not None:
        mention_entity = event.message.entities
        probable_user_mention_entity = mention_entity[0]
        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
            user_id = probable_user_mention_entity.user_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        try:
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    try:
        user_object = await event.client.get_entity(int(input_str))
        user_id = user_object.id
        replied_user = await event.client(GetFullUserRequest(user_id))
        return replied_user, None
    except Exception as e:
        return None, e


CMD_HELP.update(
    {
        "duplikat": "**Fungsi : **`Duplikat`\
        \n\n  •  **Penulisam :** `.duplikat`<reply pengguna\
        \n  •  **Fungsi : **Menduplikat profilnya\
        \n\n  •  **Pemulisan : **`.kembali`\
        \n  •  **Function : **Mengembalikan akunmu yang dulu\
    "
    }
)
