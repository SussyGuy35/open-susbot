"""template to creating new command"""
import discord
import lib.sussyutils
import lib.locareader
from lib.sussyconfig import get_config

config = get_config()

CMD_NAME = "template"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"

def command_response():
    pass

async def command_listener(message: discord.Message):
    await message.channel.send(command_response())

async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())