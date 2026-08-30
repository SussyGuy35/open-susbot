import asyncio
import discord
import discord.app_commands as app_commands
import requests
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh
import lib.vov_scraper as scraper

loca_sheet = "loca/loca - radio.csv"

cmd_names = ["radio"]

# MARK: Station list
# Each station has a list of URLs tried in order — first one that responds with
# HTTP 2xx is used. This handles servers that are temporarily down (e.g. 502).
STATIONS: dict[str, dict] = {
    "vov1": {
        "name": "VOV1 - Kênh Chính Trị Tổng Hợp",
        "urls": [
            "https://audio-lss.vov.vn/live/vov1.m3u8",
            "https://media-audio.vov.vn/vov1vov5Vietnamese.sdp_aac/playlist.m3u8",
            "https://str.vov.gov.vn/vovlive/vov1vov5Vietnamese.sdp_aac/playlist.m3u8",
        ],
        "emoji": "📻"
    },
    "vov2": {
        "name": "VOV2 - Kênh Văn Hóa và Đời Sống",
        "urls": [
            "https://audio-lss.vov.vn/live/vov2.m3u8",
            "https://media-audio.vov.vn/vov2.sdp_aac/playlist.m3u8",
            "https://str.vov.gov.vn/vovlive/vov2.sdp_aac/playlist.m3u8",
        ],
        "emoji": "🎵"
    },
    "vov3": {
        "name": "VOV3 - Kênh Âm Nhạc Thông Tin Giải Trí",
        "urls": [
            "https://audio-lss.vov.vn/live/vov3.m3u8",
            "https://media-audio.vov.vn/vov3.sdp_aac/playlist.m3u8",
            "https://str.vov.gov.vn/vovlive/vov3.sdp_aac/playlist.m3u8",
        ],
        "emoji": "🎶"
    },
    "vov5": {
        "name": "VOV5 - Hệ Phát Thanh Đối Ngoại",
        "urls": [
            "https://audio-lss.vov.vn/live/vov5.m3u8",
            "https://str.vov.gov.vn/vovlive/vov5.sdp_aac/playlist.m3u8",
        ],
        "emoji": "🌍"
    },
    "vovgt_hn": {
        "name": "VOV Giao Thông Hà Nội",
        "urls": [
            "https://play.vovgiaothong.vn/live/gthn/playlist.m3u8",
        ],
        "emoji": "🚦"
    },
    "vovgt_hcm": {
        "name": "VOV Giao Thông TP. Hồ Chí Minh",
        "urls": [
            "https://play.vovgiaothong.vn/live/gthcm/playlist.m3u8",
        ],
        "emoji": "🛣️"
    }
}

# FFmpeg options for HLS live stream stability
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Slash command dropdown choices — built from STATIONS so it's always in sync
STATION_CHOICES: list[app_commands.Choice[str]] = [
    app_commands.Choice(
        name=f"{station['emoji']} {station['name']}",
        value=key
    )
    for key, station in STATIONS.items()
]

# Schedule only supports specific stations for now
SCHEDULE_SUPPORTED_CHOICES: list[app_commands.Choice[str]] = [
    c for c in STATION_CHOICES if c.value in ["vov3", "vovgt_hn", "vovgt_hcm"]
]

# Track active voice sessions per guild: guild_id -> { voice_client, station_key, active_url }
_active_sessions: dict[int, dict] = {}

# MARK: Help registration
sh.HelpManager.add_command_help(
    sh.CommandHelpGroup(
        group_name="radio",
        command_type=sh.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        commands=[
            sh.CommandHelp(
                command_name="play",
                command_type=sh.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "play_cmd_desc"),
                usage="b!radio play <station> | /radio_play <station>",
                parameters=[
                    sh.CommandParameterDescription(
                        name="station",
                        description=get_string_by_id(loca_sheet, "station_param_desc"),
                        required=True
                    )
                ]
            ),
            sh.CommandHelp(
                command_name="stop",
                command_type=sh.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "stop_cmd_desc"),
                usage="b!radio stop | /radio_stop"
            ),
            sh.CommandHelp(
                command_name="list",
                command_type=sh.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "list_cmd_desc"),
                usage="b!radio list | /radio_list"
            ),
            sh.CommandHelp(
                command_name="status",
                command_type=sh.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "status_cmd_desc"),
                usage="b!radio status | /radio_status"
            ),
            sh.CommandHelp(
                command_name="schedule",
                command_type=sh.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "schedule_cmd_desc"),
                usage="b!radio schedule <station> | /radio_schedule <station>",
                parameters=[
                    sh.CommandParameterDescription(
                        name="station",
                        description=get_string_by_id(loca_sheet, "station_param_desc"),
                        required=True
                    )
                ]
            )
        ]
    ),
    sh.HelpSection.GENERAL
)


# MARK: Helpers

def _get_string(id_: str) -> str:
    return get_string_by_id(loca_sheet, id_)


