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
# 드라이버 연결 -> BeautifulSoup 설정
'''-------------------------------------------------------'''

##  드라이버 설치 경로
driver_path = 'C:/Project/chromedriver.exe'


## 드라이버 연결
driver = webdriver.Chrome(driver_path)



'''-------------------------------------------------------'''
# 로그인
'''-------------------------------------------------------'''

def login(id, password, url):


    try:
        ## 로그인할 url 연결
        driver.get(url)
        time.sleep(2)


        ## ID, Password 입력
        driver.find_elements_by_name("username")[0].send_keys(id)
        driver.find_elements_by_name("password")[0].send_keys(password)
        time.sleep(2)


        ## '로그인' 버튼 클릭
        driver.find_element_by_xpath("//*[@id='loginForm']/div[1]/div[3]/button/div").click()
        time.sleep(5)



        ## '로그인 정보 저장' 버튼 처리
        try:

            ### '로그인 정보 나중에 저장' 버튼 클릭
            driver.get('https://www.instagram.com/accounts/onetap/')
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()
            time.sleep(2)



        except:
            print('login info error')



    except:
        print('login error')




'''-------------------------------------------------------'''
# 인스타 크롤링
'''-------------------------------------------------------'''


def instaCrawling(id):


    ## 프로필(saved lists) 들어가기
    driver.get('https://www.instagram.com/' + id + '/saved/')


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
                print('게시물 갯수: ' + str(len(urllist)))



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
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")


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




    return ctxlist, namelist





'''-------------------------------------------------------'''
# 카카오맵에서 카페명 검색
'''-------------------------------------------------------'''


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






'''-------------------------------------------------------'''
# 주소 크롤링
'''-------------------------------------------------------'''

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






'''-------------------------------------------------------'''
# 전화번호 크롤링
'''-------------------------------------------------------'''

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




'''-------------------------------------------------------'''
# 업종명 크롤링
'''-------------------------------------------------------'''

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
                cafe_indust = cafe.select('.PlaceItem.clickArea .clickable')[0].text
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





'''-------------------------------------------------------'''
# 수식어 분석
'''-------------------------------------------------------'''

def modifierAnalysis(context):

    try:
        ## 학습모델 호출
        def classify(context):

            key = "bf8af0a0-5a41-11eb-99e6-fb4ecbaf4f51248f7a0e-6e01-438d-810a-7171f54c646e"
            classify_url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

            response = requests.get(classify_url, params={"data": context})

            if response.ok:
                responseData = response.json()
                topMatch = responseData[0]
                return topMatch
            else:
                response.raise_for_status()



        ## 분석 실행
        analysis = classify(context)



        ## 변수 설정

        ### 수식어 {dessert, mood, photo, view}
        modifier = analysis["class_name"]

        ### 신뢰도
        confidence = analysis["confidence"]




        ## 결과 저장

        ### 신뢰도가 60이상인 경우 수식어 저장
        ### 신뢰도가 낮은 경우 'non'으로 저장
        if confidence >= 60:
            return modifier, confidence
        else:
            return 'non', confidence


    except:
        print('dataAnalysis error')



'''-------------------------------------------------------'''
# db 저장
'''-------------------------------------------------------'''

def saveDB(file_path, data_length):


    ## 데이터를 저장할 변수
    dataAnalysis = dict()


    ## 데이터 저장
    for i in range(0, data_length):

        ### key 설정
        Name = dict()

        ### value 설정
        Name["name"] = namelist[i]
        Name["context"] = ctxlist[i]
        Name["address"] = address[i]
        Name["phone"] = phone[i]
        Name["industry"] = industry[i]
        Name["classify"] = classify[i]
        Name["confidence"] = confidence[i]

        ### json 저장
        dataAnalysis[str(namelist[i])] = Name


    ## 파일 저장
    with open(file_path, 'w', encoding='utf-8') as make_file:
        json.dump(dataAnalysis, make_file, indent = "\t")




'''-------------------------------------------------------'''
# 코드 실행
'''-------------------------------------------------------'''

## 변수 설정
id = ''
password = ''
instagram_url = 'https://www.instagram.com/accounts/login/'
kakaomap_url = 'https://map.kakao.com/'
namelist = []
ctxlist = []
address = []
bigRegion = []
smallRegion = []
industry = []
phone = []
classify = []
confidence = []
file_path = 'C:\Project\Data_' + id + ".json"


## 인스타 로그인
login(id, password, instagram_url)




## 인스타 크롤링(게시글, 카페명)
instagramData = instaCrawling(id)
namelist = instagramData[1]
ctxlist = instagramData[0]





## 카카오맵 크롤링(주소, 번호, 업종)
for name in namelist:

    print(name)

    ## 카페 검색
    searchDriver = searchName(name, kakaomap_url)

    ## 주소 크롤링
    a = addressCrawling(name)
    address.append(a)
    time.sleep(0.2)

    ## 번호 크롤링
    p = phoneCrawling(name)
    phone.append(p)
    time.sleep(0.2)

    ## 업종 크롤링
    i = industryCrawling(name)
    industry.append(i)
    time.sleep(0.2)

    print('----------------------------')




## 수식어 분석
for context in ctxlist:
    result = modifierAnalysis(context)
    classify.append(result[0])
    confidence.append(result[1])

print(classify)
print(confidence)



## 데이터 파일 저장
data_length = len(namelist)
saveDB(file_path, data_length)
print()



## 드라이브 종료
driver.close()
driver.quit()