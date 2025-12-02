import discord
from pytz import timezone as tz

### Core config
bot_name = "open-susbot"
prefix = 'b!'
bot_version = '2.4'

TOKEN = 'ur bot token here'

MONGO_URI = 'mongodb uri here'
MONGO_DB_NAME = 'ur db name here'

S3_CONFIG = {
    'endpoint_url': 'https://minio1.webtui.vn:9000',  # MinIO server URL
    'aws_access_key_id': 'user',                 
    'aws_secret_access_key': 'password',             
    'region_name': 'us-east-1'                        # Region (Doesn't matter much for MinIO, but boto3 requires it)
}
S3_BUCKET_NAME = 'bucket-name-here'  # Bucket must be set to Public (Read Only or Public)

language = "en"  # bot's language

timezone = tz("Asia/Ho_Chi_Minh")  # timezone for the bot

dev_ids = [  # place developer's id here!
]

banned_users = []  # place banned users' id here!

specific_prefix = {
}  # Place custom prefix for specific server here in form "server_id: prefix"
# Example:
# specific_prefix = {
# 69420105727: "n!"
# }

### osu command configs
OSUAPI_CLIENT_ID = 'ur osu!api client id here'
OSUAPI_CLIENT_SECRET = 'ur osu!api client secret here'

### autoreact configs
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

### Ghostping detector configs
enable_ghostping_detector = False  # enable ghostping detector or not
ghostping_check_time_range = 15  # time to detect ghostping
ghostping_detector_blacklist_guild = []  # place id of servers that don't use ghostping detector here!
ghostping_detector_blacklist_user = []  # place id of users that should not be warned by the ghostping detector here!
