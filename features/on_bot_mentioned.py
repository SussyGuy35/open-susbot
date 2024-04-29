try:
    import config_override as config
except:
    import config
import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix

async def reply(message: discord.Message):
    await message.reply(
        get_string_by_id("loca/loca - main.csv", "on_mentioned_response", config.language).format(get_prefix(message.guild))
    )