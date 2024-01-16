import discord, datetime, os
from lib.locareader import get_string_by_id

if os.path.exists("config_override.py"):
    import config_override as config
else:
    import config

# Config
prefix = config.prefix
bot_version = config.bot_version

TOKEN = config.TOKEN

print(f'{config.bot_name} v{bot_version}')

# import commands
from commands import (
    amogus, ask, creategif, echo, emoji,
    gacha, gvs, help as bot_help, nijika, osu, pick,
    ping, randcaps, randcat, randwaifu
)

OSUAPI_CLIENT_ID = config.OSUAPI_CLIENT_ID
OSUAPI_CLIENT_SECRET = config.OSUAPI_CLIENT_SECRET

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
ossapi_client = osu.client(OSUAPI_CLIENT_ID,OSUAPI_CLIENT_SECRET)

tree = discord.app_commands.CommandTree(client)

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
    print(f"{ctx.user} used help commands!")
    await ctx.response.send_message(bot_help.command_response(prefix))

# Ping
@tree.command(name = "ping", description = get_string("command_ping_desc")) 
async def ping(ctx: discord.Interaction):
    print(f"{ctx.user} used ping commands!")
    await ctx.response.send_message(ping.command_response())

# Avatar
@tree.command(name = "avatar", description = get_string("command_avatar_desc")) 
async def get_avatar(ctx: discord.Interaction,user:discord.User,server_avatar:bool = True):
    print(f"{ctx.user} used avatar commands!")
    await ctx.response.defer()
    avatar = user.display_avatar if server_avatar else user.avatar
    if avatar != None:
        embed = discord.Embed(title=get_string("command_avatar_embed_title"), description=get_string("command_avatar_embed_desc").format(user), color=0x03e3fc, type = "image")
        embed.set_image(url = avatar.url)
        await ctx.followup.send(embed = embed)
    else:
        await ctx.followup.send(get_string("command_avatar_noavatar"))

# Emoji
@tree.command(name = "emoji", description = get_string("command_emoji_desc")) 
async def get_emoji(ctx: discord.Interaction,emoji: str):
    print(f"{ctx.user} used emoji commands!")
    await ctx.response.defer()
    rs = emoji.command_response(client,emoji)
    if type(rs) == str:
        await ctx.followup.send(rs)
    else:
        await ctx.followup.send(embed = rs)

# Nijika command
@tree.command(name = "nijika", description = get_string("command_nijika_desc"))
async def nijika(ctx: discord.Interaction):
    print(f"{ctx.user} used nijika commands!")
    await ctx.response.defer()
    await ctx.followup.send(file = nijika.command_response())

#Amogus command
@tree.command(name = "amogus", description = get_string("command_amogus_desc"))
async def amogus(ctx: discord.Interaction):
    print(f"{ctx.user} used amogus commands!")
    await ctx.response.defer()
    await ctx.followup.send(file = amogus.command_response())

# osu user
@tree.command(name = "osu_user", description = get_string("command_osu_user_desc")) 
async def osu_user(ctx: discord.Interaction, username: str):
    print(f"{ctx.user} used osu user commands!")
    await ctx.response.defer()
    await ctx.followup.send(osu.command_response(ossapi_client,prefix,"user " + username))

# osu beatmap
@tree.command(name = "osu_beatmap", description = get_string("command_osu_beatmap_desc")) 
async def osu_beatmap(ctx: discord.Interaction, beatmap: str):
    print(f"{ctx.user} used osu beatmap commands!")
    await ctx.response.defer()
    await ctx.followup.send(osu.command_response(ossapi_client,prefix,"beatmap " + beatmap))

# gvs count
@tree.command(name = "gvs_count", description = get_string("command_gvs_count_desc"))
async def gvs_count(ctx: discord.Interaction):
    print(f"{ctx.user} used gvs count commands!")
    await ctx.response.defer()
    await ctx.followup.send(gvs.command_response(prefix,str(ctx.user.id),ctx.guild,["count"]))

# gvs lb
@tree.command(name = "gvs_leaderboard", description = get_string("command_gvs_leaderboard_desc"))
async def gvs_lb(ctx: discord.Interaction):
    print(f"{ctx.user} used gvs lb commands!")
    await ctx.response.defer()
    response = gvs.command_response(prefix,str(ctx.user.id), ctx.guild,["lb"])
    if type(response) == discord.Embed:
        await ctx.followup.send(embed = response)
    elif type(response) == str:
        await ctx.followup.send(response)

# random cat girl
@tree.command(name = "randcat", description = get_string("command_randcat_desc"))
async def randcat(ctx: discord.Interaction, is_cat_girl:bool = False):
    print(f"{ctx.user} used randcat commands!")
    await ctx.response.defer()
    await ctx.followup.send(randcat.command_response(is_cat_girl))

# random waifu
@tree.command(name = "randwaifu", description = get_string("command_randwaifu_desc"))
async def randwaifu(ctx: discord.Interaction):
    print(f"{ctx.user} used randwaifu commands!")
    await ctx.response.defer()
    await ctx.followup.send(randwaifu.command_response())

