import os
import sys
import message_template
import requests
import re
from lxml import etree
from PIL import Image
from pyquery import PyQuery
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import send_text_message , send_image_message
from library import dict_ch_en , create_dictionary

champion_name = ""
current_lane = ""
current_tier = 0
current_lane_matchup = ""
current_name_matchup = ""
matchup_list = []

def is_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True
  
def check_input_name(name):
    if name in dict_ch_en.keys():
        return True
    return False

def check_input_lane(position):
    if (position=="上") or (position=="上路") or (position=="上單") or (position=="TOP") or (position=="top") or (position=="Top"):
        return True , "TOP"
    elif (position=="野") or (position=="打野") or (position=="JG") or (position=="JUNGLE") or (position=="jungle") or (position=="Jungle"):
        return True , "JUNGLE"
    elif (position=="中") or (position=="中路") or (position=="中單") or (position=="MID") or (position=="mid") or (position=="Mid") or (position=="MIDDLE") or (position=="middle") or (position=="Middle") or (position=="AP") or (position=="ap"):
        return True , "MID"
    elif (position=="下") or (position=="下路") or (position=="ADC") or (position=="adc") or (position=="Adc") or (position=="AD") or (position=="ad") or (position=="Ad"):
        return True , "ADC"
    elif (position=="輔") or (position=="輔助") or (position=="SUP") or (position=="sup") or (position=="Sup") or (position=="SUPPORT") or (position=="support") or (position=="Support"):
        return True , "SUPPORT"
    return False , None

def check_input_tier(tier):
    if (tier=="T1") or (tier=="t1") or (tier=="1") or (tier=="TIER 1") or (tier=="tier 1") or (tier=="Tier 1"):
        return True , "T1"
    elif (tier=="T2") or (tier=="t2") or (tier=="2") or (tier=="TIER 2") or (tier=="tier 2") or (tier=="Tier 2"):
        return True , "T2"
    elif (tier=="T3") or (tier=="t3") or (tier=="3") or (tier=="TIER 3") or (tier=="tier 3") or (tier=="Tier 3"):
        return True , "T3"
    elif (tier=="T4") or (tier=="t4") or (tier=="4") or (tier=="TIER 4") or (tier=="tier 4") or (tier=="Tier 4"):
        return True , "T4"
    elif (tier=="T5") or (tier=="t5") or (tier=="5") or (tier=="TIER 5") or (tier=="tier 5") or (tier=="Tier 5"):
        return True , "T5"
    return False , None

def crawl_matchup(lane , champion):
    wait_time = 5
    url = f"https://www.op.gg/champion/{champion}/statistics/{lane}/matchup"
    print(f"URL = {url}")
    option = Options()
    option.add_argument("--headless")
    option.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯
    option.add_argument("--log-level=3");
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    browser.implicitly_wait(10)
    wait = ui.WebDriverWait(browser, wait_time)
    matchup_list.clear()
    try:
        wait.until(lambda driver: driver.find_elements(By.XPATH,"//div[@class='champion-matchup-list__champion']//span[1]"))
        Buttons = browser.find_elements(By.XPATH,"//div[@class='champion-matchup-list__champion']//span[1]")
    except:
        Buttons = browser.find_elements(By.XPATH,"//div[@class='champion-matchup-list__champion']//span[1]")
    for button in Buttons:
        browser.execute_script("arguments[0].click();", button)
        wait = ui.WebDriverWait(browser, wait_time)
        try:
            wait.until(lambda driver: driver.find_elements(By.XPATH,"//table[@class='champion-matchup-table']//td[1]"))
            col = browser.find_elements(By.XPATH,"//table[@class='champion-matchup-table']//td[1]")
        except:
            browser.execute_script("arguments[0].click();", button)
            col = browser.find_elements(By.XPATH,"//table[@class='champion-matchup-table']//td[1]")
        win_rate = col[5].text
        matchup_list.append( [button.text , win_rate] )
        matchup_list.sort(key = lambda x: x[1])
        matchup_list.reverse()
    browser.close()
    
    if matchup_list:
        return True
    else:
        matchup_list.clear()
        return False

