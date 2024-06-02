import discord
from lib.sussyconfig import get_config
import commands.gvs as gkevaysao

config = get_config()


async def gvs(message: discord.Message, userid: str, username: str):
    if message.author.bot:
        return
    if message.channel.type in config.autoreact_emojis_supported_channel_types:
        if "gvs" in message.content.lower():
            gkevaysao.gvs(userid, username, str(message.guild.id))
