import discord
from lib.locareader import get_string_list, get_string_by_id
from lib.sussyconfig import get_config
import random

config = get_config()

loca_sheet = "loca/loca - ask.csv"

ans = get_string_list(loca_sheet, config.language)


def command_response(question: str):
    if question == '':
        return get_string_by_id("loca/loca - main.csv", "command_ask_no_question", config.language)
    else:
        return random.choice(ans)


async def command_listener(message: discord.Message, usr_input: str):
    await message.channel.send(command_response(usr_input))
