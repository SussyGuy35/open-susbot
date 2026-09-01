import discord
import lib.sussyhelper as sh
import lib.locareader as loca_reader
import lib.sussyconfig as sussy_config
import requests
import random

loca_sheet = "loca/loca - ryo.csv"

cmd_names = ['ryo']
image_db = []

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

async def fetch_ryo_images_list():
    global image_db
    from lib.sussyutils import get_text_async
    text = await get_text_async(config.image_endpoint + config.file_list_name)
    image_db = [i for i in text.splitlines() if i.startswith("./ryo/")]


async def command_response():
    if not image_db:
        await fetch_ryo_images_list()
    return config.image_endpoint + random.choice(image_db).replace(" ", "%20")

async def command_listener(message: discord.Message):
    await message.channel.send(await command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used ryo commands!")
    await ctx.response.defer()
    await ctx.followup.send(await command_response())

