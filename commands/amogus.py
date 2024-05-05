import discord
import os
from lib.sussyutils import pick_random_file_from_dir

base_path = os.path.dirname(os.path.abspath(__file__))


def absolute_path(relative_path: str) -> str:
    return os.path.join(base_path, relative_path)


img_path = absolute_path("data/susimg/")


def command_response():
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def command_listener(message: discord.Message):
    await message.channel.send(file=command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
