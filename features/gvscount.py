import discord
import commands.gvs as gkevaysao
from features.auto_react_emoji import supported_channel_types as autoreact_emojis_supported_channel_types
import config



async def gvs(message: discord.Message, userid: str):
    if message.author.bot:
        return
    if message.channel.type in autoreact_emojis_supported_channel_types:
        if "gvs" in message.content.lower():
            gkevaysao.gvs(userid, str(message.guild.id))
