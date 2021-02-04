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


# 전역변수 설정

# ## BeautifulSoup 설정
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# json 파일 호출
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def json_open(json_path):

    ## 파일 열기
    with open(json_path) as json_file:
        json_data = json.load(json_file)


    ## 업소명 데이터 저장
    nameData = []
    for i in json_data:
        nameData.append(i)


    ## 업소명 리스트 리턴
    return nameData



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
# 카페명 검색
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def searchName(name, url):
    
    ## 페이지 새로고침
    driver.get(url)
    
    ## 검색어 입력
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
    search_area.send_keys(name)


    ## Enter로 검색
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  
    time.sleep(1)

    return driver






'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 주소 크롤링
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def addressCrawling(name):

    ## BeautifulSoup 설정
    html = searchDriver.page_source
    soup = BeautifulSoup(html, 'html.parser')



    ## 검색게시물 순서
    count = int(0)



    ## 검색된 각 게시물에 대해
    cafe_list = soup.select('.placelist  .PlaceItem')



    for cafe in cafe_list:


        try:

            ## 검색 게시물의 카페명
            searchedName = soup.select('.PlaceItem.clickArea .link_name')[count].text



            ## 주소 저장 (일치하는 게시물에 대해)
            if(name == searchedName):
                cafe_address = cafe.select('.PlaceItem.clickArea .addr > p')[0].text
                # address.append(cafe_address)
                print(cafe_address)

                return cafe_address



                ## 검색명과 일치하는 게시물이 없을 시
            else:


                ### 마지막 게시물이 아니면 반복 진행
                if(count <= len(cafe.select('.PlaceItem.clickArea .link_name'))):
                    print('address next')



                ### 마지막 게시물이라면 공백 저장 후 반복 종료
                else:
                    #address.append('')
                    print('address break')

                    return ''


            count += 1


        except:
            print('address error')
            return ''






'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 전화번호 크롤링
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def phoneCrawling(name):


    ## BeautifulSoup 설정
    html = searchDriver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    ## 검색게시물 순서
    count = int(0)


    ## 검색된 각 게시물에 대해
    cafe_list = soup.select('.placelist  .PlaceItem')


    for cafe in cafe_list:


        try:


            ## 검색 게시물의 카페명
            searchedName = soup.select('.PlaceItem.clickArea .link_name')[count].text


            ## 번호 저장 (일치하는 게시물에 대해)
            if (name == searchedName):
                cafe_phone = cafe.select('.PlaceItem.clickArea .phone')[0].text
                # phone.append(cafe_phone)
                print(cafe_phone)
                return cafe_phone


            ## 검색명과 일치하는 게시물이 없을 시
            else:

                ### 마지막 게시물이 아니면 반복 진행
                if (count <= len(cafe.select('.PlaceItem.clickArea .link_name'))):
                    print('phone next')


                ### 마지막 게시물이라면 공백 저장 후 반복 종료
                else:
                    phone.append('')
                    print('phone break')
                    return ''


            count += 1


        except:
            print('phone error')
            return ''




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 업종명
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def industryCrawling(name):


    ## BeautifulSoup 설정
    html = searchDriver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    ## 검색게시물 순서
    count = int(0)


    ## 검색된 각 게시물에 대해
    cafe_list = soup.select('.placelist  .PlaceItem')


    for cafe in cafe_list:


        try:


            ## 검색 게시물의 카페명
            searchedName = soup.select('.PlaceItem.clickArea .link_name')[count].text


            ## 업종명 저장 (일치하는 게시물에 대해)
            if (name == searchedName):
                cafe_indust = cafe.select('.tit_name .subcategory clickable')[0].text
                print(cafe_indust)
                return cafe_indust


            ## 검색명과 일치하는 게시물이 없을 시
            else:

                ### 마지막 게시물이 아니면 반복 진행
                if (count <= len(cafe.select('.PlaceItem.clickArea .link_name'))):
                    print('industry next')


                ### 마지막 게시물이라면 공백 저장 후 반복 종료
                else:
                    phone.append('')
                    print('industry break')
                    return ''


            count += 1


        except:
            print('industry error')
            return ''





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 코드 실행
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


## 변수 설정
json_path = 'C:\Project\Data_yun9u_00.json'
driver_path = 'C:/Project/chromedriver.exe'
url = 'https://map.kakao.com/'
# name = '커피프렌즈'


address = []
bigRegion = []
smallRegion = []
industry = []
phone = []



## json 파일 열기 ->
nameData = json_open(json_path)
driver = driverConnect(driver_path, url)


## BeautifulSoup 설정
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')





for name in nameData:

    print(name)

    ## 카페 검색
    searchDriver = searchName(name, url)

    # ## 주소 크롤링
    # a = addressCrawling(name)
    # address.append(a)
    # time.sleep(0.2)
    #
    # ## 번호 크롤링
    # p = phoneCrawling(name)
    # phone.append(p)
    # time.sleep(0.2)

    ## 업종 크롤링
    i = industryCrawling(name)
    industry.append(i)
    time.sleep(0.2)

    print('----------------------------')





driver.close()
driver.quit()