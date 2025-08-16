import discord
import random
import lib.sussyhelper as sh
import lib.locareader as loca_reader

loca_sheet = "loca/loca - pick.csv"
cmd_names = ['pick', 'choose']

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.PREFIX,
        description=loca_reader.get_string_by_id(loca_sheet, "command_desc"),
        usage=loca_reader.get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="options",
                description=loca_reader.get_string_by_id(loca_sheet, "command_param_options_desc"),
                required=True
            )
        ],
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.GENERAL
)

def command_response(args: list[str], plain_args: str):
    options = []
    if '"' in plain_args:
        options = args
    else:
        if ',' in plain_args:
            options = plain_args.split(',')
        else:
            options = args
    return random.choice(options)


async def command_listener(message: discord.Message, args: list[str], plain_args: str):
    await message.channel.send(command_response(args, plain_args))
