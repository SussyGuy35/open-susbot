import discord
import os
from lib.locareader import get_string_by_id

if os.path.exists("config_override.py"):
    import config_override as config
else:
    import config

# Config
bot_version = config.bot_version

TOKEN = config.TOKEN

print(f'{config.bot_name} v{bot_version}')

# import commands
from commands import (
    amogus, ask, creategif, echo, emoji as getemoji,
    gvs, help as bot_help, nijika, osu, pick,
    ping, randcaps, randcat, randwaifu, getprefix,
    avatar, bean, feedback
)

# import features
import features.onready_things
import features.ghostping_detector
import features.auto_react_emoji
import features.gvscount
import features.on_bot_mentioned

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

# bot prefix
def get_prefix(guild: discord.Guild):
    return getprefix.get_prefix(guild)

# autoreact emojis
autoreact_emojis = config.autoreact_emojis

# loca thing
def get_string(id: str, loca: str = "main"):
    return get_string_by_id(f"loca/loca - {loca}.csv",id,config.language)

### Slash command
# Feedback
@tree.command(name = "feedback", description = get_string("command_feedback_desc"))
async def send_feedback(ctx: discord.Interaction):
    await feedback.slash_command_listener(ctx)

# Help
@tree.command(name = "help", description = get_string("command_help_desc")) 
async def help(ctx: discord.Interaction):
    await bot_help.slash_command_listener(ctx)

# Ping
@tree.command(name = "ping", description = get_string("command_ping_desc")) 
async def pingpong(ctx: discord.Interaction):
    await ping.slash_command_listener(ctx)

# Avatar
@tree.command(name = "avatar", description = get_string("command_avatar_desc")) 
async def get_avatar(ctx: discord.Interaction,user:discord.User,server_avatar:bool = True):
    await avatar.slash_command_listener(ctx, user, server_avatar)

# Emoji
@tree.command(name = "emoji", description = get_string("command_emoji_desc")) 
async def get_emoji(ctx: discord.Interaction, emoj: str):
    await getemoji.slash_command_listener(client, ctx, emoj)

# Nijika command
@tree.command(name = "nijika", description = get_string("command_nijika_desc"))
async def get_nijika_image(ctx: discord.Interaction):
    await nijika.slash_command_listener(ctx)

#Amogus command
@tree.command(name = "amogus", description = get_string("command_amogus_desc"))
async def get_amogus_image(ctx: discord.Interaction):
    await amogus.slash_command_listener(ctx)

# osu user
@tree.command(name = "osu_user", description = get_string("command_osu_user_desc")) 
async def osu_user(ctx: discord.Interaction, username: str):
    await osu.slash_command_listener_user(ctx, username)

# osu beatmap
@tree.command(name = "osu_beatmap", description = get_string("command_osu_beatmap_desc")) 
async def osu_beatmap(ctx: discord.Interaction, beatmap: str):
    await osu.slash_command_listener_beatmap(ctx, beatmap)

# gvs count
@tree.command(name = "gvs_count", description = get_string("command_gvs_count_desc"))
async def gvs_count(ctx: discord.Interaction):
    await gvs.slash_command_listener_count(ctx)

# gvs lb
@tree.command(name = "gvs_leaderboard", description = get_string("command_gvs_leaderboard_desc"))
async def gvs_lb(ctx: discord.Interaction):
    await gvs.slash_command_listener_lb(ctx)

# random cat girl
@tree.command(name = "randcat", description = get_string("command_randcat_desc"))
async def getrandcat(ctx: discord.Interaction, is_cat_girl:bool = False):
    await randcat.slash_command_listener(ctx, is_cat_girl)

# random waifu
@tree.command(name = "randwaifu", description = get_string("command_randwaifu_desc"))
async def getrandwaifu(ctx: discord.Interaction):
    await randwaifu.slash_command_listener(ctx)

# convert image to gif (kinda)
@tree.command(name="create_gif", description = get_string("command_create_gif_desc"))
async def create_gif(ctx: discord.Interaction, file: discord.Attachment):
    await creategif.slash_command_listener(ctx, file)

# Bean user
@tree.command(name="bean", description=get_string("embed_desc", "bean"))
async def bean_user(ctx: discord.Interaction, user: discord.User, reason: str):
    await bean.slash_command_listener(ctx, user, reason)

# Get bot prefix
@tree.command(name="get_prefix", description="Lấy prefix của con bot tại server hiện tại")
async def get_bot_prefix(ctx: discord.Interaction):
    await getprefix.slash_command_listener(ctx)

# On ready event
@client.event
async def on_ready():
    #tree.clear_commands(guild = None) # Uncomment this to clear all commands
    await tree.sync()
    await features.onready_things.on_ready(client)
# On message delete event
@client.event
async def on_message_delete(message):
    # Ghost ping detector 6900
    await features.ghostping_detector.on_delete(message)

# On message edit event
@client.event
async def on_message_edit(before, after):
    # Ghost ping detector 6900
    await features.ghostping_detector.on_edit(before,after)

# On message event
@client.event
async def on_message(message: discord.Message):
    
    # log console
    if message.author == client.user:
        print(">Bot:",message.content,"\n")
        return   
    
    userid = str(message.author.id)
    username = message.author.global_name
    prefix = get_prefix(message.channel.guild)

    # If someone use command
    if message.content.startswith(prefix):
        
        # log console
        print(f"{message.author.global_name} at #{message.channel} on {message.guild} : {message.content}")  
        
        # bot user can not use this bot's commands
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send(get_string("bot_use_command_prompt"))
                return
        
        if int(userid) in config.banned_users:
            await message.channel.send(get_string("banned_user_prompt"))
            return
        
        # Get requested command
        command = message.content.split()[0].replace(prefix,'')
        
        plain_args = message.content[len(prefix+command)+1:]
        args = plain_args.split()
        
        # Main thing
        match command:
            
            # Debug
            case 'debug':
                await message.channel.send(f"user_id: {message.author.id}, channel_id: {message.channel.id}, guild: {message.guild}")
            
            # Get loca string
            case 'getloca':    
                await message.channel.send(get_string_by_id(f"loca/loca - {args[0]}.csv", args[1], args[2]))

            # Help
            case 'help':
                await bot_help.command_listener(message)
            
            # Ping pong ping pong
            case 'ping':
                await ping.command_listener(message, client)

            # Echo
            case 'echo':
                await echo.command_listener(message, client, plain_args)
            
            # Pick
            case 'pick':
                await pick.command_listener(message, plain_args)
            
            # Random caps
            case 'randcaps':
                await randcaps.command_listener(message, plain_args)  
            
            # osu!
            case 'osu':
                await osu.command_listener(message, plain_args)
            
            # emoji
            case 'emoji':
                await getemoji.command_listener(message, client, args)
            
            # Ask
            case 'ask':
                await ask.command_listener(message, plain_args)
            
            # Nijika
            case 'nijika':
                await nijika.command_listener(message)

            # Amogus
            case 'amogus':
                await amogus.command_listener(message)
            
            # Gvs
            case 'gvs':
                await gvs.command_listener(message, args)
            # Invalid command
            case _:
                await message.channel.send(get_string("command_not_found_prompt"))
           
    else:
        # On bot mentioned
        if client.user.mentioned_in(message):
            await features.on_bot_mentioned.reply(message)

        # gvs
        await features.gvscount.gvs(message, userid, username)
        
        # Auto react emojis
        await features.auto_react_emoji.react(autoreact_emojis, message)

client.run(TOKEN)
