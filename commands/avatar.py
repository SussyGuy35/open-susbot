try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - main.csv"


async def slash_command_listener(ctx: discord.Interaction, user: discord.User, server_avatar: bool = True):
    print(f"{ctx.user} used avatar commands!")
    await ctx.response.defer()
    avatar = user.display_avatar if server_avatar else user.avatar
    if avatar is not None:
        embed = discord.Embed(
            title=get_string_by_id(loca_sheet, "command_avatar_embed_title", config.language),
            description=get_string_by_id(loca_sheet, "command_avatar_embed_desc", config.language).format(user),
            color=0x03e3fc,
            type="image"
        )
        embed.set_image(url=avatar.url)
        await ctx.followup.send(embed=embed)
    else:
        await ctx.followup.send(get_string_by_id(loca_sheet, "command_avatar_noavatar", config.language))
