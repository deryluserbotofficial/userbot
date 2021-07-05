import telethon.password as pwd_mod

# https://t.me/TelethonChat/140200
from telethon.tl import functions


@bot.on(admin_cmd(pattern="transfer (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_name = event.pattern_match.group(1)
    current_channel = event.chat_id
    # not doing any validations, here FN
    # MBL
    try:
        pwd = await event.client(functions.account.GetPasswordRequest())
        my_srp_password = pwd_mod.compute_check(pwd, Config.VERIF2LANGKAH)
        await event.client(
            functions.channels.EditCreatorRequest(
                channel=current_channel, user_id=user_name, password=my_srp_password
            )
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        await event.edit("Berhasil 🌚")


CMD_HELP.update(
    {
        "kirim_channel": "**Fungsi :** `kirim_channel`\
        \n**Penulisan : **`.transfer username penerima]`\
        \n**Fungsi: **Transfer channel, jika anda memiliki verifikasi 2 langkah silahkan menonton video tutorialnya dulu. \
        "
    }
)
