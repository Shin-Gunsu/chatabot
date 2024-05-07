import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic=file_path + '/../train_tools/dict/chatbot_dict.bin',
               userdic= file_path + '/../utils/user_dict.txt')


ner = NerModel(model_name=file_path + '/../models/ner/ner_model.h5', proprocess=p)
query = '물리학과 사무실 번호 알려줘'
predicts = ner.predict(query)
print(predicts)