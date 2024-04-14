try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_emoji_id_from_snowflake

loca_sheet = "loca/loca - emoji.csv"

def command_response(client: discord.Client, emoji: str):
    try:
        emoji_to_get = client.get_emoji(get_emoji_id_from_snowflake(emoji))
    except:
        print(f"ERROR: Failed to get emoji. Message: {emoji}")
        emoji_to_get = None
    
    if emoji_to_get is not None:
        embed = discord.Embed(
            title=emoji_to_get.name,
            description = get_string_by_id(loca_sheet,"embed_desc",config.language).format(int(emoji_to_get.created_at.timestamp())), 
            color=0x03e3fc
        )
        embed.set_image(url = emoji_to_get.url)
        return embed
    else:
        return get_string_by_id(loca_sheet, "prompt_exception", config.language)
    
async def slash_command_listener(client: discord.Client, ctx: discord.Interaction, emoji: str):
    print(f"{ctx.user} used emoji commands!")
    await ctx.response.defer()
    rs = command_response(client,emoji)
    if type(rs) == str:
        await ctx.followup.send(rs)
    else:
        await ctx.followup.send(embed = rs)