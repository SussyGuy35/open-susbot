import discord
import random

def command_response(user_input: str):
    message_output = []
    for i in range(len(user_input)):
        char = user_input[i]
        char = [char.lower(),char.upper()]
        message_output.append(random.choice(char))
    return ''.join(message_output)

async def command_listener(message: discord.Message, usr_input: str):
    await message.channel.send(command_response(usr_input))