def get_image_url(champion):
    name = dict_ch_en[champion]
    img_url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_0.jpg"
    #img = Image.open(requests.get(img_url,stream=True).raw)
    return img_url

def get_opgg_url(champion):
    name = dict_ch_en[champion]
    url = f"https://www.op.gg/champion/{name}/statistics/"
    return url

def get_story_url(champion):
    base_url =  "https://universe.leagueoflegends.com/zh_TW/champion/"
    name = dict_ch_en[champion]
    result_url = base_url + name
    return result_url

def get_message(positions):
    for position in positions:
        img = position.find("td.champion-index-table__cell--value img").attr("src")
        name = position.find("div.champion-index-table__name").text()                # 獲取英雄名稱
        win_rate = position.find("td.champion-index-table__cell--value").text()[:6]  # 獲取勝率
        pick_rate = position.find("td.champion-index-table__cell--value").text()[6:] # 獲取登場率
        tier = "T"+re.match(".*r-(.*?)\.png",img).group(1)                           # 獲取src屬性並提取出優先級
        yield{"name":name , "win_rate":win_rate , "pick_rate":pick_rate , "tier":tier}

def get_win_rate(tier , lane):
    HEADERS = {"User-Agent":"Chrome/96.0.4664.110" , "Accept-Language":"zh-TW,zh;q=0.9"} # configurations
    html = requests.get("http://www.op.gg/champion/statistics",headers=HEADERS).text
    doc = PyQuery(html)
    tier = "tr"
    return_dict = {}
    for information in doc("tbody").items(): # 遍歷五個tbody節點，分別代表五個位置
        position = re.match("tabItem champion-trend-tier-(.*)",information.attr("class")).group(1) # 用regular expresion提取出tbody的class屬性的個位置
        if lane == position:
            for items in get_message(information.find(tier).items()): # 利用get_message函數，遍歷每一個tbody節點的tier節點
                if items.get("tier") == "T1" == tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T2" == tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T3" == tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T4" == tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
                elif items.get("tier") == "T5" == tier:
                    temp = [ items.get("win_rate") , items.get("pick_rate") ]
                    return_dict[items.get("name")] = temp
    print(return_dict  )
    # header = {"User-Agent": "Chrome/96.0.4664.110" , "Accept-Language":"zh-TW,zh;q=0.9"} # configurations
    # html = requests.get("http://www.op.gg/champion/statistics",headers=header).text
    # doc = PyQuery(html)
    # tier = "tr"
    # return_message = ""
    # for information in doc("tbody").items(): # 遍歷五個tbody節點，分別代表五個位置
    #     position = re.match("tabItem champion-trend-tier-(.*)",information.attr("class")).group(1) # 用regular expresion提取出tbody的class屬性的個位置
    #     if lane == position:
    #         for items in get_message(information.find(tier).items()): # 利用get_message函數，遍歷每一個tbody節點的tier節點
    #             if items.get("tier") == "T1" == tier:
    #                 temp = str( items.get("name") ) + " : " + items.get("win_rate") + "\n"
    #                 return_message += temp 
    #             elif items.get("tier") == "T2" == tier:
    #                 temp = str( items.get("name") ) + " : " + items.get("win_rate") + "\n"
    #                 return_message += temp
    #             elif items.get("tier") == "T3" == tier:
    #                 temp = str( items.get("name") ) + " : " + items.get("win_rate") + "\n"
    #                 return_message += temp
    #             elif items.get("tier") == "T4" == tier:
    #                 temp = str( items.get("name") ) + " : " + items.get("win_rate") + "\n"
    #                 return_message += temp
    #             elif items.get("tier") == "T5" == tier:
    #                 temp = str( items.get("name") ) + " : " + items.get("win_rate") + "\n"
    #                 return_message += temp
    # print("MESSAGE : ",return_message)
    # #return return_message

