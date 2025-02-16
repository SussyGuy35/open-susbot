import discord
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import requests
import typing

config = get_config()

CMD_NAME = "doino"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"

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
        rs = get_string_by_id(loca_sheet, "invalid_bank_name", config.language)
    else:
        rs = link
    await ctx.followup.send(rs)