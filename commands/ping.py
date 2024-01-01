try:
    import config_override as config
except:
    import config
from lib.locareader import get_string_by_id

loca_sheet = "loca/loca - ping.csv"

def command_response():
    return get_string_by_id(loca_sheet,"ping",config.language)