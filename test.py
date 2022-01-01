import os
import re
import requests
from pyquery import PyQuery

def get_message(positions):
    for position in positions:
        img = position.find("td.champion-index-table__cell--value img").attr("src")
        name = position.find("div.champion-index-table__name").text()                # 獲取英雄名稱
        win_rate = position.find("td.champion-index-table__cell--value").text()[:6]  # 獲取勝率
        pick_rate = position.find("td.champion-index-table__cell--value").text()[6:] # 獲取登場率
        tier = "T"+re.match(".*r-(.*?)\.png",img).group(1)                           # 獲取src屬性並提取出優先級
        yield{"name":name , "win_rate":win_rate , "pick_rate":pick_rate , "tier":tier}
    
def convert_position(position):
    ret = ""
    if (position=="上") or (position=="上路") or (position=="上單") or (position=="TOP") or (position=="top") or (position=="Top"):
        ret = "TOP"
    elif (position=="野") or (position=="打野") or (position=="JG") or (position=="JUNGLE") or (position=="jungle") or (position=="Jungle"):
        ret = "JUNGLE"
    elif (position=="中") or (position=="中路") or (position=="中單") or (position=="MID") or (position=="mid") or (position=="Mid") or (position=="MIDDLE") or (position=="middle") or (position=="Middle") or (position=="AP") or (position=="ap"):
        ret = "MID"
    elif (position=="下") or (position=="下路") or (position=="ADC") or (position=="adc") or (position=="Adc") or (position=="AD") or (position=="ad") or (position=="Ad"):
        ret = "ADC"
    elif (position=="輔") or (position=="輔助") or (position=="SUP") or (position=="sup") or (position=="Sup") or (position=="SUPPORT") or (position=="support") or (position=="Support"):
        ret = "SUPPORT"
    else:
        ret = "0"
    return ret
        
def convert_tier(tier):
    ret = ""
    if (tier=="T1") or (tier=="t1") or (tier=="1") or (tier=="TIER 1") or (tier=="tier 1") or (tier=="Tier 1"):
        return  "T1"
    elif (tier=="T2") or (tier=="t2") or (tier=="2") or (tier=="TIER 2") or (tier=="tier 2") or (tier=="Tier 2"):
        ret = "T2"
    elif (tier=="T3") or (tier=="t3") or (tier=="3") or (tier=="TIER 3") or (tier=="tier 3") or (tier=="Tier 3"):
        ret = "T3"
    elif (tier=="T4") or (tier=="t4") or (tier=="4") or (tier=="TIER 4") or (tier=="tier 4") or (tier=="Tier 4"):
        ret = "T4"
    elif (tier=="T5") or (tier=="t5") or (tier=="5") or (tier=="TIER 5") or (tier=="tier 5") or (tier=="Tier 5"):
        ret = "T5"
    else:
        ret = "0"
    return ret

def print_info(doc , which_position , which_tier):
    tier = "tr"
    return_dict = {}
    for information in doc("tbody").items(): # 遍歷五個tbody節點，分別代表五個位置
        position = re.match("tabItem champion-trend-tier-(.*)",information.attr("class")).group(1) # 用regular expresion提取出tbody的class屬性的個位置
        if which_position == position:
            for items in get_message(information.find(tier).items()): # 利用get_message函數，遍歷每一個tbody節點的tier節點
                if items.get("tier") == "T1" == which_tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T2" == which_tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T3" == which_tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T4" == which_tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T5" == which_tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
    return return_dict          

if __name__ == "__main__":
    HEADERS = {"User-Agent":"Chrome/96.0.4664.110" , "Accept-Language":"zh-TW,zh;q=0.9"} # configurations
    html = requests.get("http://www.op.gg/champion/statistics",headers=HEADERS).text
    doc = PyQuery(html)
    while True:
        lane = convert_position(input("輸入位置 : ").rstrip())
        if lane == "0":
            print("錯誤格式\n")
            continue
        tier = convert_tier(input("輸入階級 : ").rstrip())
        if tier == "0":
            print("錯誤格式\n")
            continue
        res = print_info(doc , lane , tier)
        print(res)