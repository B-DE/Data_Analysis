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





'''-------------------------------------------------------'''
# 로그인
'''-------------------------------------------------------'''

## url 열기
driver = webdriver.Chrome('C:/Project/chromedriver.exe')
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(2)


## 로그인 할 ID (인스타 아이디!! 이메일 전화번호 안됨!!)
id = 'yun9u_00'
## 로그인 할 Password
password = 'emmadaria0110##'


## ID, Password 입력
driver.find_elements_by_name("username")[0].send_keys(id)
driver.find_elements_by_name("password")[0].send_keys(password)
time.sleep(2)


## '로그인' 버튼 클릭
driver.find_element_by_xpath("//*[@id='loginForm']/div[1]/div[3]/button/div").click()
time.sleep(5)


## '로그인 정보 나중에 저장' 버튼 클릭
driver.get('https://www.instagram.com/accounts/onetap/')
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()
time.sleep(2)



## 프로필(saved lists) 들어가기
driver.get('https://www.instagram.com/' + id + '/saved/')




'''-------------------------------------------------------'''
# 크롤링
'''-------------------------------------------------------'''



## HTTP 가져오기
req = requests.get('https://www.instagram.com/' + id + '/saved/')
html = req.text



## 게시물 url 주소 저장



### url 저장할 리스트
urllist = []

while True:
    pageString = driver.page_source
    bs = BeautifulSoup(pageString, "lxml")

    for link1 in bs.find_all(name="div",attrs={"class":"Nnq7C weEfm"}):

        try:
            title = link1.select('a')[0]
            real = title.attrs['href']
            urllist.append(real)
        except :
            print('더 이상 게시글이 존재하지 않습니다.')
        try:
            title = link1.select('a')[1]
            real = title.attrs['href']
            urllist.append(real)
        except:
            print('더 이상 게시글이 존재하지 않습니다.')
        try :
            title = link1.select('a')[2]
            real = title.attrs['href']
            urllist.append(real)
        except :
            print('더 이상 게시글이 존재하지 않습니다.')


    ### 스크롤 내리기 및 반복 마무리
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue


ctxlist = []
namelist = []


try:
    for i in range(0, len(urllist)):

        ### url로 게시물 접근
        req = 'https://www.instagram.com' + urllist[i]
        driver.get(req)
        webpage = driver.page_source
        soup = BeautifulSoup(webpage, "html.parser")


        ### 게시글 크롤링
        try:
            content = soup.select('div.C4VMK > span')[0].text
        except:
            content = ''

        ctxlist.append(content)


        ### 업소명 크롤링(첫번째 해시태그가 업소명인 경우!!!)
        try:
            name = soup.select('div.C4VMK > span > a')[0].text
            name = name.replace("#", "")
        except:
            name = ''
        namelist.append(name)


except:
    print("error")




## 결과값 확인
print("게시물 갯수: " + str(len(urllist)) + "개\n\n")

for i in range(0, len(urllist)):
    print("===========================================")
    print("\n[" + str(i+1) + "번째 게시물]")
    print("\n이름: " + namelist[i])
    print("\n" + ctxlist[i])





## json 파일 저장

### 파일 쓰기
instaInfo = dict()

for i in range(0, len(urllist)):
    Name = namelist[i]
    Name = dict()
    Name["name"] = namelist[i]
    Name["context"] = ctxlist[i]
    instaInfo[str(namelist[i])] = Name



### 파일 저장
file_name = "\Data_" + id + ".json"
with open('C:\Project'+ file_name, 'w', encoding='utf-8') as make_file:
    json.dump(instaInfo, make_file, indent="\t")



## 드라이버 끄기
driver.close()
driver.quit()


'''-------------------------------------------------------'''
# 데이터 분석
'''-------------------------------------------------------'''


## 카카오맵 분석



## 수식어 분석



'''-------------------------------------------------------'''
# db 저장
'''-------------------------------------------------------'''


