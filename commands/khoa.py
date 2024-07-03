import discord, random
import os
from lib.sussyutils import pick_random_file_from_dir
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import lib.cmddata as cmddata

config = get_config()

img_path = cmddata.get_res_file_path("khoa/")
loca_sheet = "loca/loca - khoa.csv"

def search_files(path: str, name: str):
    for (root, dirs, files) in os.walk(path):
        for f in files:
            if name.lower() in f.lower():
                return f
            

def search_khoa(q: str):
    q = q.replace(" ","_")
    matching_files = search_files(img_path, q)
    if matching_files != None:
        return discord.File(img_path + matching_files)
    else:
        return get_string_by_id(loca_sheet, "quote_not_found", config.language)


def command_response(search: str = None) -> discord.File | str:
    if search:
        return search_khoa(search)
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def slash_command_listener(ctx: discord.Interaction, search: str = None):
    print(f"{ctx.user} used khoabug command with search: {search}")
    await ctx.response.defer(ephemeral=True)
    responce = command_response(search)
    if isinstance(responce, str):
        await ctx.followup.send(responce)
    else:
        await ctx.channel.send(file=responce)
        await ctx.followup.send(get_string_by_id(loca_sheet, "success", config.language))


async def slash_command_listener_list(ctx: discord.Interaction):
    print(f"{ctx.user} used khoalist command")
    await ctx.response.defer()
    file_names = os.listdir(img_path)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(img_path, f))]
    res = [f.replace('_', ' ').replace('.jpg', '') for f in file_names]
    random_res = random.sample(res, min(len(res), 10))
    body = "\n".join([f"- > {item}" for item in random_res])
    msg = get_string_by_id(loca_sheet, "list_command_response_template", config.language).format(body)
    await ctx.followup.send(msg)
