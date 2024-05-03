import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic=file_path + '/../train_tools/dict/chatbot_dict.bin',
               userdic= file_path + '/../utils/user_dict.txt')


ner = NerModel(model_name=file_path + '/../models/ner/ner_model.h5', proprocess=p)
query = '프론티어레코즈 고용서비스정책학과 코인노래방 한기대생활협동조합 컴퓨터공학부'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)


