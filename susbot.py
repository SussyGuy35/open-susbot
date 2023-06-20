import commands
import discord, os

try:
    import config_override as config
except:
    import config

# Config
prefix = config.prefix
bot_version = config.bot_version

TOKEN = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

# j4f
emojis = ["🇬","🇰","🇪","🇻","🇦","🇾","🇸","🅰️","🇴","😳"]

# Slash command
@tree.command(name = "ping", description = "Ping pong ping pong") 
async def ping(interaction):
    await interaction.response.send_message('pong! <:njnk:1094916486029639710>')

# On ready event
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity = discord.Streaming(name = 'My creator hates me',url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    print(f'open-susbot v{bot_version}')
    print(f'Logged in as {client.user}. Currently on {str(len(client.guilds))} server(s)!')
    print("List of current joined server(s):")
    for guild in client.guilds:
        print(guild)

# On message event
@client.event
async def on_message(message):
    global date, cardgame_data, cardshop_data
    
    # log console
    if message.author == client.user:
        print(">Bot:",message.content)
        return   
    
    # Auto react when someone say "gvs"
    if "gvs" in message.content.lower():
        for emoji in emojis:
            await message.add_reaction(emoji)
    
    # If someone use command
    if message.content.startswith(prefix):
        
        # log console
        print(f"{message.author.global_name} at #{message.channel} on {message.guild} : {message.content}")  
        
        # bot user can not use this bot's command
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send("Bot mà đòi dùng lệnh của bot à 🐧")
                return
        
        # Get requested command
        command = message.content.split()[0].replace(prefix,'')
        
        # Main thing
        match command:
            
            # Debug
            case 'debug':
                await message.channel.send(f"userid: {message.author.id}")
            
            # Help
            case 'help':
                await message.channel.send(commands.help.command_response())
            
            # Ping pong ping pong
            case 'ping':
                await message.channel.send(commands.ping.command_response())

            # Echo
            case 'echo':
                await message.channel.send(commands.echo.command_response(message.content))
            
            # Pick
            case 'pick':
                await message.channel.send(commands.pick.command_response(message.content))  
            
            # Random caps
            case 'randcaps':
                await message.channel.send(commands.randcaps.command_response(message.content))  
            
            # Gacha
            case 'gacha':
                userid = str(message.author.id)
                username = message.author.global_name
                command_response = commands.gacha.command_response(message.content,prefix,userid,username)
                user_level_up_response = commands.gacha.check_if_user_level_up(userid,username)
                if command_response != None:
                    await message.channel.send(command_response)
                if user_level_up_response != None:
                    await message.channel.send(user_level_up_response)
                commands.gacha.save()    
            
            # osu!
            case 'osu':
                await message.channel.send(commands.osu.command_response(message.content))
            
            # Invalid command
            case _:
                await message.channel.send("Lệnh đó không tồn tại!")
        
client.run(TOKEN)