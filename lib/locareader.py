"""Read bot's loca file"""
import csv
from lib.sussyutils import string_hash_to_newline


def get_string_list(filepath: str, lang: str) -> list:
    rs = []
    with open(filepath, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if lang in row:
                _str = string_hash_to_newline(row[lang])
                if _str == "":
                    _str = f"{lang.upper()}_NOT_IMPLEMENTED"
                rs.append(_str)
            else:
                raise ValueError(f"Language '{lang}' does not exist in the row.")
        return rs


def get_string_by_id(filepath: str, id_: str, lang: str) -> str:
    with open(filepath, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["string_id"] == id_:
                if lang in row:
                    _str = string_hash_to_newline(row[lang])
                    if _str == "":
                        _str = f"{lang}_{id_}_NOT_IMPLEMENTED".upper()
                    return _str
                else:
                    raise ValueError(f"Language '{lang}' does not exist in the row.")

        raise ValueError(f"Can not find that string!, string id: {id_}")
