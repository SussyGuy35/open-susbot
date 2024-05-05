import discord
import requests


def command_response(is_cat_girl):
    if is_cat_girl:
        return requests.get("https://nekos.life/api/v2/img/neko").json()["url"]
    else:
        return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]


async def slash_command_listener(ctx: discord.Interaction, is_cat_girl: bool):
    print(f"{ctx.user} used randcat commands!")
    await ctx.response.defer()
    await ctx.followup.send(command_response(is_cat_girl))
