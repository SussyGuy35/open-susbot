import discord
from lib.sussyutils import get_json_async
import lib.sussyhelper as sh

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="momjoke",
        command_type=sh.CommandType.SLASH,
        description="Yo mama jokes ",
        usage="Yo mama jokes",
    ),
    sh.HelpSection.FUN
)


async def command_response():
    resp = await get_json_async("https://www.yomama-jokes.com/api/v1/jokes/random/")
    return resp["joke"]


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used momjoke commands!")
    await ctx.response.defer()
    resp = await command_response()
    await ctx.followup.send(resp)
