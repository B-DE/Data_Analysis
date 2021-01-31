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



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# json 파일 호출
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## json 파일 열기
file_path = 'C:\Project\Data_yun9u_00.json'

with open(file_path) as json_file:
    json_data = json.load(json_file)



## 데이터 형식 변경

### 데이터프레임 형식
df = pd.DataFrame(json_data)

### 리스트형식으로 게시글 저장
name = []
for i in json_data:
    data.append(df[i]['name'])





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 드라이버 연결
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## 드라이버 선택
driver = webdriver.Chrome('C:/Project/chromedriver.exe')

## 카카오맵 url 연결
driver.get('https://map.kakao.com/')

##





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 주소 가져오기
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''





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