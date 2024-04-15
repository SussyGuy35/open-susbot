import discord

async def react(autoreact_emojis: list, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type == discord.ChannelType.text or message.channel.type == discord.ChannelType.voice:
        for word, emojis in autoreact_emojis.items():
            if word in message.content.lower():
                for emoji in emojis:
                    try:
                        await message.add_reaction(emoji)
                    except:
                        pass
                break