import discord
import commands.gvs as gkevaysao

async def gvs(message: discord.Message, userid: str, username: str):
    if message.author.bot:
        return
    if message.channel.type == discord.ChannelType.text or message.channel.type == discord.ChannelType.voice:
        if "gvs" in message.content.lower():
            gkevaysao.gvs(userid, username, str(message.guild.id))