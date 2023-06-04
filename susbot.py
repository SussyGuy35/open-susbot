import commands
import config, discord, os

prefix = config.prefix
bot_version = config.bot_version

TOKEN = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# j4f
emojis = ["🇬","🇰","🇪","🇻","🇦","🇾","🇸","🅰️","🇴","😳"]
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Streaming(name = 'My creator hates me',url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    print(f'open-susbot v{bot_version}')
    print(f'Logged in as {client.user}. Currently on {str(len(client.guilds))} server(s)!')
    print("List of current joined server(s):")
    for guild in client.guilds:
        print(guild)

@client.event
async def on_message(message):
    global date, cardgame_data, cardshop_data
    if message.author == client.user:
        print(">Bot:",message.content)
        return   
    if "gvs" in message.content.lower():
        # it's-a-me, BachNob
        for emoji in emojis:
            await message.add_reaction(emoji)
    if message.content.startswith(prefix):
        print(f"{message.author} at {message.channel} channel: {message.content}")  
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send("Bot mà đòi dùng lệnh của bot à 🐧")
                return
        command = message.content.split()[0].replace(prefix,'')
        match command:
            case 'debug':
                await message.channel.send(f"userid: {message.author.id}")
            case 'help':
                await message.channel.send(commands.help.command_response())
            case 'ping':
                await message.channel.send(commands.ping.command_response())
            case 'echo':
                await message.channel.send(commands.echo.command_response(message.content))
            case 'pick':
                await message.channel.send(commands.pick.command_response(message.content))  
            case 'randcaps':
                await message.channel.send(commands.randcaps.command_response(message.content))  
            case 'gacha':
                userid = str(message.author.id)
                username = message.author.name
                command_response = commands.gacha.command_response(message.content,prefix,userid,username)
                user_level_up_response = commands.gacha.check_if_user_level_up(userid,username)
                if command_response != None:
                    await message.channel.send(command_response)
                if user_level_up_response != None:
                    await message.channel.send(user_level_up_response)
                commands.gacha.save()    
            case 'osu':
                await message.channel.send(commands.osu.command_response(message.content))
            case _:
                await message.channel.send("Lệnh đó không tồn tại!")
        
client.run(TOKEN)