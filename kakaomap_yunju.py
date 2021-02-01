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



#
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# # 카페명 검색
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#
# address = []
# bigRegion = []
# smallRegion = []
# industry = []
# phone = []
#
# # count = int(0)
#
# for i in nameData:
#
#
#     ## 페이지 새로고침
#     driver.get('https://map.kakao.com/')
#
#
#     ## 카페명 변수 설정
#     searchName = i
#
#
#
#     ## 검색어 입력
#     search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
#     search_area.send_keys(i)
#
#
#     ## Enter로 검색
#     driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
#     time.sleep(1)
#
#
#
#     ## BeautifulSoup 설정
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#
#
#
#     '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     # 주소 크롤링
#     '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#
#
#     for j in range(len(soup.select('.PlaceItem.clickArea .link_name'))):
#
#         ## 태그 접근
#         try:
#             searched = soup.select('.PlaceItem.clickArea .link_name')[j].text
#             print(searched)
#
#
#             ## 주소 저장(일치하는 게시물에 대해) (!!!! 두번째 이상의 게시물 주소 크롤링)
#             if(i == searched):
#                 cafe_address = soup.select('.PlaceItem.clickArea .addr > p')[j].text
#                 address.append(cafe_address)
#                 break
#
#
#             ## 검색명과 일치하는 게시물이 없을 시
#             else:
#
#
#                 ## 마지막 게시물이 아니면 반복 진행
#                 if(j <= len(soup.select('.PlaceItem.clickArea .link_name'))):
#                     continue
#
#
#                 ## 마지막 게시물이라면 공백 저장 후 반복 종료
#                 else:
#                     address.append('')
#                     break
#
#
#         ## 태그가 없을 시 주소 공백으로 저장
#         except:
#             address.append('')
#
#
#
#
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# # 마무리
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#
# ## 드라이버 종료
# driver.close()
# driver.quit()
#
#
# ## 결과값 확인
# print(address)
# for i in address:
#     print(i + "\n\n")


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#
#
# ## 카카오맵 분석
#
# driver = webdriver.Chrome('C:/Project/chromedriver.exe')
# driver.get('https://map.kakao.com/')
# time.sleep(2)
#
# # 검색 창
# search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
#
# # 검색어 입력
# search_area.send_keys('클랭블루')
#
# # Enter로 검색
# driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
# time.sleep(1)
#
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
#
# cafe_lists = soup.select('.placelist > .PlaceItem')
# for cafe in cafe_lists:
#     cafe_address = cafe.select('div.addr > p ')[0].text  # cafeName
#
# # 결과값 확인
# print(cafe_address)