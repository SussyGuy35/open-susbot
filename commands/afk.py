import discord
import lib.locareader
import features.afk_notificer as afk_notificer
from features.afk_notificer import afk_nickname
import lib.sussyhelper as sh


cmd_names = ["afk"]
loca_sheet = f"loca/loca - {cmd_names[0]}.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.HYBRID,
        description=lib.locareader.get_string_by_id(loca_sheet, "command_desc"),
        usage=lib.locareader.get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="status",
                description=lib.locareader.get_string_by_id(loca_sheet, "command_param_status_desc"),
                required=False
            )
        ]
    ),
    sh.HelpSection.GENERAL
)


async def command_listener(message: discord.Message, user: discord.Member | discord.User, status: str | None = None):
    if not message.guild or not isinstance(user, discord.Member):
        await message.channel.send("This command can only be used in a server.")
        return
    
    status = status or "AFK"
    u = user.display_name
    try:
        new_nick = afk_nickname(user.display_name, status)
        if new_nick != user.display_name:
            await user.edit(nick=new_nick)
    except discord.Forbidden:
        pass
    afk_notificer.set_afk_status(str(user.id), status, u, message.guild.id)


    response = lib.locareader.get_string_by_id(loca_sheet, "afk_set").format(status)
    await message.reply(response, mention_author=False)

async def slash_command_listener(ctx: discord.Interaction, status: str | None = None):
    print(f"{ctx.user} used {cmd_names[0]} commands!")
    await ctx.response.defer()

    status = status or "AFK"

    if ctx.guild is None:
        await ctx.followup.send("This command can only be used in a server.")
        return
    
    member = ctx.guild.get_member(ctx.user.id)
    if member is None:
        return

    u = member.display_name

    try:
        new_nick = afk_nickname(member.display_name, status)
        if new_nick != member.display_name:
            await member.edit(nick=new_nick)
    except discord.Forbidden:
        pass

    afk_notificer.set_afk_status(str(ctx.user.id), status, u, ctx.guild.id)

    response = lib.locareader.get_string_by_id(loca_sheet, "afk_set").format(status)
    await ctx.followup.send(response)