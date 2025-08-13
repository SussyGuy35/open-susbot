import discord
from lib.locareader import get_string_by_id
from lib.sussyutils import get_emoji_id_from_snowflake
import lib.sussyhelper as ssyhelper

loca_sheet = "loca/loca - emoji.csv"

cmd_names = ['emoji', 'e']

ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelp(
        command_name="emoji",
        command_type=ssyhelper.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            ssyhelper.CommandParameterDescription(
                name="emoji",
                description=get_string_by_id(loca_sheet, "command_param_emoji_desc"),
                required=True
            )
        ],
        aliases=cmd_names[1:]
    ),
    ssyhelper.HelpSection.GENERAL
)


def command_response(client: discord.Client, emoji: str):
    try:
        emoji_to_get = client.get_emoji(get_emoji_id_from_snowflake(emoji))
    except:
        print(f"ERROR: Failed to get emoji. Message: {emoji}")
        emoji_to_get = None

    if emoji_to_get is not None:
        embed = discord.Embed(
            title=emoji_to_get.name,
            description=get_string_by_id(loca_sheet, "embed_desc").format(
                int(emoji_to_get.created_at.timestamp())
            ),
            color=0x03e3fc
        )
        embed.set_image(url=emoji_to_get.url)
        return embed
    else:
        return get_string_by_id(loca_sheet, "prompt_exception")


async def command_listener(message: discord.Message, bot: discord.Client, args: list):
    if not args:
        await message.channel.send(get_string_by_id(loca_sheet, "prompt_exception"))
    rs = command_response(bot, args[0])
    if isinstance(rs, str):
        await message.channel.send(rs)
    else:
        await message.channel.send(embed=rs)


async def slash_command_listener(client: discord.Client, ctx: discord.Interaction, emoji: str):
    print(f"{ctx.user} used emoji commands!")
    await ctx.response.defer()
    rs = command_response(client, emoji)
    if isinstance(rs, str):
        await ctx.followup.send(rs)
    else:
        await ctx.followup.send(embed=rs)
