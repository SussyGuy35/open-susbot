try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_list

loca_sheet = "loca/loca - help.csv"

def get_help_text(prefix):
    help_text = ""
    for line in get_string_list(loca_sheet, config.language):
        help_text += line + "\n"
    return help_text.format(prefix)

def command_response(prefix):
    return get_help_text(prefix)