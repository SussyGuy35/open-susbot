import discord
import string
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh
from lib.sussyconfig import get_config

config = get_config()

cmd_names = ["encrypt", "ecr", "enc", "c"]
loca_sheet = "loca/loca - encrypt.csv"

viet_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐđ"
chars = " " + viet_chars + string.punctuation + string.digits + string.ascii_letters + '\n'
chars = list(chars)
key = ['ỵ', '^', 'Ẵ', 'ớ', 'Ờ', 'ệ', 'ụ', 'Ỹ', 'ù', 'ộ', 'Ă', 'P', 'Ủ', 'Õ', 'F', 'Ĩ', 'Ẫ', 'Ổ', 'ỗ', 'Ở', 'G', 'Ả', 'S', 'á', 'ố', '=', 'Ọ', 'Đ', 'ì', 'Ể', 'ể', '"', 'ả', 'Ự', 'v', 'Z', 'ắ', 'J', '!', 'q', 'ử', 'u', 'ò', 'Ỏ', 'm', 'ỳ', 'j', '#', '%', '6', '7', 'Ữ', 'Ụ', 'Ộ', 'B', 'ị', 'i', 'Ẩ', 'ỹ', 'C', 'ỡ', 'r', 'ý', ']', '.', 'í', 'ỏ', 'Q', 'ặ', 'z', '8', 'Ý', 'Ắ', 'Ị', 'ẵ', ')', 'w', 'T', 'b', 'Ễ', 'a', 'ừ', 'Ẹ', 'Ừ', '[','\n' , 'p', 't', 'Ì', 'ạ', 'W', 'ễ', 'f', 'ỉ', 'U', 'n', '$', '1', 'Ú', 'ọ', 'Ẻ', 'R', 'ơ', 'L', 'g', 'ề', 'Ỉ', 'ủ', 'A', 'ấ', 'ô', 'Ẽ', 'H', 'ầ', 'Ứ', 'è', '+', ',', 'Í', 'Ũ', 'ậ', 'ư', ' ', 'D', 'ó', '3', 'Ỷ', 'ằ', 'ợ', 'À', 'Ế', '-', 'l', '\\', 'o', 'ứ', 'd', 'ú', 'Ử', '2', 'I', 'Ệ', '|', 'â', 'È', 'ồ', 'ũ', 'e', 'K', 'Y', 'c', 'Ề', '5', 'ẻ', 'Ỡ', 'k', 'Â', 'Ã', 'É', 'Á', 'Ô', 'Ằ', 'Ặ', 'ê', '*', 'Ầ', 'ẩ', 'ã', "'", 'ữ', 'Ỳ', 'Ấ', '&', '}', ':', '>', 'Ẳ', 'Ỵ', 'O', 'Ò', 'ẽ', '{', '4', 's', 'Ớ', 'Ơ', 'N', 'h', '~', '9', 'õ', 'x', 'Ợ', 'Ạ', 'ờ', 'ẹ', 'ĩ', 'đ', 'y', 'X', 'E', 'Ư', '/', 'Ê', 'ỷ', 'ở', 'ự', 'Ó', '?', 'Ỗ', 'M', '0', 'ă', 'ẫ', 'Ố', '(', 'ổ', 'ẳ', 'Ù', '_', ';', 'Ậ', '@', '`', 'é', 'Ồ', 'V', 'à', '<', 'ế']


sh.HelpManager.add_command_help(
    sh.CommandHelp(
        command_name=cmd_names[0],
        command_type=sh.CommandType.PREFIX,
        description=get_string_by_id(loca_sheet, "command_desc"),
        usage=get_string_by_id(loca_sheet, "command_usage"),
        aliases=cmd_names[1:],
        parameters=[
            sh.CommandParameterDescription(
                name="message",
                description=get_string_by_id(loca_sheet, "command_param_message_desc"),
                required=True
            )
        ]
    ),
    sh.HelpSection.GENERAL2
)


async def delete_message(message: discord.Message):
    try:
        await message.delete()
    except discord.Forbidden:
        print("cannot delete message or sth")
        return
    

def command_response(msg: str):
    cipher_text = ""
    for letter in msg:
        index = chars.index(letter)   
        cipher_text += key[index]      
        cipher_text = cipher_text.replace("@everyone", "`@everyone`").replace("@here", "`@here`")

    return cipher_text


async def command_listener(message: discord.Message, msg: str): 
    await delete_message(message)

    if any(filterletter not in key for filterletter in msg):
        await message.channel.send(get_string_by_id(loca_sheet, "invalid_message"))
    else:
        await message.channel.send(command_response(msg), allowed_mentions=discord.AllowedMentions.none())

 


