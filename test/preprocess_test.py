

import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.Preprocess_komoran import Preprocess

sent = "컴공 한기대 청솔관 껌퓨터꽁핚뿌 컴퓨터공학부 "
p = Preprocess(word2index_dic=file_path+'/../train_tools/dict/chatbot_dict.bin',userdic = file_path + '/../utils/user_dict_test.tsv')

pos = p.pos(sent)
keywords = p.get_keywords(pos, without_tag=False)

print(keywords)
