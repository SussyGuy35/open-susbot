import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix


loca_sheet = "loca/loca - getprefix.csv"


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used get prefix commands")
    response = get_string_by_id(loca_sheet, "prompt").format(get_prefix(ctx.guild))
    await ctx.response.defer()
    await ctx.followup.send(response)
