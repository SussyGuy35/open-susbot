import discord

bot_name = "open-susbot"
prefix = 'b!'
bot_version = '2.3'

TOKEN = 'ur bot token here'

OSUAPI_CLIENT_ID = 'ur osu!api client id here'
OSUAPI_CLIENT_SECRET = 'ur osu!api client secret here'

language = "en"  # bot's language

dev_ids = [  # place developer's id here!
]

banned_users = []  # place banned users' id here!

specific_prefix = {
}  # Place custom prefix for specific server here in form "server_id: prefix"
# Example:
# specific_prefix = {
# 69420105727: "n!"
# }

autoreact_emojis = {
}  # place autoreact emojis here in form "word: emoji"
# Example:
# autoreact_emojis = {
#   "gvs": ["🇬","🇰","🇪","🇻","🇦","🇾","🇸","🅰️","🇴","😳"],
#   "tin chuan chua anh": ["🇯", "🇺", "🇦", "🇳"]
# }
autoreact_emojis_supported_channel_types = [
    discord.ChannelType.text,
    discord.ChannelType.voice,
    discord.ChannelType.public_thread
] # Supported channel types

enable_ghostping_detector = False  # enable ghostping detector or not
ghostping_check_time_range = 15  # time to detect ghostping
ghostping_detector_blacklist_guild = []  # place id of servers that don't use ghostping detector here!
ghostping_detector_blacklist_user = []  # place id of users that should not be warned by the ghostping detector here!
