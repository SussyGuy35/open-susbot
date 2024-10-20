"""template to creating new command"""
import discord
import lib.sussyutils
import lib.locareader
from lib.sussyconfig import get_config

config = get_config()

cmd_names = ["template"]
loca_sheet = f"loca/loca - {cmd_names[0]}.csv"

def command_response():
    pass

async def command_listener(message: discord.Message):
    await message.channel.send(command_response())

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used {cmd_names[0]} commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())