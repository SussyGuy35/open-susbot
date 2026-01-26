import requests
import discord, random
from lib.locareader import get_string_by_id
import lib.sussyhelper as ssyhelper
import lib.sussyconfig as sussy_config
import random


loca_sheet = "loca/loca - khoa.csv"

config = sussy_config.get_config()
image_db = []

ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelp(
        command_name="khoabug",
        command_type=ssyhelper.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            ssyhelper.CommandParameterDescription(
                name="search",
                description=get_string_by_id(loca_sheet, "command_param_search_desc"),
                required=False
            )
        ],
    ),
    ssyhelper.HelpSection.GENERAL2
)

ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelp(
        command_name="khoalist",
        command_type=ssyhelper.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "list_command_desc"),
        usage=get_string_by_id(loca_sheet, "list_command_usage"),
    ),
    ssyhelper.HelpSection.GENERAL2
)

def fetch_khoa_images_list():
    global image_db
    image_db = [i for i in requests.get(config.image_endpoint + config.file_list_name).text.splitlines() if i.startswith("./khoa/")]


def search_files(name: str):
    fetch_khoa_images_list()
    if not name:
        return config.image_endpoint + random.choice(image_db).replace(" ", "%20")
    for files in image_db:
        for f in files:
            if name.lower() in f.lower():
                return f
            

def search_khoa(q: str):
    q = q.replace(" ","_")
    matching_files = search_files(q)
    if matching_files != None:
        return config.image_endpoint + matching_files.replace(" ", "%20")
    else:
        return get_string_by_id(loca_sheet, "quote_not_found")


def command_response(search: str | None = None) -> str:
    if search:
        return search_khoa(search)
    return search_files("")


async def slash_command_listener(ctx: discord.Interaction, search: str | None = None):
    print(f"{ctx.user} used khoabug command with search: {search}")
    await ctx.response.defer(ephemeral=True)
    responce = command_response(search)
    await ctx.followup.send(responce)


async def slash_command_listener_list(ctx: discord.Interaction):
    print(f"{ctx.user} used khoalist command")
    await ctx.response.defer()
    file_names = store.list_images(prefix='khoa/', return_names=True)
    res = [f.replace('_', ' ').replace('.jpg', '').replace('.png', '') for f in file_names]
    random_res = random.sample(res, min(len(res), 10))
    body = "\n".join([f"- > {item}" for item in random_res])
    msg = get_string_by_id(loca_sheet, "list_command_response_template").format(body)
    await ctx.followup.send(msg)
