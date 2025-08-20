import discord
from lib.locareader import get_string_list, get_string_by_id
import random
import lib.sussyhelper as sh

answer_sheet = "loca/loca - ask-sheet.csv"
loca_sheet = "loca/loca - ask.csv"

cmd_names = ['ask', 'question']

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.PREFIX,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="question",
                description=get_string_by_id(loca_sheet, "command_param_question_desc"),
                required=True
            )
        ],
        aliases=cmd_names[1:]
    ),
    sh.HelpSection.FUN
)

ans = get_string_list(answer_sheet)


def command_response(question: str):
    if question == '':
        return get_string_by_id(loca_sheet, "no_question")
    else:
        return random.choice(ans)


async def command_listener(message: discord.Message, usr_input: str):
    await message.channel.send(command_response(usr_input))
