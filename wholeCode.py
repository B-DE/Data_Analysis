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
from flask import Flask, request, json
import json
import pandas as pd






app = Flask(__name__)


commonResponse = {
    'version' : '2.0',
    'resultCode' : 'OK',
    'output' : {}
}



def getUtteranceParameter() :
    data = request.get_json()
    return data['action']['parameters']



@app.route('/instagramChatbot', methods=['POST'])
def instaAnalysis():




    '''-------------------------------------------------------'''
    # 로그인
    '''-------------------------------------------------------'''

    ## url 열기
    driver = webdriver.Chrome('C:/Project/chromedriver.exe')
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)


    ## 로그인 할 ID (인스타 아이디!! 이메일 전화번호 안됨!!)
    utteranceParameter = getUtteranceParameter()
    id = utteranceParameter['instagram']['id']
    ## 로그인 할 Password
    password = utteranceParameter['instagram']['password']


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



    ## 드라이버 끄기
    driver.close()
    driver.quit()


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # 머신러닝 url 로그인
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    ## url 열기
    driver = webdriver.Chrome('C:/Project/chromedriver.exe')
    driver.get('https://machinelearningforkids.co.uk/#!/login')
    time.sleep(2)

    ## '로그인' 버튼 클릭
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/button").click()
    time.sleep(5)

    ## 로그인
    utteranceParameter = getUtteranceParameter()
    ID = utteranceParameter['machine']['id']
    PASSWORD = utteranceParameter['machine']['password']

    ## ID, Password 입력
    driver.find_elements_by_name("username")[0].send_keys(ID)
    driver.find_elements_by_name("password")[0].send_keys(PASSWORD)
    time.sleep(2)

    ## '로그인' 버튼 클릭
    driver.find_element_by_xpath("//*[@id='auth0-lock-container-1']/div/div[2]/form/div/div/div/button").click()
    time.sleep(5)

    ## 드라이버 끄기
    driver.close()
    driver.quit()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # json 파일 호출
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    ## json 파일 열기
    json_data = instaInfo

    ## 데이터 형식 변경

    ### 데이터프레임 형식
    df = pd.DataFrame(json_data)

    ### 리스트형식으로 게시글 저장
    data = []
    for i in json_data:
        data.append(df[i]['context'])

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # 학습 모델
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    ## 수식어 분석 기능(meaching learning for kids)
    def classify(text):
        key = "bf8af0a0-5a41-11eb-99e6-fb4ecbaf4f51248f7a0e-6e01-438d-810a-7171f54c646e"
        url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

        response = requests.get(url, params={"data": text})

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()

    ## 게시글 분석

    label_data = []
    confi_data = []

    for i in data:

        ### 게시글 입력
        demoStr = i
        demo = classify(i)

        ### 수식어 {dessert, mood, photo, view}
        label = demo["class_name"]
        ### 신뢰도
        confidence = demo["confidence"]

        ### 결과 저장

        #### 신뢰도가 60이상인 경우 수식어 저장
        #### 신뢰도가 낮은 경우 'non'으로 저장
        if confidence >= 60:
            label_data.append(label)
        else:
            label_data.append('non')

        #### 신뢰도 저장
        confi_data.append("%d%%" % (confidence))

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # json 저장
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    ## label, confidence 추가
    count = int(0)
    for i in json_data:
        json_data['%s' % i]['label'] = label_data[count]
        json_data['%s' % i]['confidence'] = confi_data[count]
        count += 1
    json_data['게시물 갯수'] = count

    ''''''''''''''''''''''''''''''''''''''''''''''''''
    # 결과 출력
    ''''''''''''''''''''''''''''''''''''''''''''''''''

    ## 파일 저장
    file_name = "\Data_" + id + ".json"
    with open('C:\Project'+ file_name, 'w', encoding='utf-8') as make_file:
        json.dump(instaInfo, make_file, indent="\t")



    ## 출력
    print(json.dumps(json_data, indent="\t", ensure_ascii=False))

    for i in range(0, len(label_data)):
        print(label_data[i])
        print(confi_data[i])



    ## host url로 전송
    return json.dumps(json_data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)