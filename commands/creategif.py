import discord
from os import remove
from requests import get
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
from lib.cmddata import get_save_file_path

config = get_config()

loca_sheet = "loca/loca - creategif.csv"


def get_file(url, file_name) -> str:
    """Get a file from given url. Return file's name if the request was successful, raise error if not."""
    if file_name.split(".")[-1] in ["png", "jpg", "webp", "bmp"]:
        # Send a GET request to the URL
        response = get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Get the content of the response (i.e., the file data)
            file_data = response.content
            new_file_name = file_name[:-len(file_name.split(".")[-1])] + "gif"
        else:
            raise Exception("Can't download the file for some reasons")
        with open(get_save_file_path(new_file_name), "wb+") as f:
            f.write(file_data)
        return new_file_name
    else:
        raise ValueError("This file type is not supported")


def post_response_cleanup(response: discord.File | str):
    if isinstance(response, discord.File):
        remove(get_save_file_path(response.filename))


def command_response(attachment: discord.Attachment) -> discord.File | str:
    try:
        file_name = get_file(attachment.url, attachment.filename)
    except ValueError:
        return get_string_by_id(loca_sheet, "prompt_dont_support", config.language)
    except:
        return get_string_by_id(loca_sheet, "prompt_exception", config.language)
    else:
        return discord.File(get_save_file_path(file_name))


async def slash_command_listener(ctx: discord.Interaction, file: discord.Attachment):
    print(f"{ctx.user} used create_gif commands!")
    await ctx.response.defer()
    response = command_response(file)
    if isinstance(response, discord.File):
        await ctx.followup.send(file=response)
    elif isinstance(response, str):
        await ctx.followup.send(response)
    post_response_cleanup(response)
