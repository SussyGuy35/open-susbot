import discord
from os import remove
from requests import get

def get_file(url, file_name) -> str:
    """Get a file from given url. Return file's name if the request was successful, raise error if not."""
    if file_name.split(".")[-1] in ["png", "jpg", "webp", "bmp"]:
        # Send a GET request to the URL
        response = get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Get the content of the response (i.e., the file data)
            file_data = response.content    
            new_file_name = file_name[:-len(file_name.split(".")[-1])]+"gif"
        else:
            raise Exception("Can't download the file for some reasons")
        with open(f"{new_file_name}", "wb") as f:
            f.write(file_data)
        return new_file_name
    else:
        raise ValueError("This file type is not supported") 

def post_response_cleanup(response):
    if type(response) == discord.File:
        remove(response.filename)

def command_response(attachment) -> discord.File | str:
    try:
        file_name = get_file(attachment.url, attachment.filename)
    except ValueError:
        return "File đã là gif hoặc không được hỗ trợ (đi mà hỏi thằng chủ bot)"
    except:
        return "Đã có lỗi trong quá trình xử lý"
    else:
        return discord.File(file_name)