# convert image to gif (kinda)
@tree.command(name="create_gif", description = get_string("command_create_gif_desc"))
async def create_gif(ctx: discord.Interaction, file: discord.Attachment):
    print(f"{ctx.user} used createg_gif commands!")
    await ctx.response.defer()
    response = creategif.command_response(file)
    if type(response) == discord.File:
        await ctx.followup.send(file=response)
    elif type(response) == str:
        await ctx.followup.send(response)
    creategif.post_response_cleanup(response)

# Bean user
@tree.command(name="bean", description=get_string("embed_desc", "bean"))
async def bean(ctx: discord.Interaction, user: discord.User, reason: str):
    print(f"{ctx.user} used bean commands!")
    await ctx.response.defer()
    await ctx.followup.send(get_string("bean", "bean").format(user, reason))

# Ghost ping detector
async def ghostping_detector_on_delete(message):
    if (datetime.datetime.now(datetime.timezone.utc) - message.created_at).total_seconds() > config.ghostping_check_time_range:
        return
    if message.author.id in config.ghostping_detector_blacklist_user:
        return
    if (len(message.mentions) == 0 or (len(message.mentions) == 1 and (message.mentions[0] == message.author or message.mentions[0].bot))):
        if not message.mention_everyone:
            return
    if message.author.bot:
        return
    else:
        if message.mention_everyone: victims = "@everyone"
        else:
            victims = ""
            for victim in message.mentions:
                if not victim.bot:
                    victims += f"<@{victim.id}> "
        if victims == "": return
        print(f"{message.author.name} ghostping in {message.guild}!")
        ghostping = discord.Embed(title=f'GHOSTPING', color=0xFF0000, timestamp=message.created_at, description = "Bắn chết mẹ giờ")
        ghostping.add_field(name='**Tên:**', value=f'{message.author} (<@{message.author.id}>)')
        ghostping.add_field(name='**Tin nhắn:**', value=f'{message.content}')
        ghostping.add_field(name='**Nạn nhân:**', value=victims)
        try:
            await message.channel.send(embed=ghostping)
        except discord.Forbidden:
            try:
                await message.author.send(embed=ghostping)
            except discord.Forbidden:
                return

async def ghostping_detector_on_edit(before, after):
    if (datetime.datetime.now(datetime.timezone.utc) - before.created_at).total_seconds() > config.ghostping_check_time_range:
        return
    if before.author.id in config.ghostping_detector_blacklist_user:
        return
    if len(before.mentions) == 0 or (len(before.mentions) == 1 and (before.mentions[0] == before.author or before.mentions[0].bot)):
        if not before.mention_everyone:
            return
    if before.author.bot: return
    elif (before.mentions != after.mentions) or (before.mention_everyone and after.mention_everyone == False):
        if before.mention_everyone: victims = "@everyone"
        else:
            victims_list = before.mentions.copy()
            for mention in after.mentions:
                if mention in victims_list:
                    victims_list.remove(mention)
            victims = ""
            for victim in victims_list:
                if not victim.bot:
                    victims += f"<@{victim.id}> "
        if victims == "": return
        print(f"{before.author.name} ghostping in {before.guild}!")
        ghostping = discord.Embed(title=f'GHOSTPING', color=0xFF0000, timestamp=after.created_at, description = "Bắn chết mẹ giờ")
        ghostping.add_field(name='**Tên:**', value=f'{before.author} (<@{before.author.id}>)')
        ghostping.add_field(name='**Tin nhắn gốc:**', value=f'{before.content}')
        ghostping.add_field(name='**Tin nhắn đã chỉnh sửa:**', value=f'{after.content}')
        ghostping.add_field(name='**Nạn nhân:**', value=victims)
        try:
            await before.channel.send(embed=ghostping)
        except discord.Forbidden:
            try:
                await before.author.send(embed=ghostping)
            except discord.Forbidden:
                return

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
    if message.guild:
        if config.enable_ghostping_detector and not message.guild.id in config.ghostping_detector_blacklist_guild:
            await ghostping_detector_on_delete(message)

# On message edit event
@client.event
async def on_message_edit(before, after):
    # Ghost ping detector 6900
    if before.guild:
        if config.enable_ghostping_detector and not before.guild.id in config.ghostping_detector_blacklist_guild:
            await ghostping_detector_on_edit(before,after)

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
    
    # If someone use command
    if message.content.startswith(prefix):
        
        # log console
        print(f"{message.author.global_name} at #{message.channel} on {message.guild} : {message.content}")  
        
        # bot user can not use this bot's commands
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send(get_string("bot_use_command_prompt"))
                return
        
        if userid in config.banned_users:
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
                rs = emoji.command_response(client,args[0])
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
                response = gvs.command_response(prefix,userid, message.guild,args)
                if type(response) == discord.Embed:
                    await message.channel.send(embed = response)
                elif type(response) == str:
                    await message.channel.send(response)

            # Invalid command
            case _:
                await message.channel.send(get_string("command_not_found_prompt"))
           
    else:
        if not message.author.bot:
            # gvs
            if "gvs" in message.content.lower():
                gvs.gvs(userid, username, str(message.guild.id))
        
            # Auto react emojis
            for word, emojis in autoreact_emojis.items():
                if word in message.content.lower():
                    for emoji in emojis:
                        try:
                            await message.add_reaction(emoji)
                        except:
                            pass
                    break

client.run(TOKEN)
