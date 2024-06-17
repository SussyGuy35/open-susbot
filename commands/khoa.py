import discord, random
import os
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata

img_path = cmddata.get_path("khoa/")


def search_files(path, name):
    for (root,dirs, files) in os.walk(path):
        for f in files:
            if name in f:
                return f
            

def search_khoa(q: str):
    q = q.replace(" ","_")
    matching_files = search_files(img_path, q)
    if matching_files != None:
        return discord.File(img_path + matching_files)
    else:
        return "Ăng khoa chưa nói câu nào như thế!"


def command_response(search: str = None) -> discord.File | str:
    if search:
        return search_khoa(search)
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def slash_command_listener(ctx: discord.Interaction, search: str = None):
    print(f"{ctx.user} used khoabug command")
    await ctx.response.defer()
    responce = command_response(search)
    if isinstance(responce, str):
        await ctx.followup.send(responce)
    else:
        await ctx.followup.send(file=responce)


async def slash_command_listener_list(ctx: discord.Interaction):
    print(f"{ctx.user} used khoalist command")
    await ctx.response.defer()
    file_names = os.listdir(img_path)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(img_path, f))]
    res = [f.replace('_', ' ').replace('.jpg', '') for f in file_names]
    random_res = random.sample(res, min(len(res), 10))
    body = "\n".join([f"> {item}\n" for item in random_res])
    msg = (f"# Tổng hợp một số câu nói bất hủ của ăng Khoa (chắc ăng Khoa k biết đâu):\n{body}")
    await ctx.followup.send(msg)
