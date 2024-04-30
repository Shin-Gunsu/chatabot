import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic=file_path + '/../train_tools/dict/chatbot_dict.bin',
               userdic= file_path + '/../utils/user_dict.txt')


ner = NerModel(model_name=file_path + '/../models/ner/ner_model.h5', proprocess=p)
query = '오늘 오전 13시 2분에 탕수육 하나에 깍두기 주문 하고 싶어요'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)

