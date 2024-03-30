import discord

async def delete_message(message: discord.Message):
    try:
        await message.delete()
    except discord.Forbidden:
        print("cannot delete message or sth")
        return

def command_response(command):
    return command