def get_pick_rate(tier , lane):
    header = {"User-Agent":"Chrome/96.0.4664.110" , "Accept-Language":"zh-TW,zh;q=0.9"} # configurations
    html = requests.get("http://www.op.gg/champion/statistics",headers=header).text
    doc = PyQuery(html)
    tier = "tr"
    return_message = ""
    for information in doc("tbody").items(): # 遍歷五個tbody節點，分別代表五個位置
        position = re.match("tabItem champion-trend-tier-(.*)",information.attr("class")).group(1) # 用regular expresion提取出tbody的class屬性的個位置
        if lane == position:
            for items in get_message(information.find(tier).items()): # 利用get_message函數，遍歷每一個tbody節點的tier節點
                if items.get("tier") == "T1" == tier:
                    temp = str( items.get("name") ) + " : " + items.get("pick_rate") + "\n"
                    return_message += temp 
                elif items.get("tier") == "T2" == tier:
                    temp = str( items.get("name") ) + " : " + items.get("pick_rate") + "\n"
                    return_message += temp
                elif items.get("tier") == "T3" == tier:
                    temp = str( items.get("name") ) + " : " + items.get("pick_rate") + "\n"
                    return_message += temp
                elif items.get("tier") == "T4" == tier:
                    temp = str( items.get("name") ) + " : " + items.get("pick_rate") + "\n"
                    return_message += temp
                elif items.get("tier") == "T5" == tier:
                    temp = str( items.get("name") ) + " : " + items.get("pick_rate") + "\n"
                    return_message += temp
    return return_message 

def get_matchup_winrate():
    return_message = f"{current_name_matchup}的對位勝率 : \n"
    for name , win_rate in matchup_list:
       temp = name + " : " + win_rate + "\n"
       return_message += temp
    return return_message

