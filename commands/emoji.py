try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_by_id
import discord

loca_sheet = "loca/loca - emoji.csv"

def command_response(client, emoji: str):
    try:
        emoji_to_get = client.get_emoji(int(emoji.split()[0].split(":")[2].replace(">","")))
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