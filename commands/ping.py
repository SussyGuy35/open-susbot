try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - ping.csv"

def command_response():
    return get_string_by_id(loca_sheet,"ping",config.language)

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used ping commands!")
    await ctx.response.send_message(command_response())