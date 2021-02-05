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
# 드라이버 연결
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def driverConnect(webdriver_path, url):
    ## 드라이버 연결
    driver = webdriver.Chrome(webdriver_path)

    ## 카카오맵 url 연결
    driver.get(url)

    return driver




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 로그인
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def login(id, password, url):








'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 코드 실행
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


## 변수 설정
json_path = 'C:\Project\Data_yun9u_00.json'
driver_path = 'C:/Project/chromedriver.exe'
url = 'https://map.kakao.com/'
name = '커피프렌즈'


address = []
bigRegion = []
smallRegion = []
industry = []
phone = []



## json 파일 열기/ 저장 -> 드라이버 연결
nameData = json_open(json_path)
driver = driverConnect(driver_path, url)


## BeautifulSoup 설정
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

