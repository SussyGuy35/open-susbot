try:
    import config_override as config
except:
    import config
import discord
from lib.sussyutils import get_prefix
from lib.locareader import get_string_list

loca_sheet = "loca/loca - help.csv"

def get_help_text(prefix):
    help_text = ""
    for line in get_string_list(loca_sheet, config.language):
        help_text += line + "\n"
    return help_text.format(prefix)

def command_response(prefix):
    return get_help_text(prefix)

async def command_listener(message: discord.Message):
    prefix = get_prefix(message.guild)
    await message.channel.send(get_help_text(prefix))

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used help commands!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.send_message(command_response(prefix))