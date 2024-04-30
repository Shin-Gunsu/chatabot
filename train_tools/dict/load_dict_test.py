import pickle
import sys
import os
file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.

f = open(file_path + "/chatbot_dict.bin", "rb")
word_index = pickle.load(f)
f.close()

print(word_index['밥버러지'])