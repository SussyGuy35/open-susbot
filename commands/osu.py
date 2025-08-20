import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_prefix
from lib.sussyconfig import get_config
from ossapi import *
import lib.sussyhelper as ssyhelper

config = get_config()

loca_sheet = "loca/loca - osu.csv"

cmd_names = ['osu', 'o']


ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelpGroup(
        group_name="osu",
        command_type=ssyhelper.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "osu_cmd_desc"),
        usage=get_string_by_id(loca_sheet, "osu_cmd_usage"),
        commands=[
            ssyhelper.CommandHelp(
                command_name="user",
                command_type=ssyhelper.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "osu_user_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "osu_user_cmd_usage"),
                parameters=[
                    ssyhelper.CommandParameterDescription(
                        name="username",
                        description=get_string_by_id(loca_sheet, "osu_user_param_username_desc"),
                        required=True
                    )
                ]
            ),
            ssyhelper.CommandHelp(
                command_name="beatmap",
                command_type=ssyhelper.CommandType.HYBRID,
                description=get_string_by_id(loca_sheet, "osu_beatmap_cmd_desc"),
                usage=get_string_by_id(loca_sheet, "osu_beatmap_cmd_usage"),
                parameters=[
                    ssyhelper.CommandParameterDescription(
                        name="beatmap",
                        description=get_string_by_id(loca_sheet, "osu_beatmap_param_beatmap_desc"),
                        required=True
                    )
                ]
            )
        ],
        aliases=cmd_names[1:]
    ),
    ssyhelper.HelpSection.GENERAL2
)

ossapi_client = Ossapi(config.OSUAPI_CLIENT_ID, config.OSUAPI_CLIENT_SECRET)


# Main function
def command_response(osu_api: Ossapi, prefix: str, command: str):
    # Invalid command handler 6900
    try:
        osu_command = command.split()[0]
    except:
        return get_string_by_id(loca_sheet, "command_help").format(prefix)

    # Subcommand
    match osu_command:

        # User 
        case 'user':
            try:
                user = osu_api.user(command[len(osu_command) + 1:])
                user_most_play_beatmap = osu_api.user_beatmaps(user.id, "most_played")[0]
                user_rank_history = user.rank_history
                user_rank = user_rank_history.data[len(user_rank_history.data) - 1]

                rs = get_string_by_id(loca_sheet, "user_info_template").format(
                    user.id,
                    user.username,
                    user.country.name,
                    user.avatar_url,
                    user_rank,
                    user.rank_highest.rank,
                    int(user.rank_highest.updated_at.timestamp()),
                    get_string_by_id(loca_sheet, "status_online") if user.is_online else get_string_by_id(loca_sheet, "status_offline"),
                    user_most_play_beatmap.beatmapset.title,
                    user_most_play_beatmap._beatmap.version,
                    user_most_play_beatmap.count
                )

                return rs
            except Exception as e:
                return get_string_by_id(loca_sheet, "prompt_error") + "\n" + str(e)

        # Beatmap
        case 'beatmap':
            try:
                beatmap = osu_api.search_beatmapsets(query=command[len(osu_command) + 1:]).beatmapsets[0]
                return f'https://osu.ppy.sh/beatmapsets/{beatmap.id}\n'
            except Exception as e:
                return get_string_by_id(loca_sheet, "prompt_error") + "\n" + str(e)

        case _:
            return get_string_by_id(loca_sheet, "command_help").format(prefix)


async def command_listener(message: discord.Message, usr_input: str):
    prefix = get_prefix(message.guild)
    await message.channel.send(command_response(ossapi_client, prefix, usr_input))


async def slash_command_listener_user(ctx: discord.Interaction, username: str):
    print(f"{ctx.user} used osu user commands!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.defer()
    await ctx.followup.send(command_response(ossapi_client, prefix, "user " + username))


async def slash_command_listener_beatmap(ctx: discord.Interaction, beatmap: str):
    print(f"{ctx.user} used osu beatmap commands!")
    prefix = get_prefix(ctx.guild)
    await ctx.response.defer()
    await ctx.followup.send(command_response(ossapi_client, prefix, "beatmap " + beatmap))
