import discord
import random

def command_response(usr_input: str):
    options = usr_input.split(',')
    return random.choice(options)

async def command_listener(message: discord.Message, usr_input: str):
    await message.channel.send(command_response(usr_input))

