import discord

supported_channel_types = [
    discord.ChannelType.text,
    discord.ChannelType.voice,
    discord.ChannelType.public_thread
]


async def react(autoreact_emojis: dict, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type in supported_channel_types:
        for word, emojis in autoreact_emojis.items():
            if word in message.content.lower():
                for emoji in emojis:
                    try:
                        await message.add_reaction(emoji)
                    except:
                        pass
                break
