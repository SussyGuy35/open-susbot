import discord
from lib.sussyutils import get_json_async
import lib.sussyhelper as sh
import lib.locareader as loca_reader

loca_sheet = "loca/loca - randcat.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="randcat",
        command_type=sh.CommandType.SLASH,
        description=loca_reader.get_string_by_id(loca_sheet, "command_desc"),
        usage=loca_reader.get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="is_cat_girl",
                description=loca_reader.get_string_by_id(loca_sheet, "command_param_is_cat_girl_desc"),
                required=False
            )
        ]
    ),
    sh.HelpSection.FUN
)

async def command_response(is_cat_girl):
    if is_cat_girl:
        resp = await get_json_async("https://nekos.life/api/v2/img/neko")
        return resp["url"]
    else:
        resp = await get_json_async("https://api.thecatapi.com/v1/images/search")
        return resp[0]["url"]


async def slash_command_listener(ctx: discord.Interaction, is_cat_girl: bool):
    print(f"{ctx.user} used randcat commands!")
    await ctx.response.defer()
    resp = await command_response(is_cat_girl)
    await ctx.followup.send(resp)
