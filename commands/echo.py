import discord
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh

loca_sheet = "loca/loca - echo.csv"

cmd_names = ['echo', 'say', 't']

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name="echo",
        command_type=sh.CommandType.PREFIX,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="message",
                description=get_string_by_id(loca_sheet, "command_param_message_desc"),
                required=True
            )
        ],
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.CORE
)


async def delete_message(message: discord.Message):
    try:
        await message.delete()
    except discord.Forbidden:
        print("cannot delete message or sth")
        return


def command_response(msg: str):
    new_msg = msg
    new_msg = new_msg.replace("@everyone", "`@everyone`").replace("@here", "`@here`")
    return new_msg


async def command_listener(message: discord.Message, msg: str):
    await delete_message(message)

    if message.reference is None:
        await message.channel.send(command_response(msg), allowed_mentions=discord.AllowedMentions.none())
    else:
        if message.reference.cached_message is None:
            original_message = await message.channel.fetch_message(message.reference.message_id)
        else:
            original_message = message.reference.cached_message
        await original_message.reply(command_response(msg), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
