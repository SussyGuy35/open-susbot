import os
import discord
import lib.sussyhelper as sh
import lib.locareader as loca_reader
import lib.sussyconfig as sussy_config
import random, requests

loca_sheet = "loca/loca - nijika.csv"
cmd_names = ['nijika', 'njk', 'doritos']
img_db = []

config = sussy_config.get_config()

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.HYBRID,
        description=loca_reader.get_string_by_id(loca_sheet, "command_desc"),
        usage=loca_reader.get_string_by_id(loca_sheet, "command_usage"),
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.GENERAL2
)

def fetch_nijika_images_list():
    global img_db
    img_db = requests.get(config.NIJIKA_IMAGE_ENDPOINT + os.getenv("IMAGE_LIST_FILE_NAME", "file_list.txt")).text.splitlines()


def command_response():
    if not img_db:
        fetch_nijika_images_list()
    return config.NIJIKA_IMAGE_ENDPOINT + random.choice(img_db).replace(" ", "%20")

async def command_listener(message: discord.Message):
    await message.channel.send(command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())
