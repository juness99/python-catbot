import os
from flask import Flask,request
from pprint import pprint as pp 
#메아리쳐주기위한 form으로부터가져와서 pprint를 가져오고 pp로 명령바꾸기
import requests
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
api_url ='https://api.hphk.io/telegram'#우회값
token = os.getenv('TELE_TOKEN')#토큰값을 가져온다
    
@app.route(f'/{token}',methods=['POST'])
def telegram(): #telegram 메소드 만듬
    naver_client_id= os.getenv('NAVER_ID')#client_id 가져옴
    naver_client_secret = os.getenv('NAVER_SECRET') #client_secret을 가져옴
        #텔레그램한테 이야기를 보내면 여기서 반응함
    tele_dict = request.get_json()#챗봇내용을 터미널로 출력해줌
    pp(request.get_json()) 
    #유저 정보
    chat_id =tele_dict["message"]["from"]["id"]
    #유저가 입력한 데이터
    #text = tele_dict["message"]["text"] 원래코드
    text = tele_dict.get('message').get('text')#오류가 안나오게하기위해 쓰는 함수
    #안녕하세요
    #로또
    #번역 안녕하세요=>번역

    tran = False
    img= False
    #사용자가 img를 넣었는지 체크
    #if tele_dict['message']['photo']is not None: #is not은 if이 이거니?이러고 물어보는것
    if tele_dict.get('message').get('photo') is not None:
        img = True

    else:
    #text(유저가입력한데이터)제일 앞 두글자가 번역?
        if text[:2]=="번역":
            #번역 안녕하세요
            tran = True #만약 text에 번역이 들어오면 True로 만들어줌
            text = text.replace("번역","")#파일이름 바꾸기 번역이란 말을 빼주기위해 사용
            #(교체내용 "바꿀내용")
            #출력 --바꿀내용 안녕하세요
        
    #print(chat_id)
    #print(text)
    if tran:
        papago = requests.post("https://openapi.naver.com/v1/papago/n2mt",
                    headers = {
                        "X-Naver-Client-Id":naver_client_id,
                        "X-Naver-Client-Secret":naver_client_secret
                    },
                    data = {
                        'source':'ko',
                        'target':'en',
                        'text':text
                    }
        )
        pp(papago.json())
        text = papago.json()['message']['result']['translatedText']
    elif img:
        text = "사용자가 이미지를 넣었어요"
        #-H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
#-H "X-Naver-Client-Id: 7USjlVtb5ahzRrHaBTCF" \
#-H "X-Naver-Client-Secret: oLG74NeUpG" \
#-d "source=ko&target=en&text=만나서 반갑습니다." -v
        #텔레그램에게 사진 정보 가져오기
        
        file_id=tele_dict['message']['photo'][-1]['file_id']
        file_path=requests.get(f"{api_url}/bot{token}/getFile?file_id={file_id}").json()['result']['file_path']#요청보내는 함수 우회주소를 가져옴
        file_url = f"{api_url}/file/bot{token}/{file_path}"
        print(file_url)
        
        #사진을 네이버 유명인 인식api로 넘겨주기
        file= requests.get(file_url,stream=True)
        clova = requests.post("https://openapi.naver.com/v1/vision/celebrity",
                    headers = {
                        "X-Naver-Client-Id":naver_client_id,
                        "X-Naver-Client-Secret":naver_client_secret
                    },
                    files = {
                        'image':file.raw.read()
                        }
                        )
        #가져온 데이터 중에서 필요한 정보 빼오기
        pp(clova.json())
        #인식이 되었을때
        if clova.json().get('info').get('faceCount'):
            text = clova.json()['faces'][0]['celebrity']['value']
        #if clova.json().get('info')
        else:
            text = "얼굴이 없어요 !!"
        #인식이 되지 않았을때
    elif text=="메뉴":
        menu_list = ["한식","중식","일식","테이크아웃","분식","선택식"]
        text = random.choice(menu_list)
    elif text=="몇대":
        fight_list = ["1대","2대","3대","4대","5대","6대"]
        text= random.choice(fight_list)

            
    #유저에게 그대로 돌려주기
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    #파라미터와 파라미터를 구분하는것 &
    return '',200 
    
app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))
#앱을 실행시켜줘 host getenv를이용해 ip를 가져옴
#IP를 안가져오면 0.0.0.0을 강제로줌
#PORT를 가져오고 안가져오면 8080을 강제로줌