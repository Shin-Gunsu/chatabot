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
#랭체인 모델
#thread id는 유저 생길때 마다 새로 부여해야함,유저 종료시 스레드 삭제
thread_id = ""
langchain_model = GetAnswer_assistant(OpenAI(api_key=gptapi_key),thread_id)
print('랭체인 호출')


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

            # 답변 검색
            f = FindAnswer()
            answer_text, answer_image = f.search(intent_predict[1], ner_tags)
            answer_data = f.tag_to_word(ner_predicts, answer_text)

            #인식된 개체명이 없다면 현재정보로는 답할수 없는 정보 출력
            flag = 0
            for i in ner_tags:
                if i != 'O' :
                    flag = 1
            if flag ==1:
                answer = langchain_model.ask(query)

                send_json_data_str = {
                    "Query" : query,
                    "Answer": answer,
                    "AnswerImageUrl" : answer_image,
                    "Intent": intent_predict[1],
                    "NER": str(ner_predicts)
                }
                message = json.dumps(send_json_data_str)
                conn.send(message.encode())
            else:
                send_json_data_str = {
                    "Query" : query,
                    "Answer": "현재 정보로는 답할수 없는 정보입니다. 다시 입력해 주십시오.",
                    "AnswerImageUrl" : answer_image,
                    "Intent": intent_predict[1],
                    "NER": str(ner_predicts)
                }
                message = json.dumps(send_json_data_str)
                conn.send(message.encode())

    except Exception as ex:
        print(ex)

    # finally:
    #     if db is not None: # db 연결 끊기
    #         db.close()
    #     conn.close()


if __name__ == '__main__':

    # 질문/답변 학습 디비 연결 객체 생성
    # db = Database(
    #     host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    # )
    # print("DB 접속")

    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        # params = {
        #     "db": db
        # }

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            # params
        ))
        client.start()
