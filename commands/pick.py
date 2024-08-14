import discord
import random


def command_response(args: list[str], plain_args: str):
    options = []
    if '"' in plain_args:
        options = args
    else:
        options = plain_args.split(',')
    return random.choice(options)


async def command_listener(message: discord.Message, args: list[str], plain_args: str):
    await message.channel.send(command_response(args, plain_args))
