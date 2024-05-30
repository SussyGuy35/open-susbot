import discord
try:
    import config_override as config
except:
    import config


async def react(autoreact_emojis: dict, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type in config.autoreact_emojis_supported_channel_types:
        for word, emojis in autoreact_emojis.items():
            if word in message.content.lower():
                for emoji in emojis:
                    try:
                        await message.add_reaction(emoji)
                    except:
                        pass
                break
