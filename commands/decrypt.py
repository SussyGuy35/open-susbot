import discord
import random
import string
from lib.locareader import get_string_by_id
import lib.sussyhelper as sh
from lib.sussyconfig import get_config

config = get_config()

cmd_names = ["decrypt", "dcr", "dc", "d"]
loca_sheet = "loca/loca - decrypt.csv"

viet_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐđ"
chars = " " + viet_chars + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = ['ỵ', '^', 'Ẵ', 'ớ', 'Ờ', 'ệ', 'ụ', 'Ỹ', 'ù', 'ộ', 'Ă', 'P', 'Ủ', 'Õ', 'F', 'Ĩ', 'Ẫ', 'Ổ', 'ỗ', 'Ở', 'G', 'Ả', 'S', 'á', 'ố', '=', 'Ọ', 'Đ', 'ì', 'Ể', 'ể', '"', 'ả', 'Ự', 'v', 'Z', 'ắ', 'J', '!', 'q', 'ử', 'u', 'ò', 'Ỏ', 'm', 'ỳ', 'j', '#', '%', '6', '7', 'Ữ', 'Ụ', 'Ộ', 'B', 'ị', 'i', 'Ẩ', 'ỹ', 'C', 'ỡ', 'r', 'ý', ']', '.', 'í', 'ỏ', 'Q', 'ặ', 'z', '8', 'Ý', 'Ắ', 'Ị', 'ẵ', ')', 'w', 'T', 'b', 'Ễ', 'a', 'ừ', 'Ẹ', 'Ừ', '[', 'p', 't', 'Ì', 'ạ', 'W', 'ễ', 'f', 'ỉ', 'U', 'n', '$', '1', 'Ú', 'ọ', 'Ẻ', 'R', 'ơ', 'L', 'g', 'ề', 'Ỉ', 'ủ', 'A', 'ấ', 'ô', 'Ẽ', 'H', 'ầ', 'Ứ', 'è', '+', ',', 'Í', 'Ũ', 'ậ', 'ư', ' ', 'D', 'ó', '3', 'Ỷ', 'ằ', 'ợ', 'À', 'Ế', '-', 'l', '\\', 'o', 'ứ', 'd', 'ú', 'Ử', '2', 'I', 'Ệ', '|', 'â', 'È', 'ồ', 'ũ', 'e', 'K', 'Y', 'c', 'Ề', '5', 'ẻ', 'Ỡ', 'k', 'Â', 'Ã', 'É', 'Á', 'Ô', 'Ằ', 'Ặ', 'ê', '*', 'Ầ', 'ẩ', 'ã', "'", 'ữ', 'Ỳ', 'Ấ', '&', '}', ':', '>', 'Ẳ', 'Ỵ', 'O', 'Ò', 'ẽ', '{', '4', 's', 'Ớ', 'Ơ', 'N', 'h', '~', '9', 'õ', 'x', 'Ợ', 'Ạ', 'ờ', 'ẹ', 'ĩ', 'đ', 'y', 'X', 'E', 'Ư', '/', 'Ê', 'ỷ', 'ở', 'ự', 'Ó', '?', 'Ỗ', 'M', '0', 'ă', 'ẫ', 'Ố', '(', 'ổ', 'ẳ', 'Ù', '_', ';', 'Ậ', '@', '`', 'é', 'Ồ', 'V', 'à', '<', 'ế']



    

def command_response(msg: str):
    decipher_text = ""
    for letter in msg:
        index = chars.index(letter)   
        decipher_text += key[index]      
        decipher_text = decipher_text.replace("@everyone", "`@everyone`").replace("@here", "`@here`")

    return decipher_text

async def command_listener(message: discord.Message, msg: str): 
    
    await message.channel.send(command_response(msg))


