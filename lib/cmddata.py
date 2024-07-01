"""Using external data files for commands"""

def file_save_open_read(filepath: str):
    """Open save file for read"""
    return open("commands/data/save + temp/" + filepath, "r")


def file_save_open_write(filepath: str):
    """Open save file for write"""
    return open("commands/data/save + temp/" + filepath, "w+")


def file_res_open_read(filepath: str):
    """Open resource file for read"""
    return open("commands/data/res/" + filepath, "r")


def get_save_file_path(file_or_dir_name: str):
    """Get save file path"""
    return "commands/data/save + temp/" + file_or_dir_name


def get_res_file_path(file_or_dir_name: str):
    """Get resource file path"""
    return "commands/data/res/" + file_or_dir_name
