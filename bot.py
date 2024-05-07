import threading
import json
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
        query = recv_json_data['Query']

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
                    ner_list.append(keyword)

            send_json_data_str = {
                "Intent": intent_predict[1],
                "Ner": ner_list
            }
            # 답변 검색
            f = FindAnswer()
            answer_text, answer_image = f.search(intent_predict[1], ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)

            send_json_data_str = {
                "Query" : query,
                "Answer": answer,
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
