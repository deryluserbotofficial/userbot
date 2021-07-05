"""Create Private Groups
Available Commands:
.create (b|g) GroupName"""
from telethon.tl import functions


@bot.on(admin_cmd(pattern="create (sp|gr|ch) (.*)"))  # pylint:disable=E0602
@bot.on(sudo_cmd(pattern="create (sp|gr|ch) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "ch":
        descript = "Ini tes channel yang dibuat dengan deryluserbot"
    else:
        descript = "Ini tes channel yang dibuat dengan deryluserbot"
    event = await edit_or_reply(event, "Membuat......")
    if type_of_group == "sp":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(  # pylint:disable=E0602
                    users=["@sarah_robot"],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            await event.client(
                functions.messages.DeleteChatUserRequest(
                    chat_id=created_chat_id, user_id="@sarah_robot"
                )
            )
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Group `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    elif type_of_group in ["g", "c"]:
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=type_of_group != "ch",
                )
            )

            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "Channel `{}` berhasil dibuat. Link {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
    else:
        await event.edit("Baca `.info buat` untuk mengetahui cara kerjaku")


CMD_HELP.update(
    {
        "buat": "**PENULISAN :** `.buat sp <nama group>`\
    \n**FUNGSI : **Membuat supergroup dan mengirimkan linknya\
    \n\n**PENULISAN : **`.buat gr <nama group>`\
    \n**FUNGSI : **Membuat private group dan mengirimkan linknya\
    \n\n**PENULISAN : **`.buat ch <nama channel>`\
    \n**FUNGSI : **Membuat channel dan mengirimkan linknya\
    \n\nKamu selalu rajanya\
    "
    }
)
