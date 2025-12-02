import discord
import lib.sussyhelper as sh
import lib.locareader as loca_reader
import lib.miniomanager as store
import random

loca_sheet = "loca/loca - nijika.csv"
cmd_names = ['nijika', 'njk', 'doritos']

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


def command_response():
    return random.choice(store.list_images(prefix='nijika/'))


async def command_listener(message: discord.Message):
    await message.channel.send(file=command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())
