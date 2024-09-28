import discord
import discord.app_commands as app_commands
from lib.sussyconfig import get_config
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix, parse_command

# import commands
from commands import (
    amogus, ask, creategif, echo, emoji as getemoji,
    gvs, help as bot_help, nijika, osu, pick,
    ping, randcaps, randcat, randwaifu, getprefix,
    avatar, bean, feedback, khoa, doino, clear,
    gacha, reactionroles, nijipray
)

# import features
import features.onready_things
import features.ghostping_detector
import features.auto_react_emoji
import features.gvscount
import features.on_bot_mentioned
import features.reaction_roles

config = get_config()

# Config
bot_version = config.bot_version

TOKEN = config.TOKEN

print(f'{config.bot_name} v{bot_version}')

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

autoreact_emojis = config.autoreact_emojis


# loca thing
def get_string(id_: str, loca: str = "main"):
    return get_string_by_id(f"loca/loca - {loca}.csv", id_, config.language)


# --- Slash command ---

@tree.command(name="feedback", description=get_string("command_feedback_desc"))
async def send_feedback(ctx: discord.Interaction):
    await feedback.slash_command_listener(ctx)


@tree.command(name="help", description=get_string("command_help_desc"))
async def get_help(ctx: discord.Interaction):
    await bot_help.slash_command_listener(ctx)


