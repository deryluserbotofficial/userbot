# corona virus stats for catuserbot
from covid import Covid

from . import covidindia


@bot.on(admin_cmd(pattern="covid(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="covid(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = (event.pattern_match.group(1)).title()
    else:
        country = "World"
    catevent = await edit_or_reply(event, "`Menghubungkan ke server WHO...`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⚠️ Terkonfirmasi   : <code>{hmm1}</code>"
        data += f"\n😔 Aktif           : <code>{country_data['active']}</code>"
        data += f"\n⚰️ Meninggal         : <code>{hmm2}</code>"
        data += f"\n🤕 Kritis          : <code>{country_data['critical']}</code>"
        data += f"\n😊 Sembuh   : <code>{country_data['recovered']}</code>"
        data += f"\n💉 Total tes    : <code>{country_data['total_tests']}</code>"
        data += f"\n🥺 Kasus baru   : <code>{country_data['new_cases']}</code>"
        data += f"\n😟 Kematian baru : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>Corona Virus Info of {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            der1 = int(data["new_positive"]) - int(data["positive"])
            der2 = int(data["new_death"]) - int(data["death"])
            der3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\n⚠️ Terkonfirmasi   : <code>{data['new_positive']}</code>\
                \n😔 Aktif           : <code>{data['new_active']}</code>\
                \n⚰️ Kematian         : <code>{data['new_death']}</code>\
                \n😊 Sembuh   : <code>{data['new_cured']}</code>\
                \n🥺 Kasus baru   : <code>{der1}</code>\
                \n😟 Kematian baru : <code>{der2}</code>\
                \n😃 Kesembuhan baru  : <code>{der3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "`Corona Virus Info of {} is not avaiable or unable to fetch`".format(
                    country
                ),
                5,
            )


CMD_HELP.update(
    {
        "covid": "**Fungsi : **`covid`\
        \n\n  •  **Penulisan : **`.covid <negara>`\
        \n  •  **Fungsi :** __Informasi covid sebuah negara.__\
        \n\n  •  **Penulisan : **`.covid <nama daerah>`\
        \n  •  **Fungsi :** __Khusus india.__\
        "
    }
)
