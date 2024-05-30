import discord
try:
    import config_override as config
except:
    import config
import commands.gvs as gkevaysao



async def gvs(message: discord.Message, userid: str, username: str):
    if message.author.bot:
        return
    if message.channel.type in config.autoreact_emojis_supported_channel_types:
        if "gvs" in message.content.lower():
            gkevaysao.gvs(userid, username, str(message.guild.id))
