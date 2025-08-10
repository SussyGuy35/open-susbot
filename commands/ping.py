import discord
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh


loca_sheet = "loca/loca - ping.csv"

cmd_names = ["ping", "pong"]

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="ping",
        command_type=sh.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.CORE
)


def command_response(bot: discord.Client):
    return get_string_by_id(loca_sheet, "ping").format(round(bot.latency * 1000))


async def command_listener(message: discord.Message, bot: discord.Client):
    await message.channel.send(command_response(bot))


async def slash_command_listener(ctx: discord.Interaction, client: discord.Client):
    print(f"{ctx.user} used ping commands!")
    await ctx.response.send_message(command_response(client))
