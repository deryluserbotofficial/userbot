import time
from platform import python_version

from telethon import version

from . import ALIVE_NAME, StartTime, catversion, get_readable_time, mention, reply_id

DEFAULTUSER = ALIVE_NAME or "Deryl"
DER_IMG = Config.FOTO
CUSTOM_ALIVE_TEXT = Config.STATUS_KUSTOM or "✮ HAI, BOTKU BERJALAN DENGAN BAIK ✮"
DERT = Config.STATUS_KUSTOM or "  💎 "


@bot.on(admin_cmd(outgoing=True, pattern="cek$"))
@bot.on(sudo_cmd(pattern="cek$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if DER_IMG:
        deryl = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        deryl += f"**{DERT} Database :** `{check_sgnirts}`\n"
        deryl += f"**{DERT} Versi telethon :** `{version.__version__}\n`"
        deryl += f"**{DERT} Versi bot :** `{catversion}`\n"
        deryl += f"**{DERT} Versi python :** `{python_version()}\n`"
        deryl += f"**{DERT} Ping :** `{uptime}\n`"
        deryl += f"**{DERT} Bos:** {mention}\n\n\n"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=deryl, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await edit_or_reply(
            alive,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{DERT} Database :** `{check_sgnirts}`\n"
            f"**{DERT} Versi telethon :** `{version.__version__}\n`"
            f"**{DERT} Versi bot :** `{catversion}`\n"
            f"**{DERT} Versi python :** `{python_version()}\n`"
            f"**{DERT} Ping :** `{uptime}\n`"
            f"**{DERT} Bos:** {mention}\n",
        )


@bot.on(admin_cmd(outgoing=True, pattern="cekbot$"))
@bot.on(sudo_cmd(pattern="cekbot$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    tgbotusername = Config.BOT_USERNAME
    reply_to_id = await reply_id(alive)
    cat_caption = f"**Bot sedang berjalan**\n"
    cat_caption += f"**  -Telethon versi :** `{version.__version__}\n`"
    cat_caption += f"**  -Versi bot :** `{catversion}`\n"
    cat_caption += f"**  -Python Versi :** `{python_version()}\n`"
    cat_caption += f"**  -Bos:** {mention}\n"
    results = await bot.inline_query(tgbotusername, cat_caption)  # pylint:disable=E0602
    await results[0].click(alive.chat_id, reply_to=reply_to_id, hide_via=True)
    await alive.delete()




def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "No Database is set"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "Berfungsi dengan baik"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update(
    {
        "status": "**Fungsi :** `cek`\
      \n\n  •  **Penulisan : **`.cek` \
      \n  •  **Fungsi : **__cek status userbot__\
      \n\n  •  **Penulisan : **`.cekbot` \
      \n  •  **Fungsi : **__Cek status inlinebot mu.__\
      \nTambahkan variable `FOTO` untuk media cekmu"\
    }
)
