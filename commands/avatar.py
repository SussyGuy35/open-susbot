import discord
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh


loca_sheet = "loca/loca - avatar.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="avatar",
        command_type=sh.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="user",
                description=get_string_by_id(loca_sheet, "command_param_user_desc"),
                required=True
            ),
            sh.CommandParameterDescription(
                name="server_avatar",
                description=get_string_by_id(loca_sheet, "command_param_server_avatar_desc"),
                required=False
            )
        ]
    ),
    sh.HelpSection.GENERAL
)

async def slash_command_listener(ctx: discord.Interaction, user: discord.User, server_avatar: bool = True):
    print(f"{ctx.user} used avatar commands!")
    await ctx.response.defer() 
    avatar = user.display_avatar if server_avatar else user.avatar
    if avatar is not None:
        embed = discord.Embed(
            title=get_string_by_id(loca_sheet, "avatar_embed_title"),
            description=get_string_by_id(loca_sheet, "avatar_embed_desc").format(user),
            color=0x03e3fc,
            type="image"
        )
        embed.set_image(url=avatar.url)
        await ctx.followup.send(embed=embed)
    else:
        await ctx.followup.send(get_string_by_id(loca_sheet, "avatar_noavatar"))
