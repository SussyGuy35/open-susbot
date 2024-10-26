import discord
import lib.sussyutils
import lib.locareader
from lib.sussyconfig import get_config
import features.reaction_roles as reaction_roles

config = get_config()

CMD_NAME = "send_reaction_roles_message"
loca_sheet = f"loca/loca - reactionrole.csv"

async def slash_command_listener(
        ctx: discord.Interaction,
        prompt_message: str,
        role1: discord.Role, 
        emoji1: str,
        role2: discord.Role | None,
        emoji2: str | None,
        role3: discord.Role | None,
        emoji3: str | None,
        role4: discord.Role | None,
        emoji4: str | None,
        role5: discord.Role | None,
        emoji5: str | None,
        one_role: bool = False
        ):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer(ephemeral=True)
    if not ctx.user.guild_permissions.manage_roles:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "no_permission", config.language))
        return
    
    rs = ""
        
    rs += f"{emoji1} - {role1.mention}\n"
    if role2 and emoji2:
        rs += f"{emoji2} - {role2.mention}\n"
    if role3 and emoji3:
        rs += f"{emoji3} - {role3.mention}\n"
    if role4 and emoji4:
        rs += f"{emoji4} - {role4.mention}\n"
    if role5 and emoji5:
        rs += f"{emoji5} - {role5.mention}\n"

    eb = discord.Embed(
        title=prompt_message,
        description=rs,
        color=discord.Color.blue()
    ) 
    try:
        msg = await ctx.channel.send(embed=eb)
    except discord.Forbidden:
        await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "bot_no_permission", config.language))
        return
    reaction_roles.add_reaction_role(msg.id, emoji1, role1.id, one_role)
    if role2 and emoji2:
        reaction_roles.add_reaction_role(msg.id, emoji2, role2.id, one_role)
    if role3 and emoji3:
        reaction_roles.add_reaction_role(msg.id, emoji3, role3.id, one_role)
    if role4 and emoji4:
        reaction_roles.add_reaction_role(msg.id, emoji4, role4.id, one_role)
    if role5 and emoji5:
        reaction_roles.add_reaction_role(msg.id, emoji5, role5.id, one_role)
    
    for emoji in [emoji1, emoji2, emoji3, emoji4, emoji5]:
        if emoji:
            try:
                await msg.add_reaction(emoji)
            except discord.errors.HTTPException:
                await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "failed", config.language))
                return
            except discord.Forbidden:
                await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "bot_no_permission", config.language))
                return
    
    await ctx.followup.send(lib.locareader.get_string_by_id(loca_sheet, "success", config.language))
    
    
