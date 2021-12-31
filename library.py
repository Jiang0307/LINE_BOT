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

dict_ch_en = {}

def create_dictionary():
    header = {"User-Agent":"Chrome/96.0.4664.110" , "Accept-Language":"zh-TW,zh;q=0.9"} # configurations
    opgg_url = "https://tw.op.gg/champion/statistics"
    X_PATH =  '//div[@class="champion-index__champion-list"]//div[@data-champion-name and @data-champion-key]'
    webpage = requests.get(opgg_url, headers=header)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    champ_list = dom.xpath(X_PATH)
    champ_count =  len(champ_list)
    for i in range(champ_count):
        chinese = champ_list[i].get("data-champion-name")
        english = champ_list[i].get("data-champion-key")
        english = english.capitalize()
        dict_ch_en[chinese] = english
        #dict_en_ch[english] = chinese
    dict_ch_en["翱銳龍獸"]="AurelionSol";dict_ch_en["蒙多醫生"]="DrMundo";dict_ch_en["寇格魔"]="KogMaw";dict_ch_en["李星"]="LeeSin";dict_ch_en["易大師"]="MasterYi";dict_ch_en["好運姐"]="MissFortune";dict_ch_en["雷珂煞"]="RekSai";dict_ch_en["貪啃奇"]="TahmKench";dict_ch_en["逆命"]="TwistedFate";dict_ch_en["趙信"]="XinZhao";
    return