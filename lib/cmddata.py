"""Using external data files for commands"""
from pathlib import Path
Path("commands/data/save").mkdir(parents=True, exist_ok=True)
Path("commands/data/temp").mkdir(parents=True, exist_ok=True)

def file_save_open_read(filepath: str, mode: str = "r"):
    """Open save file for read"""
    return open("commands/data/save/" + filepath, mode)


def file_save_open_write(filepath: str, mode: str = "w+"):
    """Open save file for write"""
    return open("commands/data/save/" + filepath, mode)


def file_temp_open_read(filepath: str, mode: str = "r"):
    """Open temp file for read"""
    return open("commands/data/temp/" + filepath, mode)


def file_temp_open_write(filepath: str, mode: str = "w+"):
    """Open temp file for write"""
    return open("commands/data/temp/" + filepath, mode)


def file_res_open_read(filepath: str, mode: str = "r"):
    """Open resource file for read"""
    return open("commands/data/res/" + filepath, mode)


def get_save_file_path(file_or_dir_name: str):
    """Get save file path"""
    return "commands/data/save + temp/" + file_or_dir_name


def get_res_file_path(file_or_dir_name: str):
    """Get resource file path"""
    return "commands/data/res/" + file_or_dir_name


def get_temp_file_path(file_or_dir_name: str):
    """Get temp file path"""
    return "commands/data/temp/" + file_or_dir_name