@tree.command(name="ping", description=get_string("command_ping_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def pingpong(ctx: discord.Interaction):
    await ping.slash_command_listener(ctx, client)


@tree.command(name="avatar", description=get_string("command_avatar_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_avatar(ctx: discord.Interaction, user: discord.User, server_avatar: bool = True):
    await avatar.slash_command_listener(ctx, user, server_avatar)


@tree.command(name="emoji", description=get_string("command_emoji_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_emoji(ctx: discord.Interaction, emoji: str):
    await getemoji.slash_command_listener(client, ctx, emoji)


@tree.command(name="nijika", description=get_string("command_nijika_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_nijika_image(ctx: discord.Interaction):
    await nijika.slash_command_listener(ctx)

@tree.command(name="khoabug", description=get_string("command_khoabug_desc"))
async def get_khoabug(ctx: discord.Interaction, search: str = None):
    await khoa.slash_command_listener(ctx, search)

@tree.command(name="khoalist", description=get_string("command_khoalist_desc"))
async def get_khoalist(ctx: discord.Interaction):
    await khoa.slash_command_listener_list(ctx)

@tree.command(name="amogus", description=get_string("command_amogus_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_amogus_image(ctx: discord.Interaction):
    await amogus.slash_command_listener(ctx)


@tree.command(name="osu_user", description=get_string("command_osu_user_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def osu_user(ctx: discord.Interaction, username: str):
    await osu.slash_command_listener_user(ctx, username)


@tree.command(name="osu_beatmap", description=get_string("command_osu_beatmap_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def osu_beatmap(ctx: discord.Interaction, beatmap: str):
    await osu.slash_command_listener_beatmap(ctx, beatmap)


@tree.command(name="gvs_count", description=get_string("command_gvs_count_desc"))
async def gvs_count(ctx: discord.Interaction, user: discord.User | None = None):
    await gvs.slash_command_listener_count(ctx, user)


@tree.command(name="gvs_leaderboard", description=get_string("command_gvs_leaderboard_desc"))
async def gvs_lb(ctx: discord.Interaction):
    await gvs.slash_command_listener_lb(ctx)


@tree.command(name="gvs_react", description=get_string("command_gvs_react_desc"))
async def gvs_react(ctx: discord.Interaction, message_id: str | None = None):
    await gvs.slash_command_listener_react_message(ctx, message_id)


@tree.command(name="randcat", description=get_string("command_randcat_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_randcat(ctx: discord.Interaction, is_cat_girl: bool = False):
    await randcat.slash_command_listener(ctx, is_cat_girl)


@tree.command(name="randwaifu", description=get_string("command_randwaifu_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_randwaifu(ctx: discord.Interaction):
    await randwaifu.slash_command_listener(ctx)


@tree.command(name="create_gif", description=get_string("command_create_gif_desc"))
async def create_gif(ctx: discord.Interaction, file: discord.Attachment):
    await creategif.slash_command_listener(ctx, file)


@tree.command(name="bean", description=get_string("embed_desc", "bean"))
async def bean_user(ctx: discord.Interaction, user: discord.User, reason: str):
    await bean.slash_command_listener(ctx, user, reason)


@tree.command(name="get_prefix", description=get_string("command_getprefix_desc"))
async def get_bot_prefix(ctx: discord.Interaction):
    await getprefix.slash_command_listener(ctx)


@tree.command(name="doino", description=get_string("command_doino_desc"))
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_vietqr(
        ctx: discord.Interaction,
        bankname: doino.bank_names,
        accountnumber: str,
        accountname: str | None = None,
        amount: int | None = None,
        note: str | None = None):
    await doino.slash_command_listener(ctx, bankname, accountnumber, accountname, amount, note)


@tree.command(name="clear", description=get_string("command_clear_desc"))
async def clear_messages(ctx: discord.Interaction, number: int):
    await clear.slash_command_listener(ctx, number)


@tree.command(name="send_reaction_roles_message", description=get_string("command_reaction_roles_desc"))
async def send_reaction_roles_message(
        ctx: discord.Interaction,
        prompt_message: str,
        role1: discord.Role,
        emoji1: str,
        role2: discord.Role | None,
        emoji2: str | None,
        role3: discord.Role | None,
        emoji3: str | None,
        role4: discord.Role | None,
        emoji4: str | None,
        role5: discord.Role | None,
        emoji5: str | None,
):
    await reactionroles.slash_command_listener(
        ctx, prompt_message, role1, emoji1, role2, emoji2, role3, emoji3, role4, emoji4, role5, emoji5
    )


# On ready event
@client.event
async def on_ready():
    # tree.clear_commands(guild = None) # Uncomment this to clear all commands
    await tree.sync()
    await features.onready_things.on_ready(client)


# On message delete event
@client.event
async def on_message_delete(message: discord.Message):
    await features.ghostping_detector.on_delete(message)


# On message edit event
@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    await features.ghostping_detector.on_edit(before, after)


# On raw reaction add event
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await features.reaction_roles.reaction_roles_on_raw_reaction_add_and_remove(payload, client)


# On raw reaction remove event
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    await features.reaction_roles.reaction_roles_on_raw_reaction_add_and_remove(payload, client)


# On message event
@client.event
async def on_message(message: discord.Message):
    # log console
    if message.author == client.user:
        print(">Bot:", message.content, "\n")
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
        command = message.content.split()[0].replace(prefix, '')

        plain_args = message.content[len(prefix + command) + 1:]
        args = parse_command(plain_args)

        # Main thing
        match command:

            case 'debug':
                await message.channel.send(
                    f"user_id: {message.author.id}, channel_id: {message.channel.id}, guild: {message.guild}")

            case 'getloca':
                await message.channel.send(get_string_by_id(f"loca/loca - {args[0]}.csv", args[1], args[2]))

            case 'help':
                await bot_help.command_listener(message)

            case 'ping':
                await ping.command_listener(message, client)

            case 'echo':
                await echo.command_listener(message, plain_args)

            case 'pick':
                await pick.command_listener(message, args, plain_args)

            case 'randcaps':
                await randcaps.command_listener(message, plain_args)

            case 'osu':
                await osu.command_listener(message, plain_args)

            case 'emoji':
                await getemoji.command_listener(message, client, args)

            case 'ask':
                await ask.command_listener(message, plain_args)

            case 'nijika':
                await nijika.command_listener(message)

            case 'amogus':
                await amogus.command_listener(message)

            case 'gvs':
                await gvs.command_listener(message, args)
            
            case 'gacha':
                await gacha.command_listener(message, args, client)
            
            case 'nijipray':
                await nijipray.command_listener(message, client, args)

            # Invalid command
            case _:
                await message.channel.send(get_string("command_not_found_prompt"))

    else:
        await features.on_bot_mentioned.reply(client, message)
        await features.gvscount.gvs(message, userid)
        await features.auto_react_emoji.react(autoreact_emojis, message)


client.run(TOKEN)
