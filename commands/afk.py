import discord
import lib.locareader
import features.afk_notificer as afk_notificer

cmd_names = ["afk"]
loca_sheet = f"loca/loca - {cmd_names[0]}.csv"


async def command_listener(message: discord.Message, user: discord.Member | discord.User, status: str | None = None):
    if message.guild is None or not isinstance(user, discord.Member):
        await message.channel.send("This command can only be used in a server.")
        return
    
    status = status or "AFK"

    if len(f"[{status}] {user.display_name}") < 32:
        await user.edit(nick=f"[{status}] {user.display_name}")
    elif len(f"[AFK] {user.display_name}") < 32:
        await user.edit(nick=f"[AFK] {user.display_name}")
    afk_notificer.set_afk_status(str(user.id), status)


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

    await member.edit(nick=f"[{status}] {ctx.user.display_name}")

    afk_notificer.set_afk_status(str(ctx.user.id), status)

    response = lib.locareader.get_string_by_id(loca_sheet, "afk_set").format(status)
    await ctx.followup.send(response)