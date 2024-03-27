bot_name = "open-susbot"
prefix = 'b!'
bot_version = '1.7'

TOKEN = 'ur bot token here'

OSUAPI_CLIENT_ID = 'ur osu!api client id here'
OSUAPI_CLIENT_SECRET = 'ur osu!api client secret here'

language = "en" # bot's language

banned_users = [] # place banned users's id here!

specific_prefix = {
} # Place custom prefix for specific server here in form "serverid: prefix"
# Example:
# specific_prefix = {
# 69420105727: "n!"
# }

autoreact_emojis = {
} # place autoreact emojis here in form "word: emoji"
# Example:
# autoreact_emojis = {
#   "gvs": ["🇬","🇰","🇪","🇻","🇦","🇾","🇸","🅰️","🇴","😳"],
#   "tin chuan chua anh": ["🇯", "🇺", "🇦", "🇳"]
# }

enable_ghostping_detector = False # enable ghostping detector or not
ghostping_check_time_range = 15 # time to detect ghostping
ghostping_detector_blacklist_guild = [] # place id of servers that dont use ghostping detector here!
ghostping_detector_blacklist_user = [] # place id of users that should not be warn by the ghostping detector here!