import discord
import random
import lib.sussyhelper as sh
import lib.locareader as loca_reader

loca_sheet = "loca/loca - randcaps.csv"

cmd_names = ['randcaps', 'rc']

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.PREFIX,
        description=loca_reader.get_string_by_id(loca_sheet, "command_desc"),
        usage=loca_reader.get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="text",
                description=loca_reader.get_string_by_id(loca_sheet, "command_param_text_desc"),
                required=True
            )
        ],
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.FUN
)

def command_response(user_input: str):
    message_output = []
    for i in range(len(user_input)):
        char = user_input[i]
        char = [char.lower(), char.upper()]
        message_output.append(random.choice(char))
    return ''.join(message_output)


async def command_listener(message: discord.Message, usr_input: str):
    await message.channel.send(command_response(usr_input))
