import discord
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata
import lib.sussyhelper as sh
import lib.locareader as loca_reader

loca_sheet = "loca/loca - ryo.csv"

cmd_names = ['ryo']

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.HYBRID,
        description=loca_reader.get_string_by_id(loca_sheet, "command_desc"),
        usage=loca_reader.get_string_by_id(loca_sheet, "command_usage")
    ),
    sh.HelpSection.GENERAL2
)

img_path = cmddata.get_res_file_path("ryo/")


def command_response():
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def command_listener(message: discord.Message):
    await message.channel.send(file=command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used ryo commands!")
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
