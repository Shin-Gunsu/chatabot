import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
import sys
import os

file_path = os.path.dirname(__file__) 
sys.path.append(file_path+'../../../')
from utils.Preprocess import Preprocess

# 의도 분류 모델 불러오기
model = load_model(file_path + '/intent_model.h5')

query = "청솔관 어디지?"

p = Preprocess(word2index_dic=file_path + '/../../train_tools/dict/chatbot_dict.bin',
               userdic= file_path + '/../../utils/user_dict.txt')
pos = p.pos(query)
keywords = p.get_keywords(pos, without_tag=True)
seq = p.get_wordidx_sequence(keywords)
sequences = [seq]

# 단어 시퀀스 벡터 크기
from config.GlobalParams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')
intent_labels = {0: "졸업요건", 1: "위치", 2: "번호", 3: "과제"}
predict = model.predict(padded_seqs)
predict_class = tf.math.argmax(predict, axis=1)
print(query)
print("의도 예측 점수 : ", predict)
print("의도 예측 클래스 : ", predict_class.numpy())
print("의도  : ", intent_labels[predict_class.numpy()[0]])