import discord
from lib.locareader import get_string_by_id
import requests
import typing
import lib.sussyhelper as sh

CMD_NAME = "doino"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"

sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=CMD_NAME,
        command_type=sh.CommandType.SLASH,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        parameters=[
            sh.CommandParameterDescription(
                name="bankname",
                description=get_string_by_id(loca_sheet, "command_param_bankname_desc"),
                required=True
            ),
            sh.CommandParameterDescription(
                name="accountnumber",
                description=get_string_by_id(loca_sheet, "command_param_accountnumber_desc"),
                required=True
            ),
            sh.CommandParameterDescription(
                name="accountname",
                description=get_string_by_id(loca_sheet, "command_param_accountname_desc"),
                required=False
            ),
            sh.CommandParameterDescription(
                name="amount",
                description=get_string_by_id(loca_sheet, "command_param_amount_desc"),
                required=False
            ),
            sh.CommandParameterDescription(
                name="note",
                description=get_string_by_id(loca_sheet, "command_param_note_desc"),
                required=False
            )
        ]
    ),
    sh.HelpSection.GENERAL
)

bank_names = typing.Literal[
    "ACB", 
    "Agribank", 
    "BIDV", 
    "BacABank", 
    "CAKE", 
    "COOPBANK",
    "Eximbank", 
    "HDBank", 
    "LienVietPostBank",
    "MBBank",
    "OCB",
    "Oceanbank",
    "Sacombank",
    "SaigonBank",
    "ShinhanBank",
    "TPBank",
    "Techcombank",
    "Timo",
    "VIB",
    "VNPTMoney",
    "VPBank",
    "VietCapitalBank",
    "Vietcombank",
    "VietinBank",
    "ViettelMoney"
]

async def slash_command_listener(
        ctx: discord.Interaction, 
        bankname: bank_names, 
        accountnumber: str, 
        accountname: str | None = None, 
        amount: int | None = None, 
        note: str | None = None):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer()
    
    link = f"https://img.vietqr.io/image/{bankname}-{accountnumber}-print.png?"
    if amount:
        link += f'amount={amount}&'
    if note:
        link += f'addInfo={note.replace(" ", "%20")}&'
    if accountname:
        link += f'accountName={accountname.replace(" ", "%20")}&'

    if requests.get(link).content == b'invalid acqId':
        rs = get_string_by_id(loca_sheet, "invalid_bank_name")
    else:
        rs = link
    await ctx.followup.send(rs)