import discord
from lib.sussyutils import pick_random_file_from_dir
import lib.cmddata as cmddata
import lib.sussyhelper as sh

cmd_names = ["amogus", "sus"]

img_path = cmddata.get_res_file_path("susimg/")

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="amogus",
        command_type=sh.CommandType.HYBRID,
        description="Sussy",
        usage="amogus",
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.FUN
)

def command_response():
    return discord.File(img_path + pick_random_file_from_dir(img_path))


async def command_listener(message: discord.Message):
    await message.channel.send(file=command_response())


async def slash_command_listener(ctx: discord.Interaction):
    print(f"{ctx.user} used amogus commands!")
    await ctx.response.defer()
    await ctx.followup.send(file=command_response())
