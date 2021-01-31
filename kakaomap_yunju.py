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



## 리스트형식으로 게시글 저장
nameData = []
for i in json_data:
    nameData.append(i)



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 드라이버 연결
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



## 드라이버 선택
driver = webdriver.Chrome('C:/Project/chromedriver.exe')



## 카카오맵 url 연결
driver.get('https://map.kakao.com/')



## BeautifulSoup 설정
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 카페명 검색
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

address = []
bigRegion = []
smallRegion = []
industry = []
phone = []


for i in nameData:

    ## 카페명 변수 설정
    searchName = i


    ## 검색어 입력
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
    search_area.send_keys(i)


    ## Enter로 검색
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    time.sleep(1)



    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # 주소 크롤링
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


    cafe_lists = soup.select('.placelist > .PlaceItem')
    for cafe in cafe_lists:
        cafe_address = cafe.select('div.addr > p ')[0].text



# 결과값 확인
print(cafe_address)