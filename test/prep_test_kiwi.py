from tensorflow.keras import preprocessing
import sys
sys.path.append('../../')
from chatbot.utils.Preprocess_kiwi import Preprocess

sent = "청솔관이 좋음 솔빛관이 좋음?"

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',userdic = '../utils/user_dict.txt')

pos = p.pos(sent)
keywords = p.get_keywords(pos, without_tag=False)

print(keywords)
