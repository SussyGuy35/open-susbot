import discord
import lib.locareader

CMD_NAME = "clear"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"

async def slash_command_listener(ctx: discord.Interaction, number: int):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer(ephemeral=True)
    
    if not ctx.user.guild_permissions.manage_messages:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "no_permission"))
        return
    
    if number > 100 or number < 0:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "invalid_number"))
        return
    
    try:
        await ctx.channel.purge(limit=number)

    except discord.Forbidden: # can't delete messages
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "bot_no_permission").format(number))
    
    else:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "success").format(number))