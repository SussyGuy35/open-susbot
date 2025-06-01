import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - bean.csv"


async def slash_command_listener(ctx: discord.Interaction, user: discord.User, reason: str):
    print(f"{ctx.user} used bean commands!")
    await ctx.response.defer()
    await ctx.followup.send(get_string_by_id(loca_sheet, "bean").format(user, reason))
