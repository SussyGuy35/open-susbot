import discord, random

import os

def search_files(path, name):
    for (root,dirs, files) in os.walk(path):
        for f in files:
            if name in f:
                return f

async def search_khoa(q, ctx: discord.Interaction):
    q = q.replace(" ","_")
    print(q)
    directory_path = 'khoa_search//'
    matching_files = search_files(directory_path, q)
    await ctx.response.defer()
    await ctx.followup.send(file=discord.File(f'khoa_search/{matching_files}'))

def command_response():
    return discord.File(f'khoa_quote/k_{random.randint(1,35)}.jpg')

async def slash_command_listener(ctx: discord.Interaction):
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())