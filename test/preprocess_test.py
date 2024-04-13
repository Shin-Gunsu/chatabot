from tensorflow.keras import preprocessing

import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess_komoran import Preprocess

sent = "한기대 컴공 고려대 컴공"
p = Preprocess(word2index_dic=file_path+'/../train_tools/dict/chatbot_dict.bin')

pos = p.pos(sent)
keywords = p.get_keywords(pos, without_tag=False)

print(keywords)
