import discord
from lib.locareader import get_string_by_id
from lib.sussyconfig import get_config
import requests

config = get_config()

CMD_NAME = "doino"
loca_sheet = f"loca/loca - {CMD_NAME}.csv"

async def slash_command_listener(
        ctx: discord.Interaction, 
        bankname: str, 
        accountnumber: str, 
        accountname: str, 
        amount: int, 
        note: str):
    print(f"{ctx.user} used {CMD_NAME} commands!")
    await ctx.response.defer()
    link = f"https://img.vietqr.io/image/{bankname}-{accountnumber}-print.png?amount={amount}&addInfo={note.replace(" ", "%20")}&accountName={accountname.replace(" ", "%20")}"
    if requests.get(link).content == b'invalid acqId':
        rs = get_string_by_id(loca_sheet, "invalid_bank_name", config.language)
    else:
        rs = link
    await ctx.followup.send(rs)