create_dictionary()
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "主選單"
        else:        
            return text.lower() == "menu"

    def is_going_to_feature(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "功能"
        else:        
            return text.lower() == "feature"
    
    def is_going_to_input_name(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "依照英雄查詢"
        else:        
            return text.lower() == "search by champion"
    
    def is_going_to_select_service(self , event):
        global champion_name
        text = event.message.text
        print(text)
        if is_chinese(text) == True:
            ret = check_input_name(text)    # 英雄名稱是否存在
            if ret == True:
                print("TRUE!!!\n")
                champion_name = text
            else:
                print("FALSE!!!\n")
                champion_name = ""            
            return ret
        else:        
            return False
        
    
    def is_going_to_send_image(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            
            return text == "下載圖片"
        else:        
            return text.lower() == "download image"
        
    def is_going_to_opgg_url(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "英雄數據"
        else:
            return text.lower() == "champion statistics"

    def is_going_to_story_url(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "英雄故事"
        else:
            return text.lower() == "champion story"

    def is_going_to_input_lane(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "依照階級查詢"
        else:
            return text.lower() == "search by tier"

    def is_going_to_input_tier(self , event):
        global current_lane
        text = event.message.text
        ret , lane = check_input_lane(text)
        if ret == True: # 位置名稱是否存在
            current_lane = lane
            print(f"TRUE CURRENT lANE = {current_lane}\n")
            return True
        else:
            current_lane = ""
            print(f"FALSE CURRENT lANE = {current_lane}\n")
            return False

    def is_going_to_select_info(self , event):
        global current_tier
        text = event.message.text
        ret , tier = check_input_tier(text)
        if ret == True: # 階級名稱是否存在
            current_tier = tier
            print(f"TRUE CURRENT TIER = {current_tier}\n")
            return True
        else:
            current_tier = 0
            print(f"FALSE CURRENT TIER = {current_tier}\n")
            return False
        
    def is_going_to_win_rate(self,event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "勝率"
        else:
            return text.lower() == "win rate"
        
    def is_going_to_pick_rate(self,event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "選取率"
        else:
            return text.lower() == "pick rate"
        
    def is_going_to_input_lane_matchup(self , event):
        text = event.message.text
        if is_chinese(text) == True:
            return text == "依照對抗查詢"
        else:
            return text.lower() == "search by matchup"

    def is_going_to_input_name_matchup(self , event):
        global current_lane_matchup
        text = event.message.text
        ret , lane = check_input_lane(text)
        print("LANE : ",lane,"\n")
        if ret == True: # 位置名稱是否存在
            print("TRUE!!!\n")
            current_lane_matchup = lane
            return True
        else:
            print("FALSE!!!\n")
            current_lane_matchup = ""
            return False
    def is_going_to_matchup_winrate(self , event):
        global current_name_matchup
        text = event.message.text
        if is_chinese(text) == False:                                    # 先確定輸入的是中文
            print("TEXT : ",text,"FALSE!!!\n")
            return False
        else:
            ret = check_input_name(text)    
            if ret == False:                                             # 再確定英雄名稱是否存在   
                print(f"FALSE!!!\n")
                return False
            else:
                current_name_matchup = text
                ret2 = crawl_matchup(current_lane_matchup , current_name_matchup)                                    # 最後看該輸入組合是否回傳空的list
                print("RET2 : ",ret2)
                print(f"LANE = {current_lane_matchup}",f"NAME = {current_name_matchup}")
                return ret2                
            
#=======================================ON ENTER=======================================
    def on_enter_menu(self , event):
        print("enter menu !!!\n")
        global champion_name,current_lane,current_tier,current_lane_matchup,current_name_matchup,matchup_list
        champion_name = ""
        current_lane = ""
        current_tier = 0
        current_lane_matchup = ""
        current_name_matchup = ""
        matchup_list.clear()
        reply_token = event.reply_token
        send_text_message(reply_token, "進入選單")

    def on_enter_feature(self , event):
        print("enter feature !!!\n")
        reply_token = event.reply_token
        message = message_template.feature
        message_to_reply = FlexSendMessage("功能介紹與說明", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_input_name(self , event):
        print("enter input name !!!\n")
        print("TEXT : ",)
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入英雄中文名稱")
        
    def on_enter_select_service(self , event):
        print("enter select service !!!\n")
        reply_token = event.reply_token
        message = message_template.service
        message_to_reply = FlexSendMessage("選擇項目", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        
    def on_enter_send_image(self , event):
        global champion_name
        print(f"enter send message , champion : {champion_name} !!!\n")
        reply_token = event.reply_token
        url = get_image_url(champion_name)
        send_image_message(reply_token , url)
        self.go_back()

    def on_enter_opgg_url(self , event):
        global champion_name
        print(f"enter opgg_url , champion : {champion_name} !!!\n")
        reply_token = event.reply_token
        url = get_opgg_url(champion_name)
        send_text_message(reply_token , url)
        self.go_back()
        
    def on_enter_story_url(self , event):
        global champion_name
        print(f"enter opgg_url , champion : {champion_name} !!!\n")        
        reply_token = event.reply_token
        url = get_story_url(champion_name)
        send_text_message(reply_token , url)
        self.go_back()

    def on_enter_input_lane(self , event):
        print("enter input lane !!!\n")        
        reply_token = event.reply_token
        send_text_message(reply_token , "請輸入路線")
        
    def on_enter_input_tier(self , event):
        print("enter input tier !!!\n")        
        reply_token = event.reply_token
        send_text_message(reply_token , "請輸入階級")
    
    def on_enter_select_info(self , event):
        print("enter select info !!!\n")
        reply_token = event.reply_token
        message = message_template.info
        message_to_reply = FlexSendMessage("選擇項目", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_win_rate(self , event):
        print("enter win rate !!!\n")
        reply_token = event.reply_token
        get_win_rate(current_tier , current_lane)
        ret = "FUCK\nFUCK\nFUCK\n"
        send_text_message(reply_token , ret)
        self.go_back()
        
    def on_enter_pick_rate(self , event):
        print("enter pick rate !!!\n")
        reply_token = event.reply_token
        ret = get_pick_rate(current_tier , current_lane)
        send_text_message(reply_token , ret)
        self.go_back()
        
# states = ["input_lane_matchup","input_name_matchup","matchup_winrate"]
    def on_enter_input_lane_matchup(self , event):
        print("on enter input lane matchup !!!\n")
        reply_token = event.reply_token
        send_text_message(reply_token , "請輸入路線")
    
    def on_enter_input_name_matchup(self , event):
        print("enter input name matchup !!!\n")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入英雄中文名稱")
        
    def on_enter_matchup_winrate(self , event):
        print("enter matchup winrate !!!\n")
        reply_token = event.reply_token
        ret = get_matchup_winrate()
        send_text_message(reply_token , ret)
        self.go_back()
        
        
    # def on_exit_state1(self):
    #     print("Leaving state1")
    
    
    
    # def on_exit_state2(self):
    #     print("Leaving state2")
