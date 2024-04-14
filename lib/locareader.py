"""Read bot's loca file"""
import csv

def string_hash_to_newline(_str):
    _result = ""
    _start = 0
    i = 0
    lc = None

    while i < len(_str):
        c = _str[i]
        if c == "#":
            if lc != "\\":
                _result += _str[_start:i] + "\n"
            else:
                _result += _str[_start:i - 1] + "#"
            _start = i + 1
        lc = c
        i += 1

    return _result + _str[_start:i]

def get_string_list(filepath: str, lang: str) -> list:
    rs = []
    with open(filepath,encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if lang in row:
                _str = string_hash_to_newline(row[lang])
                if _str == "": _str = f"{lang.upper()}_NOT_IMPLEMENTED"
                rs.append(_str)
            else:
                raise ValueError(f"Language '{lang}' does not exist in the row.")
        return rs

def get_string_by_id(filepath: str, id: str, lang: str) -> str:
    with open(filepath,encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["string_id"] == id:
                if lang in row:
                    _str = string_hash_to_newline(row[lang])
                    if _str == "":
                        _str = f"{lang}_{id}_NOT_IMPLEMENTED".upper()
                    return _str
                else:
                    raise ValueError(f"Language '{lang}' does not exist in the row.")

        raise ValueError(f"Can not find that string!, string id: {id}")