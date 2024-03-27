try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - getprefix.csv"

def get_prefix(guild: discord.Guild | None):
    if guild == None: return config.prefix
    if guild.id in config.specific_prefix.keys():
        return config.specific_prefix[guild.id]
    return config.prefix

def slash_command_listener(ctx: discord.Interaction):
    return get_string_by_id(loca_sheet, "prompt", config.language).format(get_prefix(ctx.guild))