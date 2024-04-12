from tensorflow.keras import preprocessing
import sys
sys.path.append('../')
from utils.Preprocess_kiwi import Preprocess

sent = "빩때는 얼마야?"

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',userdic = '../utils/user_dict.txt')

pos = p.pos(sent)
keywords = p.get_keywords(pos, without_tag=False)

print(keywords)