def _resolve_url(urls: list[str], timeout: int = 5) -> str | None:
    """Try each URL in order and return the first one that responds with HTTP 2xx.
    Runs a lightweight HEAD request — no audio data is downloaded."""
    for url in urls:
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            if resp.status_code < 400:
                return url
        except requests.RequestException:
            continue
    return None


async def _resolve_url_async(urls: list[str]) -> str | None:
    """Async wrapper for _resolve_url so it doesn't block the event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _resolve_url, urls)


def _build_list_embed() -> discord.Embed:
    embed = discord.Embed(
        title=_get_string("list_title"),
        color=discord.Color.blurple()
    )
    for key, station in STATIONS.items():
        embed.add_field(
            name=f"{station['emoji']} `{key}` — {station['name']}",
            value="",
            inline=False
        )
    embed.set_footer(text=_get_string("list_footer"))
    return embed


async def _build_status_embed(guild: discord.Guild) -> discord.Embed:
    embed = discord.Embed(
        title=_get_string("status_title"),
        color=discord.Color.blurple()
    )
    guild_id = guild.id
    
    if guild.voice_client and guild_id in _active_sessions:
        session = _active_sessions[guild_id]
        station_key = session["station_key"]
        station = STATIONS[station_key]
        vc = guild.voice_client
        
        desc = f"{station['emoji']} **{station['name']}**"
        
        # Try fetching schedule to show current program
        if station_key in [c.value for c in SCHEDULE_SUPPORTED_CHOICES]:
            schedule = await scraper.get_schedule(station_key)
            if schedule:
                current_program = scraper.get_current_program(schedule)
                if current_program:
                    desc += f"\n\n**{_get_string('schedule_program_list')}**: {current_program}"
                    
        embed.add_field(
            name=_get_string("status_playing"),
            value=desc,
            inline=False
        )
        embed.add_field(
            name=_get_string("status_channel"),
            value=vc.channel.mention,
            inline=False
        )
    else:
        embed.description = _get_string("status_not_playing")
    return embed


# MARK: Core actions

async def _action_play(
    guild: discord.Guild,
    voice_channel: discord.VoiceChannel,
    station_key: str,
    reply,  # callable(content=str | embed=discord.Embed)
):
    """Play a VOV radio station in the given voice channel.
    Automatically tries fallback URLs if the primary one is unavailable.
    If already playing, switches to the new station instead of returning an error."""
    guild_id = guild.id

    # Validate station
    if station_key not in STATIONS:
        await reply(content=_get_string("invalid_station"))
        return

    station = STATIONS[station_key]
    urls: list[str] = station["urls"]

    # Resolve a working URL (HEAD-checks each candidate, non-blocking)
    print(f"[radio] Resolving stream URL for {station_key}...")
    active_url = await _resolve_url_async(urls)

    if active_url is None:
        await reply(content=_get_string("stream_unavailable"))
        print(f"[radio] All URLs for {station_key} are unavailable: {urls}")
        return

    print(f"[radio] Using URL: {active_url}")

    # Get or create VoiceClient robustly
    voice_client: discord.VoiceClient = guild.voice_client

    if voice_client is not None:
        if not voice_client.is_connected():
            # Stale connection (e.g. kicked from channel but state wasn't cleared)
            await voice_client.disconnect(force=True)
            voice_client = None

    if voice_client is None:
        # Case: Not playing -> connect and start
        try:
            voice_client = await voice_channel.connect(timeout=10.0, reconnect=True)
        except Exception as e:
            print(f"[radio] Failed to connect to voice channel: {e}")
            await reply(content=_get_string("connect_error"))
            return
    else:
        # Case: Already playing -> switch station
        if voice_client.channel != voice_channel:
            try:
                await voice_client.move_to(voice_channel)
            except Exception as e:
                print(f"[radio] Failed to move to voice channel: {e}")
                await reply(content=_get_string("connect_error"))
                return
        # Stop current stream to prepare for new one
        voice_client.stop()

    def after_play(error):
        print(f"[radio] Stream ended ({station_key}): {error}" if error else f"[radio] Stream ended ({station_key})")
        # Optional: cleanup _active_sessions if we want, but we rely on guild.voice_client now
        if guild_id in _active_sessions and _active_sessions[guild_id].get("station_key") == station_key:
            # We don't delete the session here because the stream might end during a switch,
            # but if it genuinely stops and voice_client.is_playing() is false, we could clean up.
            pass

    try:
        # Try FFmpegOpusAudio first for lower CPU, fallback to FFmpegPCMAudio
        try:
            source = discord.FFmpegOpusAudio(active_url, **FFMPEG_OPTIONS)
        except Exception:
            source = discord.FFmpegPCMAudio(active_url, **FFMPEG_OPTIONS)
            
        voice_client.play(source, after=after_play)
    except discord.ClientException as e:
        print(f"[radio] ClientException playing audio: {e}")
        await reply(content=_get_string("stream_unavailable"))
        return

    _active_sessions[guild_id] = {
        "voice_client": voice_client,
        "station_key": station_key,
        "active_url": active_url
    }

    await reply(content=_get_string("now_playing").format(station["name"]))


async def _action_stop(guild: discord.Guild, reply):
    """Stop radio and disconnect from voice channel."""
    guild_id = guild.id
    
    voice_client = guild.voice_client

    if voice_client is None:
        if guild_id in _active_sessions:
            del _active_sessions[guild_id]
        await reply(content=_get_string("not_playing"))
        return

    await voice_client.disconnect(force=True)
    if guild_id in _active_sessions:
        del _active_sessions[guild_id]

    await reply(content=_get_string("stopped"))


async def _action_list(reply):
    """Send the list of available stations."""
    await reply(embed=_build_list_embed())


async def _action_status(guild: discord.Guild, reply):
    """Send the current playback status."""
    await reply(embed=await _build_status_embed(guild))


async def _build_schedule_embed(station_key: str, schedule: list[tuple[str, str]]) -> discord.Embed:
    station_name = STATIONS[station_key]["name"]
    embed = discord.Embed(
        title=f"{_get_string('schedule_title')} - {station_name}",
        color=discord.Color.blue()
    )
    
    # Discord embed fields have a max length of 1024 chars
    # We will combine schedule items into chunks
    chunks = []
    current_chunk = ""
    for time_str, program_str in schedule:
        line = f"**{time_str}** - {program_str}\n"
        if len(current_chunk) + len(line) > 1000:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += line
            
    if current_chunk:
        chunks.append(current_chunk)
        
    for i, chunk in enumerate(chunks):
        field_name = _get_string("schedule_program_list") if i == 0 else "\u200b"
        embed.add_field(name=field_name, value=chunk, inline=False)
        
    return embed

async def _action_schedule(reply, station_key: str):
    """Fetch and send the broadcast schedule for a station."""
    if station_key not in [c.value for c in SCHEDULE_SUPPORTED_CHOICES]:
        await reply(content=_get_string("schedule_unsupported").format(STATIONS.get(station_key, {}).get("name", station_key)))
        return
        
    schedule_data = await scraper.get_schedule(station_key)
    if not schedule_data:
        await reply(content=_get_string("scraping_error"))
        return
        
    embed = await _build_schedule_embed(station_key, schedule_data)
    await reply(embed=embed)


# MARK: Prefix command listener

async def command_listener(message: discord.Message, args: list[str]):
    if not message.guild:
        return

    async def reply(**kwargs):
        await message.channel.send(**kwargs)

    if not args:
        await reply(embed=_build_list_embed())
        return

    subcommand = args[0].lower()

    if subcommand == "play":
        if len(args) < 2:
            await reply(content=_get_string("invalid_station"))
            return
        if not message.author.voice or not message.author.voice.channel:
            await reply(content=_get_string("not_in_voice"))
            return
        station_key = args[1].lower()
        await _action_play(message.guild, message.author.voice.channel, station_key, reply)

    elif subcommand == "stop":
        await _action_stop(message.guild, reply)

    elif subcommand == "list":
        await _action_list(reply)

    elif subcommand == "status":
        await _action_status(message.guild, reply)

    elif subcommand == "schedule":
        if len(args) < 2:
            await reply(content=_get_string("invalid_station"))
            return
        station_key = args[1].lower()
        await _action_schedule(reply, station_key)

    else:
        await reply(content=_get_string("invalid_station"))


# MARK: Slash command listeners

async def slash_play(ctx: discord.Interaction, station: str):
    await ctx.response.defer()
    print(f"{ctx.user} used /radio_play {station}")

    async def reply(**kwargs):
        await ctx.followup.send(**kwargs)

    if not ctx.user.voice or not ctx.user.voice.channel:  # type: ignore
        await reply(content=_get_string("not_in_voice"))
        return

    await _action_play(ctx.guild, ctx.user.voice.channel, station.lower(), reply)  # type: ignore


async def slash_stop(ctx: discord.Interaction):
    await ctx.response.defer()
    print(f"{ctx.user} used /radio_stop")

    async def reply(**kwargs):
        await ctx.followup.send(**kwargs)

    await _action_stop(ctx.guild, reply)  # type: ignore


async def slash_list(ctx: discord.Interaction):
    await ctx.response.defer()
    print(f"{ctx.user} used /radio_list")
    await ctx.followup.send(embed=_build_list_embed())


async def slash_status(ctx: discord.Interaction):
    await ctx.response.defer()
    print(f"{ctx.user} used /radio_status")
    embed = await _build_status_embed(ctx.guild)  # type: ignore
    await ctx.followup.send(embed=embed)

async def slash_schedule(ctx: discord.Interaction, station: str):
    await ctx.response.defer()
    print(f"{ctx.user} used /radio_schedule {station}")

    async def reply(**kwargs):
        await ctx.followup.send(**kwargs)

    await _action_schedule(reply, station.lower())
