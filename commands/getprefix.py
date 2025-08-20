import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix
import lib.sussyhelper as ssyhelper


loca_sheet = "loca/loca - getprefix.csv"

ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelp(
        command_name="get_prefix",
        command_type=ssyhelper.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
    ),
    ssyhelper.HelpSection.CORE
)


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used get prefix commands")
    response = get_string_by_id(loca_sheet, "prompt").format(get_prefix(ctx.guild))
    await ctx.response.defer()
    await ctx.followup.send(response)
