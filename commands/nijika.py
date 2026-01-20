import discord
import lib.sussyhelper as sh
import lib.locareader as loca_reader
import lib.miniomanager as store
import random

loca_sheet = "loca/loca - nijika.csv"
cmd_names = ['nijika', 'njk', 'doritos']
img_db = []

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

def fetch_nijika_images():
    global img_db
    img_db = store.list_images(prefix='nijika/')


def command_response():
    if not img_db:
        fetch_nijika_images()
    return random.choice(img_db)

async def command_listener(message: discord.Message):
    await message.channel.send(command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())
