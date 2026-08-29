from datetime import datetime
import pytz

def parse_time(time_str):
    # e.g., "07h30-09h15" or "21h00- 22h00" or "05h00 - 06h00"
    time_str = time_str.replace(" ", "")
    if "-" not in time_str:
        return None, None
    start_str, end_str = time_str.split("-")
    
    def to_minutes(t_str):
        # handle "07h30" or "07:30"
        t_str = t_str.replace(":", "h")
        if "h" not in t_str: return 0
        h, m = t_str.split("h")
        return int(h) * 60 + int(m)
        
    return to_minutes(start_str), to_minutes(end_str)

tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime.now(tz)
current_mins = now.hour * 60 + now.minute

print("Current:", f"{now.hour}h{now.minute}", current_mins)
print(parse_time("07h30-09h15"))
print(parse_time("21h00- 22h00"))
print(parse_time("23h00-24h00"))
