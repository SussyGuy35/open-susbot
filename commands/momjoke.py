import discord
import requests



def command_response():
    return requests.get("https://www.yomama-jokes.com/api/v1/jokes/random/").json()["joke"]


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used momjoke commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response())
