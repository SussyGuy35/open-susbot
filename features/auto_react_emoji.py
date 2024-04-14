import discord

async def react(autoreact_emojis: list, message: discord.Message):
    # Auto react emojis
    for word, emojis in autoreact_emojis.items():
        if word in message.content.lower():
            for emoji in emojis:
                try:
                    await message.add_reaction(emoji)
                except:
                    pass
            break