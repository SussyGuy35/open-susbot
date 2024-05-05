import discord


async def delete_message(message: discord.Message):
    try:
        await message.delete()
    except discord.Forbidden:
        print("cannot delete message or sth")
        return


def command_response(msg: str):
    new_msg = msg
    new_msg = new_msg.replace("@everyone", "`@everyone`").replace("@here", "`@here`")
    return new_msg


async def command_listener(message: discord.Message, msg: str):
    await delete_message(message)

    if message.reference is None:
        await message.channel.send(command_response(msg))
    else:
        if message.reference.cached_message is None:
            original_message = await message.channel.fetch_message(message.reference.message_id)
        else:
            original_message = message.reference.cached_message
        await original_message.reply(command_response(msg))
