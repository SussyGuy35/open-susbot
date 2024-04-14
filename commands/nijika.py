import discord
from lib.sussyutils import pick_random_file_from_dir

imgpath = "data/nijika/"

def command_response():
    return discord.File(imgpath + pick_random_file_from_dir(imgpath))

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(file = command_response())