import discord
import re
import requests
import lib.sussyconfig
from lib.sussyutils import get_prefix

config =  lib.sussyconfig.get_config()

bank_names = [
    "ICB",
    "VietinBank",
    "VCB",
    "Vietcombank",
    "BIDV",
    "VBA",
    "Agribank",
    "OCB",
    "MB",
    "MBBank",
    "TCB",
    "Techcombank",
    "ACB",
    "VPB",
    "VPBank",
    "TPB",
    "TPBank",
    "STB",
    "Sacombank",
    "HDB",
    "HDBank",
    "VCCB",
    "VietCapitalBank",
    "SCB",
    "VIB",
    "SHB",
    "EIB",
    "Eximbank",
    "MSB",
    "CAKE",
    "UBank",
    "Timo",
    "VTLMoney",
    "ViettelMoney",
    "VNPTMoney",
    "VNPT",
    "SGICB",
    "SaigonBank",
    "BAB",
    "BacABank",
    "PVCB",
    "PVcomBank",
    "Oceanbank",
    "NCB",
    "SHBVN",
    "ShinhanBank",
    "ABB",
    "ABBANK",
    "VAB",
    "VietABank",
    "NAB",
    "NamABank",
    "PGB",
    "PGBank",
    "VietBank",
    "BVB",
    "BaoVietBank",
    "SEAB",
    "SeABank",
    "COOPBANK",
    "LPB",
    "LienVietPostBank",
    "KLB",
    "KienLongBank",
    "KBank",
    "KBHN",
    "KookminHN",
    "KEBHANAHCM",
    "KEBHANAHN",
    "MAFC",
    "Citibank",
    "KBHCM",
    "KookminHCM",
    "VBSP",
    "WVN",
    "Woori",
    "VRB",
    "UOB",
    "UnitedOverseas",
    "SCVN",
    "StandardChartered",
    "PBVN",
    "PublicBank",
    "IVB",
    "IndovinaBank",
    "HSBC",
    "HLBVN",
    "HongLeong",
    "GPB",
    "GPBank",
    "DOB",
    "DongABank",
    "DBS",
    "DBSBank",
    "CIMB",
    "CBB",
    "CBBank"
]


async def check_auto_qr(message: discord.Message):
    if message.author.bot:
        return
    if message.content.startswith(get_prefix(message.guild)):
        return
    
    content = message.content.lower()

    stk_match = re.search(r'\b\d{6,19}\b', content)
    stk = stk_match.group() if stk_match else None

    if not stk:
        return

    words = content.split()

    bankname = None
    for word in words:
        for bank in bank_names:
            if word == bank.lower():
                bankname = bank
                break
    
    if not bankname:
        return
    
    link = f"https://img.vietqr.io/image/{bankname}-{stk}-print.png?"
    if requests.get(link).content == b'invalid acqId':
        return

    await message.add_reaction("🆗")
    await message.channel.send(link)