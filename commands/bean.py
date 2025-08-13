import discord
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh

loca_sheet = "loca/loca - bean.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="bean",
        command_type=sh.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "embed_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="user",
                description=get_string_by_id(loca_sheet, "command_param_user_desc"),
                required=True
            ),
            sh.CommandParameterDescription(
                name="reason",
                description=get_string_by_id(loca_sheet, "command_param_reason_desc"),
                required=True
            )
        ]
    ),
    sh.HelpSection.FUN
)


async def slash_command_listener(ctx: discord.Interaction, user: discord.User, reason: str):
    print(f"{ctx.user} used bean commands!")
    await ctx.response.defer()
    await ctx.followup.send(get_string_by_id(loca_sheet, "bean").format(user, reason))
