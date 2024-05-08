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
from config.GlobalParams import gptapi_key

# 전처리 객체 생성
p = Preprocess(word2index_dic=file_path + '/train_tools/dict/chatbot_dict.bin',
               userdic=file_path + '/utils/user_dict.txt')

# 의도 파악 모델
intent = IntentModel(model_name=file_path + '/models/intent/intent_model.h5', proprocess=p)
print('의도 분류 모델 호출')
# 개체명 인식 모델
ner = NerModel(model_name=file_path + '/models/ner/ner_model.h5', proprocess=p)
print('개체명 인식 모델 호출')




def to_client(conn, addr):

    try:
        # db.connect()  # 디비 연결

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
        query = recv_json_data['query']

        # 의도 파악
        intent_model = FindIntent(intent)
        intent_predict = intent_model.classification(query)
        
        if intent_predict[0] == 0 or intent_predict[0] == 3 or intent_predict[0] == 4:
            #졸업요건, 과제, 과목추천
            send_json_data_str = {
                "Intent": intent_predict[1],
            }
            message = json.dumps(send_json_data_str)
            conn.send(message.encode())

        else :
            # 개체명 파악
            ner_predicts = ner.predict(query)
            ner_tags = ner.predict_tags(query)
            ner_list = []
            for keyword, tag in ner_predicts:
                if tag != 0 and tag != 1:
                    print(keyword, tag)
                    ner_list.append(keyword)

            #ASSISTANT 모델
            #thread id는 유저 생길때 마다 새로 부여해야함,유저 종료시 스레드 삭제
            thread_id = "thread_1CFWA8SZL27chvsuQXGcOkLX"
            assistant_model = GetAnswer_assistant(OpenAI(api_key=gptapi_key),thread_id)
            
            answer = assistant_model.ask(query)
            print(answer)
            send_json_data_str = {
                "Answer" : answer,
                "Intent": intent_predict[1],
                "Ner": ner_list
            }
            message = json.dumps(send_json_data_str)
            conn.send(message.encode())
            print(send_json_data_str)

  

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
