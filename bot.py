import os
import requests 
import json
token = os.getenv('TELE_TOKEN')
method = 'getUpdates'
url="https://api.hphk.io/telegram/bot{}/{}".format(token,method)#c9에서 챗봇을 막아놨기때문에 asw로 우회하여 들어감

print(url)
#json파일 뜬다
res=requests.get(url).json()
user_id = res["result"][0]["message"]["from"]["id"]
msg= "야 라고 해도되~" #메세지 보내기
method = 'sendMessage'#대문자 주의

msg_url ="https://api.hphk.io/telegram/bot{}/{}?chat_id={}&text={}".format(token,method,user_id,msg)
requests.get(msg_url)