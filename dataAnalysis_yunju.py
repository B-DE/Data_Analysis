import requests
import json
import pandas as pd
from selenium import webdriver
import time



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
id = ''
password = ''


## ID, Password 입력
driver.find_elements_by_name("username")[0].send_keys(id)
driver.find_elements_by_name("password")[0].send_keys(password)
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
file_path = 'C:\Project\Data_yun9u_00.json'

with open(file_path) as json_file:
    json_data = json.load(json_file)



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
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

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
    confi_data.append("%d%%" %(confidence))


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# json 저장
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## label, confidence 추가
count = int(0)
for i in json_data:
    json_data['%s'%i]['label'] = label_data[count]
    json_data['%s'%i]['confidence'] = confi_data[count]
    count += 1


## 파일 수정
with open(file_path, 'w', encoding='utf-8') as make_file:
    json.dump(json_data, make_file, indent="\t")




'''''''''''''''''''''''''''
# 결과 출력
'''''''''''''''''''''''''''
print(json.dumps(json_data, indent="\t", ensure_ascii=False))

for i in range(0, len(label_data)):
    print(label_data[i])
    print(confi_data[i])
