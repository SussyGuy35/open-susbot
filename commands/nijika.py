import discord
import os
from lib.sussyutils import pick_random_file_from_dir

base_path = os.path.dirname(os.path.abspath(__file__))

def absolute_path(relative_path: str) -> str:
    return os.path.join(base_path,relative_path)

imgpath = absolute_path("data/nijika/")

def command_response():
    return discord.File(imgpath + pick_random_file_from_dir(imgpath))

async def command_listener(message: discord.Message):
    await message.channel.send(file =command_response())

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(file = command_response())