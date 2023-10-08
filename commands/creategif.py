from os import remove
import discord
from requests import get

def get_file(url, file_name):
    """Get a file from given url. Return file's name if the request was successful, None if not."""
    # Send a GET request to the URL
    response = get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the content of the response (i.e., the file data)
        file_data = response.content
        if file_name.split(".")[-1] in ["png", "jpg", "webp", "bmp"]:
            new_file_name = file_name[:-len(file_name.split(".")[-1])]+"gif"
        else:
            return None
        with open(f"{new_file_name}", "wb") as f:
            f.write(file_data)
        return new_file_name
    else:
        return None

def command_response(attactment):
    file_name = get_file(attactment.url, attactment.filename)

    if file_name:
        file = discord.File(file_name)
        remove(file_name)
        return file
    else:
        return "Xin lỗi, đã có lỗi xảy ra!"