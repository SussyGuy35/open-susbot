import discord, datetime, os
import features.auto_react_emoji
from lib.locareader import get_string_by_id
import lib.himom as himom

if os.path.exists("config_override.py"):
    import config_override as config
else:
    import config

# Config
bot_version = config.bot_version

TOKEN = config.TOKEN

print(f'{config.bot_name} v{bot_version}')
himom.himom() # say hi to ur mom!

# import commands
from commands import (
    amogus, ask, creategif, echo, emoji as getemoji,
    gacha, gvs, help as bot_help, nijika, osu, pick,
    ping, randcaps, randcat, randwaifu, getprefix,
    avatar, bean
)

# import features
import features.ghostping_detector

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
ossapi_client = osu.client(config.OSUAPI_CLIENT_ID, config.OSUAPI_CLIENT_SECRET)

tree = discord.app_commands.CommandTree(client)

# bot prefix
def get_prefix(guild: discord.Guild):
    return getprefix.get_prefix(guild)

# autoreact emojis
autoreact_emojis = config.autoreact_emojis

#loca thing
def get_string(id: str, loca: str = "main"):
    return get_string_by_id(f"loca/loca - {loca}.csv",id,config.language)

# Send feedback
class FeedbackButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label=get_string("feedback_button_1"),style=discord.ButtonStyle.red,emoji = "💲")
    async def dua_tien_day(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(get_string("feedback_button_1_prompt").format(interaction.user))
        button.disabled = True
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label=get_string("feedback_button_2"),style=discord.ButtonStyle.gray,emoji = "🔫")
    async def bot_dao_lua(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(get_string("feedback_button_2_prompt").format(interaction.user))
        button.disabled = True
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label=get_string("feedback_button_3"),style=discord.ButtonStyle.blurple,emoji = "🐧")
    async def dev_tu_ban(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(get_string("feedback_button_3_prompt").format(interaction.user))
        button.disabled = True
        await interaction.response.edit_message(view=self)

# Slash command

# Feedback
@tree.command(name = "feedback", description = get_string("command_feedback_desc"))
async def button(ctx: discord.Interaction):
    view = FeedbackButtons()
    view.add_item(discord.ui.Button(label=get_string("feedback_button_4"),style=discord.ButtonStyle.link,url="https://SussyGuy35.github.io/duatienday.html",emoji="😏"))
    print(f"{ctx.user} used feedback commands!")
    await ctx.response.send_message(get_string("command_feedback_prompt"),view=view)

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
    await osu.slash_command_listener_user(ossapi_client, ctx, username)

# osu beatmap
@tree.command(name = "osu_beatmap", description = get_string("command_osu_beatmap_desc")) 
async def osu_beatmap(ctx: discord.Interaction, beatmap: str):
    await osu.slash_command_listener_beatmap(ossapi_client, ctx, beatmap)

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
    await client.change_presence(activity = discord.Streaming(name = 'My creator hates me',url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    prompt = f"""Logged in as {client.user}. Currently in {str(len(client.guilds))} server(s)!
List of current joined server(s):
"""
    for guild in client.guilds:
        prompt += f"{guild}\n"
    print(prompt)
# On message delete event
@client.event
async def on_message_delete(message):
    # Ghost ping detector 6900
    await features.ghostping_detector.ghostping_detector_on_delete(message)

# On message edit event
@client.event
async def on_message_edit(before, after):
    # Ghost ping detector 6900
    await features.ghostping_detector.ghostping_detector_on_edit(before,after)

# On message event
@client.event
async def on_message(message: discord.Message):
    global date, cardgame_data, cardshop_data
    
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
                await message.channel.send(bot_help.command_response(prefix))
            
            # Ping pong ping pong
            case 'ping':
                await message.channel.send(ping.command_response())

            # Echo
            case 'echo':
                await echo.delete_message(message)
                await message.channel.send(echo.command_response(plain_args))
            
            # Pick
            case 'pick':
                await message.channel.send(pick.command_response(plain_args))
            
            # Random caps
            case 'randcaps':
                await message.channel.send(randcaps.command_response(plain_args))
            
            # Gacha
            case 'gacha':
                command_response = gacha.command_response(message.content,prefix,userid,username)
                user_level_up_response = gacha.check_if_user_level_up(userid)
                super_user = gacha.cardgame_user_check_beaten(userid)
                if command_response != None:
                    if type(command_response) == str:
                        await message.channel.send(command_response)
                    else:
                        await message.channel.send(file = command_response)
                if user_level_up_response != None:
                    await message.channel.send(user_level_up_response)
                if super_user != None:
                    await message.channel.send(super_user)
                gacha.save()    
            
            # osu!
            case 'osu':
                await message.channel.send(osu.command_response(ossapi_client,prefix,plain_args))
            
            # emoji
            case 'emoji':
                rs = getemoji.command_response(client,args[0])
                if type(rs) == str:
                    await message.channel.send(rs)
                else:
                    await message.channel.send(embed = rs)
            
            # Ask
            case 'ask':
                await message.channel.send(ask.command_response(plain_args))
            
            # Nijika
            case 'nijika':
                await message.channel.send(file = nijika.command_response())

            # Amogus
            case 'amogus':
                await message.channel.send(file = amogus.command_response())
            
            # Gvs
            case 'gvs':
                if message.channel.type == discord.ChannelType.text or message.channel.type == discord.ChannelType.voice:
                    response = gvs.command_response(prefix,userid, message.guild,args)
                    if type(response) == discord.Embed:
                        await message.channel.send(embed = response)
                    elif type(response) == str:
                        await message.channel.send(response)
                else:
                    await message.channel.send(get_string("not_supported", "gvs"))
            # Invalid command
            case _:
                await message.channel.send(get_string("command_not_found_prompt"))
           
    else:
        if not message.author.bot:
            if message.channel.type == discord.ChannelType.text or message.channel.type == discord.ChannelType.voice:
                # gvs
                if "gvs" in message.content.lower():
                    gvs.gvs(userid, username, str(message.guild.id))
            
                # Auto react emojis
                await features.auto_react_emoji.react(autoreact_emojis, message)

client.run(TOKEN)
