import discord
import os
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata

img_path = cmddata.get_path("khoa/")

def search_files(path, name):
    for (root,dirs, files) in os.walk(path):
        for f in files:
            if name in f:
                return f
            
async def list_name(ctx):
    file_names = os.listdir(img_path)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(img_path, f))]
    res = [f.replace('_', ' ').replace('.jpg', '') for f in file_names]
    body = "\n".join([f"{index + 1}. `{item}`" for index, item in enumerate(res)])
    msg = f"`{"Tổng hợp những câu nói bất hủ của a khoa"}`\n\n`{"Sử dụng lệnh search để hiển thị câu nói bạn cần"}`\n\n{body}"
    await ctx.response.defer()
    await ctx.followup.send(msg)

async def search_khoa(q, ctx: discord.Interaction):
    q = q.replace(" ","_")
    matching_files = search_files(img_path, q)
    await ctx.response.defer()
    if matching_files != None:
        await ctx.followup.send(file=discord.File(img_path + matching_files))
    else:
        await ctx.followup.send('Ăng khoa chưa nói câu nào như thế!')

def command_response():
    return discord.File(img_path + pick_random_file_from_dir(img_path))

async def slash_command_listener(ctx: discord.Interaction):
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
