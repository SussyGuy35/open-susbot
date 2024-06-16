import discord
import os
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata

img_rand_path = cmddata.get_path("khoa/khoa_quote/")
img_search_path = cmddata.get_path("khoa/khoa_search/")

def search_files(path, name):
    for (root,dirs, files) in os.walk(path):
        for f in files:
            if name in f:
                return f

async def search_khoa(q, ctx: discord.Interaction):
    q = q.replace(" ","_")
    directory_path = 'khoa_search//'
    matching_files = search_files(directory_path, q)
    await ctx.response.defer()
    if matching_files != None:
        await ctx.followup.send(file=discord.File(img_search_path + matching_files))
    else:
        await ctx.followup.send(file=discord.File('Ăng khoa chưa nói câu nào như thế!'))

def command_response():
    return discord.File(img_rand_path + pick_random_file_from_dir(img_rand_path))

async def slash_command_listener(ctx: discord.Interaction):
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
