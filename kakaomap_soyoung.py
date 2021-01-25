# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 21:11:56 2021

@author: a7580
"""
# 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.parse
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, json

## 카카오맵 분석

driver = webdriver.Chrome('C:/instachatbot/chromedriver_win32 (2)/chromedriver.exe')
driver.get('https://map.kakao.com/')
time.sleep(2)


# 검색 창
search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')

# 검색어 입력
search_area.send_keys('클랭블루')  

# Enter로 검색
driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

cafe_lists = soup.select('.placelist > .PlaceItem')
for cafe in cafe_lists:
	cafe_address = cafe.select('div.addr > p ')[0].text  # cafeName
    

    
# 결과값 확인
print(cafe_address)