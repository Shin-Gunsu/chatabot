import threading
import json
from openai import OpenAI
import sys
import os
file_path = os.path.dirname(__file__) 

# from config.DatabaseConfig import *
# from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer
from utils.FindIntent import FindIntent
from utils.Preprocess import Preprocess
from utils.GetAnswer_assistant import GetAnswer_assistant
from utils.Scrap import Scrap
from utils.LoginMakeCookie import LoginMakeCookie
from config.GlobalParams import gptapi_key
from models.recommender import Recommender

# 전처리 객체 생성
p = Preprocess(word2index_dic=file_path + '/train_tools/dict/chatbot_dict.bin',
               userdic=file_path + '/utils/user_dict.txt')

# 의도 파악 모델
intent = IntentModel(model_name=file_path + '/models/intent/intent_model.h5', proprocess=p)
print('의도 분류 모델 호출')
# 개체명 인식 모델
ner = NerModel(model_name=file_path + '/models/ner/ner_model.h5', proprocess=p)
print('개체명 인식 모델 호출')

#chat에서 받은 데이터 
def send_chat_data(conn,recv_json_data):
    query = recv_json_data['query']
    # 의도 파악
    intent_model = FindIntent(intent)
    intent_predict = intent_model.classification(query)
    
    if intent_predict[0] == 1:
        # QnA
        print(12)
        ner_predicts = ner.predict(query)
        ner_list = []
        for keyword, tag in ner_predicts:
            if tag != 0 and tag != 1:
                print(keyword, tag)
                ner_list.append(keyword)
        #ASSISTANT 모델
        assistant_model = GetAnswer_assistant(OpenAI(api_key=gptapi_key))
        assistant_model.create_thread()
        answer = assistant_model.ask(query)
        img_set =""
        if ("캠퍼스" in answer or "지도" in answer) and "위치하고" in answer:
            img_set = "map"

        print(answer)
        send_json_data_str = {
            "Answer" : answer,
            "Img":img_set
        }
        assistant_model.end_QnA()
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
        print(send_json_data_str)
    elif intent_predict[0] == 2:
        #과제 가져오기
        print(34)
        
        hwscrap = Scrap()
        r = hwscrap.scrapHW(host_response)
        print(r)
        send_string = ""
        for i in r:
            send_string = send_string + i + '\n'
        send_json_data_str = {
            "Answer" : send_string,
            "Img": ""
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
        
    elif intent_predict[0] == 4:
        #학식 가져오기
        print(56)
        menuscrap = Scrap()
        r = menuscrap.scrapMenu()
        send_string = ""
        for i in r:
            send_string = send_string + i + '\n'
        send_json_data_str = {
            "Answer" : send_string,
            "Link": "https://coop.koreatech.ac.kr/dining/menu.php"
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
    elif intent_predict[0] == 0:
        print(78)
        #수강이력 가져오기(일단 졸업요건 레이블 사용)
        studentnumscrap = Scrap()
        r = studentnumscrap.scrapStudentNumber(host_response)

        start_year = ''.join(filter(str.isdigit, r))[:4]
        coursehistoryscrap = Scrap()
        chlist = coursehistoryscrap.scrapCourseHistory(user_id, int(start_year)) #수강이력 리스트(포맷: 과목명(분반))
        for i in chlist:
            print(i)
        '''
        send_string = ""
        for i in chlist:
            send_string = send_string + i + '\n'
        send_json_data_str = {
            "Answer" : send_string,
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode()) 
        '''
        
    else :
        #졸업요건, 과목추천 의도 보냄
        send_json_data_str = {
            "Intent": intent_predict[1],
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())

def get_lecture_recommend(conn,host_response,user_id):
    a = Recommender('../models/recommender/lecture_dic.txt','../models/recommender/lecture_model.bin')
    input_list = a.get_input_list(host_response,user_id)
    data = a.find_similar_list(input_list,5)
    send_json_data_str = {
        "recommend" : data
    }
    message = json.dumps(send_json_data_str)
    conn.send(message.encode())

host_response = None
user_id = ""
def to_client(conn, addr):
    global host_response
    global user_id
    #로그인 POST 요청 응답
    
    try:
        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)


        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        if "id" in recv_json_data:
            if "pw" in recv_json_data:
                        user_id = recv_json_data['id']
                        user_pw = recv_json_data['pw']
                        lmc = LoginMakeCookie(user_id, user_pw)
                        if user_pw == "logout":
                            lmc.logout()
                            send_json_data_str = {
                                "Logout": "로그아웃 성공!"
                            }
                            message = json.dumps(send_json_data_str)
                            conn.send(message.encode())
                        else:
                            host_response = lmc.makeCookie() #쿠키 생성 및 HOST 응답 저장

                            if (lmc.isLogin()):
                                studentnumscrap = Scrap()
                                studentnum = studentnumscrap.scrapStudentNumber(host_response)
                                emailscrap = Scrap()
                                email = emailscrap.scrapEmail(user_id)
                                start_year = ''.join(filter(str.isdigit, studentnum))[:4]
                                coursehistoryscrap = Scrap()
                                coursehistory = coursehistoryscrap.scrapCourseHistory(user_id, int(start_year))
                                send_json_data_str = {
                                    "LoginState": True,
                                    "StudentNumber": studentnum,
                                    "Email": email,
                                    "CourseHistory": coursehistory,
                                }
                            else:
                                send_json_data_str = {
                                    "LoginState": False
                                }
                            

                            message = json.dumps(send_json_data_str)
                            conn.send(message.encode())

        else:
            if recv_json_data['class'] == 'query' :
                #챗봇 
                send_chat_data(conn,recv_json_data)
            elif recv_json_data['class'] == 'recommend':
                #과목추천
                get_lecture_recommend(conn,host_response,user_id)
 
   

    except Exception as ex:
        print(ex)



if __name__ == '__main__':

    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
        ))
        client.start()
