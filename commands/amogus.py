import discord
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata

cmd_names = ["amogus", "sus"]

img_path = cmddata.get_res_file_path("susimg/")


def command_response():
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def command_listener(message: discord.Message):
    await message.channel.send(file=command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used amogus commands!")
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
