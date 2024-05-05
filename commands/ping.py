try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - ping.csv"


def command_response(bot: discord.Client):
    return get_string_by_id(loca_sheet, "ping", config.language).format(round(bot.latency * 1000))


async def command_listener(message: discord.Message, bot: discord.Client):
    await message.channel.send(command_response(bot))


async def slash_command_listener(ctx: discord.Interaction, client: discord.Client):
    print(f"{ctx.user} used ping commands!")
    await ctx.response.send_message(command_response(client))
