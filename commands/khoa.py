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

async def fetch_khoa_images_list():
    global image_db
    from lib.sussyutils import get_text_async
    text = await get_text_async(config.image_endpoint + config.file_list_name)
    image_db = [i for i in text.splitlines() if i.startswith("./khoa/")]


async def search_files(name: str):
    await fetch_khoa_images_list()
    if not name:
        return random.choice(image_db)
    for files in image_db:
        if name.lower() in files.lower():
            return files
    return None

async def search_khoa(q: str):
    q = q.replace(" ","_")
    matching_files = await search_files(q)
    if matching_files is not None:
        return config.image_endpoint + matching_files.replace(" ", "%20")
    else:
        return get_string_by_id(loca_sheet, "prompt_not_found")


async def command_response(search: str | None = None) -> str:
    try:
        if not search:
            return config.image_endpoint + (await search_files("")).replace(" ", "%20")
        else:
            return await search_khoa(search)
    except Exception as e:
        return f"Error: {e}"


async def slash_command_listener(ctx: discord.Interaction, search: str | None = None):
    print(f"{ctx.user} used khoa commands!")
    await ctx.response.defer(ephemeral=True)
    responce = await command_response(search)
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
