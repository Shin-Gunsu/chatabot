import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel

p = Preprocess(word2index_dic=file_path+'/../train_tools/dict/chatbot_dict.bin',
               userdic=file_path + '/../utils/user_dict.txt')

intent = IntentModel(model_name=file_path + '/../models/intent/intent_model.h5', proprocess=p)
query = "졸업"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)