# Code by LeiZanTheng
import random
common = 0
uncommon = 0
rare = 0
epic = 0
legendary = 0
def roll(s_percent,a_percent,b_percent,c_percent,d_percent):
    curPer = random.randint(1,100)
    print(curPer)
    if curPer <= d_percent:
        print("common")
        return "common"
    elif curPer <= d_percent + c_percent:
        print("Uncommon")
        return "Uncommon"
    elif curPer <= d_percent + c_percent + b_percent:
        print("Rare")
        return "Rare"
    elif curPer <= 100 - s_percent:
        print("ePIC")
        return "ePIC"
    else:
        print("Legendary")
        return "Legendary"
for i in range(200):
    match roll(2,5,8,20,65):
        case "common":
            common += 1
        case "Uncommon":
            uncommon += 1
        case "Rare":
            rare += 1
        case "ePIC":
            epic += 1
        case "Legendary":
            legendary += 1
print("common:", common,"Uncommon:" , uncommon,"Rare:",rare,"ePIC:",epic,"Legendary:" , legendary)
