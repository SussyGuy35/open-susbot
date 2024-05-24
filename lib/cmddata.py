"""Using external data files for commands"""

def open_file_read(filepath: str):
    """Open data file for read"""
    return open("commands/data/" + filepath, "r")


def open_file_write(filepath: str):
    """Open data file for write"""
    return open("commands/data/" + filepath, "w+")


def get_path(file_or_dir_name: str):
    """Get data file path"""
    return "commands/data/" + file_or_dir_name